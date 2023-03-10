from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model

from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import os
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import pandas as pd
import pickle

from google.cloud import storage
from zipfile import ZipFile
import io

BUCKET_NAME = '30k-images'

UNZIPPED_IMAGE_PATH = f"{os.getcwd()}/resources/unzipped_images/"
PICKLE_FILE_PATH = f"{os.getcwd()}/resources/"

def image_files(path):
    '''
    Creates a list with the names of the images to be processed.
    '''
    image_files = []
    # creates a ScandirIterator aliased as files
    with os.scandir(path) as files:
        for file in files:
            if file.name.endswith('.jpg'):
              # adds only the image files to the flowers list
                image_files.append(file.name)
    return image_files


def load_model():
    model = VGG16()
    model = Model(inputs = model.inputs, outputs = model.layers[-2].output)
    return model


def extract_features(file, path, model):
    '''
    Extract features of an image file using the VGG16 model.
    '''
    # load the image as a 224x224 array
    img = load_img(f'{path}/{file}', target_size=(224,224))
    # convert from 'PIL.Image.Image' to numpy array
    img = np.array(img)
    # reshape the data for the model reshape(num_of_samples, dim 1, dim 2, channels)
    reshaped_img = img.reshape(1,224,224,3)
    # prepare image for model
    imgx = preprocess_input(reshaped_img)
    # get the feature vector
    features = model.predict(imgx, use_multiprocessing=True)
    return features


def all_features(image_files, path, model):
    '''
    Extracts features of all files in a folder.
    '''
    data = {}
    for image in image_files:
    # extracts the features and update the dictionary
        feat = extract_features(image, path, model)
        image = image.split('/')[-1]
        data[image] = feat

    # splits the dictionary into 2 numpy arrays
    filenames = np.array(list(data.keys()))
    feat = np.array(list(data.values()))

    # saves the file names as a pickle file
    with open(f"{PICKLE_FILE_PATH}filenames.pkl", "wb") as file:
        pickle.dump(filenames, file)

    return feat


def pca(feat):
    '''
    Saves pickle files of the PCA model and the features after the PCA
    '''
    feat = feat.reshape(-1,4096)
    pca = PCA(n_components=100, random_state=22)
    pca.fit(feat)
    X = pca.transform(feat)
    with open(f"{PICKLE_FILE_PATH}features.pkl", "wb") as file:
        pickle.dump(X, file)
    with open(f"{PICKLE_FILE_PATH}pca.pkl", "wb") as file:
        pickle.dump(pca, file)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
  """Uploads a file to the bucket."""
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)

  blob.upload_from_filename(source_file_name)

  print('File {} uploaded to {}.'.format(
      source_file_name,
      destination_blob_name))

def batch_features(image_files, path, model, batch_size):
    '''
    Extracts features of all files in a folder.
    '''
    for i in range(0, len(image_files), batch_size):
        data = {}
        batch_files = image_files[i:i+batch_size]

        for image in batch_files:
            feat = extract_features(image, path, model)
            image = image.split('/')[-1]
            data[image] = feat

        filenames = np.array(list(data.keys()))
        feat = np.array(list(data.values()))

        with open(f"filenames_{i//batch_size}.pkl", "wb") as file:
            pickle.dump(filenames, file)

        with open(f"features_{i//batch_size}.pkl", "wb") as file:
            pickle.dump(feat, file)

        print(f'BATCH {i//batch_size+1} processed')

if __name__ == '__main__':
    mode = input("\n\n\nDo you want to train model from \n1. Images saved locally\n2. Images on the cloud\n")
    if mode == '1':
        path = input("Please provide the folder path: ")
    elif mode == '2':
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.get_blob('images_metropolitan.zip')

        object_bytes = blob.download_as_bytes()

        archive = io.BytesIO()
        archive.write(object_bytes)

        print(UNZIPPED_IMAGE_PATH)

        with ZipFile(archive) as zip_archive:
            zip_archive.extractall(UNZIPPED_IMAGE_PATH)
    else:
        print("Re enter choice 1 or 2")


    model = load_model()
    images = image_files(UNZIPPED_IMAGE_PATH)
    feat = all_features(images, UNZIPPED_IMAGE_PATH, model)
    pca(feat)

    upload_blob(BUCKET_NAME, f"{PICKLE_FILE_PATH}filenames.pkl", "filenames.pkl")
    upload_blob(BUCKET_NAME, f"{PICKLE_FILE_PATH}features.pkl", "features.pkl")
    upload_blob(BUCKET_NAME, f"{PICKLE_FILE_PATH}pca.pkl", "pca.pkl")

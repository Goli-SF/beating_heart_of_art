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
    with open("resources/filenames.pkl", "wb") as file:
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
    with open("resources/features.pkl", "wb") as file:
        pickle.dump(X, file)
    with open("resources/pca.pkl", "wb") as file:
        pickle.dump(pca, file)




if __name__ == '__main__':
    path = input("Please provide the folder path: ")
    model = load_model()
    images = image_files(path)
    feat = all_features(images, path, model)
    pca(feat)

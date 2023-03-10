from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
# models
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
# neighbors and dimension reduction
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
# for everything else
import os
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import pandas as pd
import pickle

# PROJECT_PATH = os.getcwd()
# RESOURCE_PATH = '/projects/interface/resources/'


class CModel():

    def __init__(self, resource_path=''):
        self.model = VGG16()
        self.model = Model(inputs=self.model.inputs,
                           outputs=self.model.layers[-2].output)
        self.pca = pickle.load(open(f"{resource_path}pca.pkl", "rb"))
        self.X = pickle.load(open(f"{resource_path}features.pkl", "rb"))
        self.filenames = pickle.load(
            open(f"{resource_path}filenames.pkl", "rb"))

    def get_model(self):
        # print("I AM NOW IN THE MAIN.PY MODULE")
        # model = VGG16()
        # model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
        # pca = pickle.load(open(f"{PROJECT_PATH}{RESOURCE_PATH}pca.pkl", "rb"))
        # X = pickle.load(
        #     open(f"{PROJECT_PATH}{RESOURCE_PATH}features.pkl", "rb"))
        # filenames = pickle.load(
        #     open(f"{PROJECT_PATH}{RESOURCE_PATH}filenames.pkl", "rb"))

        # print("model loaded")
        # return self.model, self.pca, self.X, self.filenames
        return self.pca, self.X, self.filenames

    def extract_features(self, image):
        '''
        Extract features of an image file using the selected model.
        '''
        # convert from 'PIL.Image.Image' to numpy array
        print(image.mode)
        # TODO: does not work with png
        img = image.convert('RGB')
        print("After convert Statememnt image type is :", image.mode)
        img = np.array(image)
        print(img.shape)
        # reshape the data for the model reshape(num_of_samples, dim 1, dim 2, channels)
        reshaped_img = img.reshape(1, 224, 224, 3)
        # prepare image for model
        imgx = preprocess_input(reshaped_img)
        # get the feature vector
        features = self.model.predict(imgx, use_multiprocessing=True)
        # pca of the features
        target = self.pca.transform(features)

        return target

    def find_neighbors(self, target, filenames, n_neighbors=5):
        '''
        Find the nearest neighbors of a target image.
        Returns a list with objectIDs
        '''
        neigh = NearestNeighbors(n_neighbors=n_neighbors)
        neigh.fit(self.X)
        kneighbors_index = neigh.kneighbors(
            target.reshape(1, -1))[1].tolist()[0]

        kneighbors = [int(filenames[neighbor].split('.')[0])
                      for neighbor in kneighbors_index]

        return kneighbors

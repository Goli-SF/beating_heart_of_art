from fastapi import FastAPI, File, UploadFile
from PIL import Image
import pandas as pd
from projects.interface.main import extract_features, find_neighbors, load_model
import os

PROJECT_PATH = os.getcwd()
RESOURCE_PATH = '/projects/interface/resources/'

app = FastAPI()
model, pca, X, filenames, images_df = load_model()

@app.get("/")
def root():
    return {
        'Message': '❤️ Welcome to the beating ❤️ of art ❤️ '
        }

@app.post("/uploader")
async def create_upload_file(file: UploadFile = File(...), num_of_results :int =5):
    uploaded_image = Image.open(file.file)
    #print(type(uploaded_image))
    resized_image = uploaded_image.resize((224,224))
    #print(type(resized_image))
    #print("Model loaded!!!")
    features = extract_features(resized_image, model, pca)
    #print("Features Extracted!!!")
    nearest_neighbors = find_neighbors(X = X, target = features, n_neighbors = num_of_results, filenames = filenames)
    print(nearest_neighbors)
    print(images_df.head(1))
    similar_images = images_df[images_df['id'].isin(nearest_neighbors)]
    print(similar_images)

    # create a categorical data type with the desired order as contained in the list nearest_neighbors
    cat_dtype = pd.CategoricalDtype(categories=nearest_neighbors, ordered=True)
    # convert the 'ObjectID' column to the categorical data type
    similar_images['id'] = similar_images['id'].astype(cat_dtype)
    # sort the DataFrame by the 'objectID' column
    similar_images = similar_images.sort_values('id')
    print("After Sorting")
    print(similar_images)
    # # replace NaN with empty string
    similar_images = similar_images.fillna('')
    result_dict = similar_images.to_dict('records')

    result = {'nearest_neighbours': result_dict}
    return result

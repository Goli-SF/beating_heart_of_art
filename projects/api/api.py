from fastapi import FastAPI, File, UploadFile
from PIL import Image
import pandas as pd
from projects.interface.main import extract_features, find_neighbors, load_model
import os

app = FastAPI()
PROJECT_PATH = os.getcwd()
RESOURCE_PATH = '/projects/interface/resources/'
model, pca, X, filenames = load_model() ## should be a function in Eric's code

@app.get("/recommend")
def dummy():
    return{
        'Message' : 'This page is supposed to return the N most similar images'
    }


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
    df = pd.read_csv(f'{PROJECT_PATH}{RESOURCE_PATH}image_links.csv')

    similar_images = df[df['objectID'].isin(nearest_neighbors)]
    print(similar_images)

    # create a categorical data type with the desired order as contained in the list nearest_neighbors
    cat_dtype = pd.CategoricalDtype(categories=nearest_neighbors, ordered=True)
    # convert the 'ObjectID' column to the categorical data type
    similar_images['objectID'] = similar_images['objectID'].astype(cat_dtype)
    # sort the DataFrame by the 'objectID' column
    similar_images = similar_images.sort_values('objectID')
    print("After Sorting")
    print(similar_images)
    # # replace NaN with empty string
    similar_images = similar_images.fillna('')
    result_dict = similar_images.to_dict('records')

    result = {'nearest_neighbours': result_dict}
    return result


'''
Response object back to Streamlit
V2 - more information
Let us return some dummy data for name, location, year for V1
        'nearest_neighbors': [{link: 'link1', 'name' : 'name1' , 'location' : 'Paris', 'year' : 1755}
            , {link: 'link2', 'name' : 'name2' , 'location' : 'London', 'year' : 1955}]

        }
'''
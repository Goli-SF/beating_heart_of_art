from fastapi import FastAPI, File, UploadFile
from PIL import Image
import pandas as pd
from interface.main import extract_features, find_neighbors, load_model

app = FastAPI()


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


@app.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...), num_of_results = 5):
    uploaded_image = Image.open(file.file)
    resized_image = uploaded_image.resize((224,224))

    model, pca, X, filenames = load_model() ## should be a function in Eric's code

    features = extract_features(resized_image, model, pca)
    nearest_neighbors = find_neighbors(X = X, features = features, n_neighbors = num_of_results, filenames = filenames)

    df = pd.read_csv('./resources/features.pkl"/image_links.csv')

    similar_images = df[df['objectID'] in nearest_neighbors]

    return {'nearest_neighbours': similar_images.to_dict('records')}

    #return output_dict #should return the list as written out below back to Gunther's streamliot

'''
Response object back to Streamlit


V2 - more information
Let us return some dummy data for name, location, year for V1
        'nearest_neighbors': [{link: 'link1', 'name' : 'name1' , 'location' : 'Paris', 'year' : 1755}
            , {link: 'link2', 'name' : 'name2' , 'location' : 'London', 'year' : 1955}]

        }
'''
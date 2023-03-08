from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
import pandas as pd
import shutil

app = FastAPI()


@app.get("/recommend")
def dummy():
    return {
        'Message': 'This page is supposed to return the N most similar images'
    }


@app.get("/")
def root():
    return {
        'Message': '❤️ Welcome to the beating ❤️ of art ❤️ '
    }


@app.post("/uploader")
async def create_upload_file(file: UploadFile = File(...), data={'num_of_results': 5}):

    uploaded_image = Image.open(file.file)

    resized_image = uploaded_image.resize((224, 224))

    # -- Dummy data
    df = pd.read_csv('image_links.csv')
    df_resized = df.head(int(data.get('num_of_results')))
    # replace NaN with empty string
    df_resized = df_resized.fillna('')
    result_dict = df_resized.to_dict('records')

    result = {'nearest_neighbours': result_dict}
    return result

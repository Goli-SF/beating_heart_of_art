from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
import pandas as pd
#import shutil

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
    uploaded_image = Image.open(BytesIO(file.file))
    resized_image = uploaded_image.resize((224,224)) #just to test if the Image.open works

    df = pd.read_csv('/home/krishnaram/code/image_links.csv')
    return {'nearest_neighbours': df.tail(num_of_results).to_dict('records')}
    #return output_dict #should return the list as written out below back to Gunther's streamliot

'''
Response object back to Streamlit


V2 - more information
Let us return some dummy data for name, location, year for V1
        'nearest_neighbors': [{link: 'link1', 'name' : 'name1' , 'location' : 'Paris', 'year' : 1755}
            , {link: 'link2', 'name' : 'name2' , 'location' : 'London', 'year' : 1955}]

        }
'''

'''
Request object from Streamlit

from fastapi import FastAPI, File, UploadFile
import shutil
@app.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...)):
   with open("destination.png", "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
   return {"filename": file.filename}

'''

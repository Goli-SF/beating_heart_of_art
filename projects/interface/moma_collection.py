import requests
from PIL import Image
import pandas as pd
import os
from io import BytesIO
import numpy as np
from ratelimit import limits, sleep_and_retry


def collect_and_clean(json_file_path):
    """
    collects the .json file of MoMa which is stored on the hard drive, cleans it,
    and saves it into a pickle file.
    """
    moma_data = pd.read_json('moma_artworks.json')
    moma_df=pd.DataFrame(moma_data)
    moma_df_update=moma_df[['ObjectID', 'Title', 'Artist', 'Date', 'Medium', 'URL', 'ThumbnailURL']]
    moma_df_update=moma_df_update[moma_df_update['Medium'].notna()]
    moma_df_update=moma_df_update[moma_df_update['ThumbnailURL'].notna()]
    moma_df_update=moma_df_update[moma_df_update['Date'].notna()]
    moma_df_update['intDate']= moma_df_update['Date'].apply(lambda x: int(x[:4]) if len(x)>3 and x[:3].isdigit() else 0)
    moma_df_update=moma_df_update[moma_df_update['intDate'].astype('int')>1900]
    moma_df_update.to_pickle('moma_df_update.pkl')


def image_preprocessor(image):
    """
    takes an image and changes its size to 224x224 pixels for feeding it to the model.
    """
    resized_image = image.resize((224,224))
    return resized_image


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def moma_downloader (pkl_file_path, download_dir):
    """
    reads a pkl file containing thumbnail links and downloads the images to the given path.
    """
    df = pd.read_pickle(pkl_file_path)
    for index, row in df[['ObjectID', 'ThumbnailURL']].iterrows():
        id= row['ObjectID']
        if pd.notna(row['ThumbnailURL']):
            url= row['ThumbnailURL']
            file_name= f'{id}.jpg'
            response = requests.get(
            url,
            headers={
                'authority': 'www.moma.org',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-GB,en;q=0.9',
                'cache-control': 'no-cache',
                'cookie': '_gorilla_csrf=MTY3ODM2NDY3NnxJa2xQYkV0b1NrSnJjaXREVnpWMGQwVTVMemx2TjFKdFNYWk9SREF4ZDFSc0syOXNhWFV5V1hONUszTTlJZ289fDzirBgF_op8ZBg9OrQRosZs96_OoyzzTRK4N2Z1Nm9U; viewedCookieBanner=true; sessionHighlightColor=0; global=MTY3ODM2NTA5NHxOd3dBTkVneVVWRkJXRmhZVGsxRE4wbGFWMUpPVUZCWFNUTTBWa3hCUWxkTlFVUmFVVnBJU1V4RFMwaENXRkkxV2swME5Vb3pXbEU9fMTTVMx8jUCEMc0rOJAX_SI4D3aqPgtr-geehbeVT9Pr',
                'dnt': '1',
                'pragma': 'no-cache',
                'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            }
            )

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                resized_image= image_preprocessor(image)
                file_name= f'{id}.jpg'
                resized_image.save(f"{download_dir}/{file_name}")
        if index%50==0:
            print(f'{index} images downloaded.')

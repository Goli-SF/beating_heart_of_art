import requests
from PIL import Image
import pandas as pd
import os
from io import BytesIO
import numpy as np

def df_from_csv(local_path):
    """
    creates a dataframe with the desired columns from the csv-file of the metropolitan museum of art.
    """

    metropol_csv=pd.read_csv(local_path)
    metropol_primary=pd.DataFrame(metropol_csv)
    metropol_df=metropol_primary[metropol_primary['Object Name'].isin(['Photograph', 'Painting', 'Drawing'])]
    image_links_df = metropol_df[['Object ID', 'Object Number', 'Title', 'Object Name',
                              'Artist Display Name', 'Country', 'Object Date', 'Medium', 'Classification']]
    image_links_df.columns=['objectID', 'objectNR', 'title', 'objectName', 'artistDisplayName','country',
                                       'objectDate', 'medium', 'classification']
    image_links_df.reset_index(inplace=True)
    image_links_df.drop('index', axis=1, inplace=True)

    return image_links_df



def imagelink_collector(df):
    """
    adds the 'imageURL' column to the input dataframe.
    """

    df['imageURL'] = ''
    for index, row in df.iterrows():

        result = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{row['objectID']}").json()

        if 'primaryImage' in result and result['primaryImage']:
            df.loc[index, 'imageURL'] = result['primaryImage']

        if index%50 == 0:
            print(f"processing row {index}")
    #dropnas
    df['imageURL'].replace('', np.nan, inplace=True)
    df = df[df['imageURL'].notna()]

    return df


def imagelink_csv_maker(df):
    """
    takes a dataframe that includes the imageURL-column and saves it as a csv-file on the hard drive.
    """
    df.to_csv('image_links.csv')


def image_downloader(local_path):
    """
    takes the path to a csv-file and downloads the images from the URLs provided in its imageURL-column.
    """
    df= pd.read_csv(local_path)
    for index, row in df[['objectID', 'imageURL']].iterrows():
        id= row['objectID']
        url= row['imageURL']

        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            resized_image = image.resize((224,224))
            file_name= f'{id}.jpg'
            resized_image.save(file_name)

import os
import streamlit as st
import pandas as pd
# import folium
# from streamlit_folium import st_folium
import requests
import json
import io
from PIL import Image


APP_TITLE = 'The beating heart of Art'
APP_SUB_TITLE = 'Find similar artwork from the Metropolitan Museum of Art'
PROJECT_FOLDER = os.getcwd()
PREDICTION_URL = os.getenv('PREDICTION_URL', 'http://localhost:8000/uploader')


def predict(image_data, num_of_results=10):
    # encode image_data as enctype="multipart/form-data and post ist to the API
    response = requests.post(
        PREDICTION_URL,
        files={'file': image_data},
        params={'num_of_results': num_of_results}
    )

    # Get the prediction
    prediction = response.json()

    # Convert the prediction to a dataframe
    df = pd.DataFrame(prediction.get('nearest_neighbours'))
    return df

    # df = pd.read_csv(
    #     PROJECT_FOLDER+"/"+'data/image_links.csv')
    # return df.head(num_of_results)


def display_image_grid(df):
    df = df.reset_index(drop=True)
    print('Reset index', df)
    st.header('Similar Artwork')
    col1, col2 = st.columns(2)
    for index, row in df.iterrows():
        if row.get('imageURL'):
            if index == 0 or index % 2 == 0:
                with col1:
                    image_link = row['imageURL']
                    # print image_link
                    st.write(image_link)
                    image = requests.get(image_link).content
                    image = Image.open(io.BytesIO(image))
                    st.image(image)
            else:
                with col2:
                    image_link = row['imageURL']
                    # print image_link
                    st.write(image_link)
                    image = requests.get(image_link).content
                    image = Image.open(io.BytesIO(image))
                    st.image(image)

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # file_uploader accepting images
    image = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    num_of_results = st.slider('How many results do you want?', 1, 10, 1)
    # import numpy as np
    # image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    # prediction_df = predict(image, num_of_results)

    if image is not None:
        # display image inline
        st.header('Uploaded Image')
        st.image(image, use_column_width=True)
        prediction_df = predict(image, num_of_results)
        # json_prediction = json.dumps(prediction_df)
        # print(json_prediction)
        # # if lenght of datafarme
        if len(prediction_df) > 0:
            st.header('Predictions')
            display_image_grid(prediction_df)
        else:
            st.write('No results found')


if __name__ == "__main__":
    main()

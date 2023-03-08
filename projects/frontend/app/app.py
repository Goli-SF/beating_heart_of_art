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
PREDICTION_URL = os.getenv('PREDICTION_URL', 'http://localhost:5000/predict')


def predict(image_data, num_of_results=5):
    # # Convert the image to a string
    # image_string = cv2.imencode('.jpg', image)[1].tostring()

    # encode image_data as enctype="multipart/form-data and post ist to the API
    # response = requests.post(
    #     PREDICTION_URL,
    #     files={'file': image_data},
    #     data={'num_of_results': num_of_results}
    # )

    # Get the prediction
    # prediction = json.loads(response.text)
    # df = pd.DataFrame(prediction)

    df = pd.read_csv(
        PROJECT_FOLDER+"/"+'data/image_links.csv')
    return df.head(num_of_results)


def display_image_grid(df):
    st.header('Similar Artwork')
    for index, row in df.iterrows():
        if row.get('imageURL'):
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
    num_of_results = st.slider('How many resukts do you want?', 1, 10, 1)
    # import numpy as np
    # image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    # prediction_df = predict(image, num_of_results)

    if image is not None:
        # display image inline
        st.header('Uploaded Image')
        st.image(image, use_column_width=True)
        prediction_df = predict(image, num_of_results)
        # if lenght of datafarme
        if len(prediction_df) > 0:
            st.header('Predictions')
            display_image_grid(prediction_df)
        else:
            st.write('No results found')


if __name__ == "__main__":
    main()

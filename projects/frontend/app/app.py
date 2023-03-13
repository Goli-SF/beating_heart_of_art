import os
import streamlit as st
import pandas as pd
# import folium
# from streamlit_folium import st_folium
import requests
import json
import io
from PIL import Image


APP_TITLE = 'The Beating Heart of Art'
APP_SUB_TITLE = 'Discover similar artworks from the Metropolitan Museum of Art and MOMA'
PROJECT_FOLDER = os.getcwd()
PREDICTION_URL = os.getenv('PREDICTION_URL', 'http://localhost:8000/uploader')


def predict(image_data, num_of_results=10):
    # encode image_data as enctype="multipart/form-data and post it to the API
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


def url_image_embedder (url):
    """
    this function decides if the link is from metropolitan or moma. Regarding that, it uses the proper method to get the image and
    embed it in the website.
    """
    if url.startswith('http://www.moma.org'):
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
        image = Image.open(io.BytesIO(response.content))
    else:
        image = requests.get(url).content
        image = Image.open(io.BytesIO(image))

    return image


def display_image_grid(df):
    """
    this function is based on the dataframe and not on the database.
    """
    df = df.reset_index(drop=True)
    #print('Reset index', df)
    st.header('The most similar artworks are:')

    def chunks(df, n):
        for i in range(0, len(df), n):
            yield df[i:i + n]

    for chunk in chunks(df, 2):
        # in the following if-statement, imageURL should be replaces with URL.
        with st.container():
            col1, col2 = st.columns(2)
            # if index == 0 or index % 2 == 0:
            with col1:
                row = chunk.iloc[0]
                image_link = row['URL']
                museum_link=row['source_URL']
                # museum_name=row['source']
                # date=row['date']
                # medium=row['medium']

                image=url_image_embedder(image_link)

                text=f"{row['title']} by {row['artist']}"
                st.image(image, use_column_width=True)
                st.caption(f"[{text}]({museum_link}")

            # else:
            with col2:
                # if second does not exists, skip teh rest
                if len(chunk) == 1:
                    continue

                row = chunk.iloc[1]
                image_link = row['URL']
                museum_link=row['source_URL']
                # museum_name=row['source']
                # date=row['date']
                # medium=row['medium']

                image=url_image_embedder(image_link)

                text=f"{row['title']} by {row['artist']}"
                st.image(image, use_column_width=True)
                st.caption(f"[{text}]({museum_link}")
                #st.caption(f"[{text}]({museum_link})\n{medium}, {date}\n from the collection of {museum_name}")

        st.write(
            """<style>
            [data-testid="stHorizontalBlock"] {
                align-items: baseline;
            }
            </style>
            """,
            unsafe_allow_html=True
            )


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # file_uploader accepting images
    image = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    num_of_results = st.slider('How many results do you want?', 1, 10, 3)
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

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

PREDICTION_URL = os.getenv('PREDICTION_URL')
print('---Prediction URL:', PREDICTION_URL)


def predict(image_data, num_of_results=10):
    # encode image_data as enctype="multipart/form-data and post it to the API
    try:
        response = requests.post(
            PREDICTION_URL,
            files={'file': image_data},
            params={'num_of_results': num_of_results}
        )
        # Get the prediction
        prediction = response.json()
    except Exception as e:
        print('Error:', e)
        return json.dumps({'error': str(e)})

    # Convert the prediction to a dataframe
    df = pd.DataFrame(prediction.get('nearest_neighbours'))
    return df

    # df = pd.read_csv(
    #     PROJECT_FOLDER+"/"+'data/image_links.csv')
    # return df.head(num_of_results)


def display_image_grid(df):
    df = df.reset_index(drop=True)
    # print('Reset index', df)
    st.header('The most similar artworks are:')
    # col1, col2 = st.columns(2)

    # function that yields a list of two rows at a dataframe at a time
    def chunks(df, n):
        for i in range(0, len(df), n):
            yield df[i:i + n]

    for chunk in chunks(df, 2):
        with st.container():
            col1, col2 = st.columns(2)
            # if index == 0 or index % 2 == 0:
            with col1:
                row = chunk.iloc[0]
                image_link = row['embed_url']
                # add link to open in new window
                st.markdown(
                    f"""<a href="{row['image_url']}" target="_blank" style="float: right;">Open at {row['source_name']}</a>""", unsafe_allow_html=True)

                st.image(image_link, use_column_width=True,
                         caption=f"{row['title']} by {row['artist']}")
            with col2:
                # if second does not exists, skip teh rest
                if len(chunk) == 1:
                    continue
                row = chunk.iloc[1]
                image_link = row['embed_url']
                # add link to open in new window
                st.markdown(
                    f"""<a href="{row['image_url']}" target="_blank" style="float: right;">Open at {row['source_name']}</a>""", unsafe_allow_html=True)

                st.image(image_link, use_column_width=True,
                         caption=f"{row['title']} by {row['artist']}")
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

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(APP_TITLE)
    # print current working directory
    print('---Current working directory:', os.getcwd())

    with col2:
        st.image('./static/beating-heart-reduced2-1.gif')

    st.caption(APP_SUB_TITLE)

    col3, col4 = st.columns(2)
    # file_uploader accepting images
    with col3:
        image = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

    with col4:
        img_file_buffer = st.camera_input("Take a picture")

    col5, col6 = st.columns(2)
    with col5:
        num_of_results = st.slider('How many results do you want?', 1, 10, 3)

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

    if img_file_buffer is not None:
        # display image inline
        st.header('Uploaded Image')
        st.image(img_file_buffer, use_column_width=True)
        prediction_df = predict(img_file_buffer, num_of_results)
        # json_prediction = json.dumps(prediction_df)
        # print(json_prediction)
        # # if lenght of datafarme
        if len(prediction_df) > 0:
            display_image_grid(prediction_df)
        else:
            st.write('No results found')


if __name__ == "__main__":
    main()

import requests
import pandas as pd
from database.database import DataStore

set_name = 'metropolitan'

db = DataStore(
    '/Users/guntherschulz/dev/beating_heart_of_art/database/database.db')

# # load pickle file moma_df_update.pkl
# df = pd.read_pickle('moma_rename.pkl')


# db.load_df_to_sqlite(df, 'moma')

# res = db.get_info_by_object_ids(
#     set_name, [470, 471])
# print(res['image_url'].values)

# # db.load_csv_to_sqlite('moma.csv', 'moma')

# print(db.list_all_tables())

r = db.get_info_by_ids(['MTRP-001a2270-0cb3-4c51-8b78-ee6bc58a8674',
                       'MOMA-adc4a537-6523-47a1-bbff-a9237fa68784'])
print(r)

# load pickle file moma_rename.pkl
# df = pd.read_pickle('moma_rename.pkl')
# print(df.columns)
# print(df.head())

# db.drop_table('moma')

t = db.return_table('moma')
# print column 'id' from head
print(t['id'].head())
print(t.columns)

# images = db.get_images(set_name)

# print(images.head())

# info = db.get_info_from_id('MTRP-001a2270-0cb3-4c51-8b78-ee6bc58a8674')
# print(info)

# count = db.count(set_name)
# print(count)

# url = 'https://www.moma.org/media/W1siZiIsIjIyNjUxMiJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDMwMHgzMDBcdTAwM2UiXV0.jpg?sha=481b05786494f6eb'

# file_name = url.split('/')[-1].split('?')[0]

# response = requests.get(
#     url,
#     headers={
#         'authority': 'www.moma.org',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'accept-language': 'en-GB,en;q=0.9',
#         'cache-control': 'no-cache',
#         'cookie': '_gorilla_csrf=MTY3ODM2NDY3NnxJa2xQYkV0b1NrSnJjaXREVnpWMGQwVTVMemx2TjFKdFNYWk9SREF4ZDFSc0syOXNhWFV5V1hONUszTTlJZ289fDzirBgF_op8ZBg9OrQRosZs96_OoyzzTRK4N2Z1Nm9U; viewedCookieBanner=true; sessionHighlightColor=0; global=MTY3ODM2NTA5NHxOd3dBTkVneVVWRkJXRmhZVGsxRE4wbGFWMUpPVUZCWFNUTTBWa3hCUWxkTlFVUmFVVnBJU1V4RFMwaENXRkkxV2swME5Vb3pXbEU9fMTTVMx8jUCEMc0rOJAX_SI4D3aqPgtr-geehbeVT9Pr',
#         'dnt': '1',
#         'pragma': 'no-cache',
#         'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"macOS"',
#         'sec-fetch-dest': 'document',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-site': 'none',
#         'sec-fetch-user': '?1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
#     }
# )

# # print status code
# # print(response.status_code)
# # save image
# with open(file_name, 'wb') as f:
#     f.write(response.content)

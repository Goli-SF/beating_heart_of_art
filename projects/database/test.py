import requests
from database.database import Database

db = Database('database.db', images_directory='.')

# db.load_csv_to_sqlite('metropolitan.csv', 'metropolitan')

# print(db.list_all_tables())

images = db.get_images('metropolitan')

print(images.head())

info = db.get_info_from_id('MTRP-001a2270-0cb3-4c51-8b78-ee6bc58a8674')
print(info)

# curl 'https://www.moma.org/media/W1siZiIsIjIyNjUxMiJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDMwMHgzMDBcdTAwM2UiXV0.jpg?sha=481b05786494f6eb' \
#   -H 'authority: www.moma.org' \
#   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
#   -H 'accept-language: en-GB,en;q=0.9' \
#   -H 'cache-control: no-cache' \
#   -H 'cookie: _gorilla_csrf=MTY3ODM2NDY3NnxJa2xQYkV0b1NrSnJjaXREVnpWMGQwVTVMemx2TjFKdFNYWk9SREF4ZDFSc0syOXNhWFV5V1hONUszTTlJZ289fDzirBgF_op8ZBg9OrQRosZs96_OoyzzTRK4N2Z1Nm9U; viewedCookieBanner=true; sessionHighlightColor=0; global=MTY3ODM2NTA5NHxOd3dBTkVneVVWRkJXRmhZVGsxRE4wbGFWMUpPVUZCWFNUTTBWa3hCUWxkTlFVUmFVVnBJU1V4RFMwaENXRkkxV2swME5Vb3pXbEU9fMTTVMx8jUCEMc0rOJAX_SI4D3aqPgtr-geehbeVT9Pr' \
#   -H 'dnt: 1' \
#   -H 'pragma: no-cache' \
#   -H 'sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   -H 'sec-fetch-dest: document' \
#   -H 'sec-fetch-mode: navigate' \
#   -H 'sec-fetch-site: none' \
#   -H 'sec-fetch-user: ?1' \
#   -H 'upgrade-insecure-requests: 1' \
#   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36' \
#   --compressed

url = 'https://www.moma.org/media/W1siZiIsIjIyNjUxMiJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDMwMHgzMDBcdTAwM2UiXV0.jpg?sha=481b05786494f6eb'

file_name = url.split('/')[-1].split('?')[0]

print(file_name)

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

# print status code
# print(response.status_code)
# save image
with open(file_name, 'wb') as f:
    f.write(response.content)

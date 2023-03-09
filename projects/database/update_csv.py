import pandas as pd
import uuid
import os
# load image_links.csv

INPUT_CSV = 'image_links.csv'
OUTPUT_CSV = 'image_links_new.csv'
MTRP_IMAGE_PATH = 'metropolitan'
OLD_IMAGE_COLUMN_NAME = 'objectID'
IMAGE_URL_COLUMN_NAME = 'imageURL'


def udpate():
    if not os.path.exists(OUTPUT_CSV):
        # create a dataframe with the desired columns from the csv-file of the metropolitan museum of art.
        metropol_csv = pd.read_csv(INPUT_CSV)
        # add collumn with unique id
        metropol_csv['id'] = metropol_csv.apply(
            lambda _: 'MTRP' + '-' + str(uuid.uuid4()), axis=1)
        # add collumn set_name
        metropol_csv['set_name'] = MTRP_IMAGE_PATH
        metropol_csv['image_name'] = metropol_csv['id'] + '.jpg'
        # save to csv
        metropol_csv.to_csv(OUTPUT_CSV, index=False)
        return True
    else:
        print(f'{OUTPUT_CSV} already exists')
        return False


def rename():
    metropol_csv = pd.read_csv(OUTPUT_CSV)
    # rename all images. they right now have the name of column 'objectID'. rename them to the unique id
    for index, row in metropol_csv.iterrows():
        if os.path.exists(f'{row["set_name"]}/{row[OLD_IMAGE_COLUMN_NAME]}.jpg'):
            os.rename(f'{row["set_name"]}/{row[OLD_IMAGE_COLUMN_NAME]}.jpg',
                      f'{row["set_name"]}/{row["image_name"]}')
        elif os.path.exists(f'{row["set_name"]}/{row["image_name"]}'):
            # print(f'{row["image_name"]}.jpg already exists')
            pass
        else:
            # print(f'{row["set_name"]}/{row["objectID"]}.jpg does not exist')
            print(f'{row[IMAGE_URL_COLUMN_NAME]}')
            # remove row from csv
            metropol_csv.drop(index, inplace=True)
    metropol_csv.to_csv(OUTPUT_CSV, index=False)


if udpate():
    rename()

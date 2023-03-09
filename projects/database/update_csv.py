import pandas as pd
import uuid
import os
# load image_links.csv

MTRP_IMAGE_PATH = 'metropolitan'


def udpate():
    # create a dataframe with the desired columns from the csv-file of the metropolitan museum of art.
    metropol_csv = pd.read_csv('image_links.csv')
    # add collumn with unique id
    metropol_csv['id'] = metropol_csv.apply(
        lambda _: 'MTRP' + '-' + str(uuid.uuid4()), axis=1)
    # add collumn set_name
    metropol_csv['set_name'] = MTRP_IMAGE_PATH
    # add .jpg to the end of the image_path
    # metropol_csv['image_path'] = MTRP_IMAGE_PATH + \
    #     '/' + metropol_csv['id'] + '.jpg'
    metropol_csv['image_name'] = metropol_csv['id'] + '.jpg'
    # save to csv
    metropol_csv.to_csv('image_links_new.csv', index=False)


def rename():
    metropol_csv = pd.read_csv('image_links_new.csv')
    # rename all images. they right now have the name of column 'objectID'. rename them to the unique id
    for index, row in metropol_csv.iterrows():
        if os.path.exists(f'{row["set_name"]}/{row["objectID"]}.jpg'):
            os.rename(f'{row["set_name"]}/{row["objectID"]}.jpg',
                      f'{row["set_name"]}/{row["image_name"]}')
        elif os.path.exists(f'{row["set_name"]}/{row["image_name"]}'):
            # print(f'{row["image_name"]}.jpg already exists')
            pass
        else:
            # print(f'{row["set_name"]}/{row["objectID"]}.jpg does not exist')
            print(f'{row["imageURL"]}')
            # remove row from csv
            metropol_csv.drop(index, inplace=True)
            # save
            # break
    metropol_csv.to_csv('image_links_new.csv', index=False)


rename()

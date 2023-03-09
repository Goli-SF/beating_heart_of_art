import argparse
import pandas as pd
import uuid
import os
# load image_links.csv


def drop_columns(columns_to_drop, csv_file_name):
    csv = pd.read_csv(csv_file_name)
    csv.drop(columns_to_drop, axis=1, inplace=True)
    csv.to_csv(csv_file_name, index=False)


def udpate(prefix, output_csv, input_csv, image_name, image_file_type='jpg'):
    if not os.path.exists(output_csv):
        # create a dataframe with the desired columns from the csv-file of the metropolitan museum of art.
        csv = pd.read_csv(input_csv)
        # add collumn with unique id
        csv['id'] = csv.apply(
            lambda _: prefix + '-' + str(uuid.uuid4()), axis=1)
        # add collumn set_name
        csv['set_name'] = image_name
        csv['image_name'] = csv['id'] + '.' + image_file_type
        # save to csv
        csv.to_csv(output_csv, index=False)
        return True
    else:
        print(f'{output_csv} already exists')
        return False


def rename(output_csv, old_image_column_name, image_url_column_name, image_file_type='jpg'):
    csv = pd.read_csv(output_csv)
    # rename all images. they right now have the name of column 'objectID'. rename them to the unique id
    for index, row in csv.iterrows():
        if os.path.exists(f'{row["set_name"]}/{row[old_image_column_name]}.{image_file_type}'):
            os.rename(f'{row["set_name"]}/{row[old_image_column_name]}.{image_file_type}',
                      f'{row["set_name"]}/{row["image_name"]}')
        elif os.path.exists(f'{row["set_name"]}/{row["image_name"]}'):
            # print(f'{row["image_name"]}.jpg already exists')
            pass
        else:
            # print(f'{row["set_name"]}/{row["objectID"]}.jpg does not exist')
            print(f'{row[image_url_column_name]}')
            # remove row from csv
            csv.drop(index, inplace=True)
    csv.to_csv(output_csv, index=False)


dataset_name = 'metropolitan'

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_name', type=str, default=dataset_name,
                    help='the name of the dataset')


def main():
    if dataset_name == 'metropolitan':
        prefix = 'MTRP'
        input_csv = 'metropolitan_in.csv'
        image_path = 'metropolitan'
        output_csv = image_path + '.csv'
        old_image_column_name = 'objectID'
        image_url_column_name = 'imageURL'
        # if direcory dataset_name exists
        if os.path.exists(image_path):
            if udpate(prefix, output_csv, input_csv, image_path):
                drop_columns(['oid'], output_csv)
                rename(output_csv, old_image_column_name, image_url_column_name)


if __name__ == '__main__':
    main()

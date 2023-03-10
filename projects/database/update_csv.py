import argparse
import pandas as pd
import uuid
import os
# load image_links.csv


def drop_columns(columns_to_drop, csv_file_name):
    csv = pd.read_csv(csv_file_name)
    csv.drop(columns_to_drop, axis=1, inplace=True)
    csv.to_csv(csv_file_name, index=False)


def udpate(prefix, df, image_name, image_file_type='jpg'):
    # if not os.path.exists(output_csv):
    # create a dataframe with the desired columns from the csv-file of the metropolitan museum of art.
    # input_df = pd.read_csv(input_csv)
    # add collumn with unique id
    df['id'] = df.apply(
        lambda _: prefix + '-' + str(uuid.uuid4()), axis=1)
    # add collumn set_name
    df['set_name'] = image_name
    df['image_name'] = df['id'] + '.' + image_file_type
    # save to csv
    # input_df.to_csv(output_csv, index=False)
    return df


def rename(df, old_image_column_name, images_source_path, image_file_type='jpg'):
    # rename all images. they right now have the name of column 'objectID'. rename them to the unique id
    for index, row in df.iterrows():
        if os.path.exists(f'{images_source_path}/{row["set_name"]}/{row[old_image_column_name]}.{image_file_type}'):
            os.rename(f'{images_source_path}/{row["set_name"]}/{row[old_image_column_name]}.{image_file_type}',
                      f'{images_source_path}/{row["set_name"]}/{row["image_name"]}')
        elif os.path.exists(f'{row["set_name"]}/{row["image_name"]}'):
            # print(f'{row["image_name"]}.jpg already exists')
            pass
        else:
            print(
                f'{images_source_path}/{row["set_name"]}/{row[old_image_column_name]}.{image_file_type} does not exist')
            # print(f'{row[image_url_column_name]}')
            # remove row from csv
            df.drop(index, inplace=True)
    return df


dataset_name = 'moma'

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_name', type=str, default=dataset_name,
                    help='the name of the dataset')


def main():
    if dataset_name == 'metropolitan':
        prefix = 'MTRP'
        input_csv = 'image_links.csv'
        image_path = 'metropolitan'
        # output_csv = image_path + '.csv'
        output_csv = image_path + 'image_links_new.csv'
        old_image_column_name = 'objectID'
        image_file_type = 'jpg'
        # if direcory dataset_name exists
        if os.path.exists(image_path):
            if udpate(prefix, output_csv, input_csv, image_path, image_file_type=image_file_type):
                drop_columns(['oid'], output_csv)
                rename(output_csv, old_image_column_name,
                       image_file_type=image_file_type)

    if dataset_name == 'moma':
        prefix = 'MOMA'
        input_df_pickle = 'moma_df_update.pkl'
        df = pd.read_pickle(input_df_pickle)
        image_path = 'moma'
        # output_csv = image_path + '.csv'
        output_csv = 'moma.csv'
        old_image_column_name = 'ObjectID'
        image_file_type = 'jpg'
        images_source_path = '../../img'
        # if direcory dataset_name exists
        update_df = None
        update_df = udpate(prefix, df, image_path,
                           image_file_type=image_file_type)
        print(update_df)
        # if new_df:
        #     drop_columns(['oid'], output_csv)

        if os.path.exists(images_source_path):
            rename_df = rename(df, old_image_column_name, images_source_path,
                               image_file_type=image_file_type)
            # pickle the dataframe
            rename_df.to_pickle('moma_rename.pkl')


if __name__ == '__main__':
    main()

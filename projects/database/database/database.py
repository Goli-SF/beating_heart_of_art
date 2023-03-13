import sqlite3
import pandas as pd
import os


class DataStore:

    table_names = ['metropolitan', 'moma']
    source_names = ['Metropolitan Museum of Art', 'Museum of Modern Art']
    prefixes = ['MTRP', 'MOMA']
    image_url_names = ['imageURL', 'URL']
    embed_url_names = ['imageURL', 'ThumbnailURL']
    title_names = ['title', 'Title']
    artist_names = ['artistDisplayName', 'Artist']

    def __init__(self, database_name):
        self.database_name = database_name

    def count(self, table_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            f'SELECT COUNT(*) FROM {table_name}', conn)

        # close the connection
        conn.close()

        return df

    def list_all_tables(self):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table'", conn)

        # close the connection
        conn.close()

        return df

    def drop_table(self, table_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            f'DROP TABLE {table_name}', conn)

        # close the connection
        conn.close()

        return True

    def return_table(self, table_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            f'SELECT * FROM {table_name}', conn)

        # close the connection
        conn.close()

        return df

    def get_image_paths(self, table_name, images_directory="./"):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            f'SELECT id, set_name, image_name FROM {table_name}', conn)

        # close the connection
        conn.close()

        # add full path column using path.join
        df['full_path'] = df.apply(
            lambda row: os.path.join(images_directory, row['set_name'], row['image_name']), axis=1)

        # print columns
        # print('columns:', df.columns)

        return df

    def get_info_by_ids(self, ids=[]):
        '''
        Return a dataframe with the following columns:
        id, image_url, embed_url, source_name
        '''

        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        output_df = pd.DataFrame()

        separated_ids = {}
        for idx in ids:
            prefix = idx[:4]
            if prefix not in separated_ids:
                separated_ids[prefix] = []
            separated_ids[prefix].append(idx)

        for prefix in separated_ids:
            table_name = self.table_names[self.prefixes.index(prefix)]

            ids_to_find = separated_ids[prefix]
            token = "','".join(ids_to_find)

            # return all rows with object_id is in object_ids
            df = pd.read_sql_query(
                f"SELECT * FROM {table_name} WHERE id IN ('{token}')", conn)

            image_url_name = self.image_url_names[self.prefixes.index(
                prefix)]
            embed_url_name = self.embed_url_names[self.prefixes.index(
                prefix)]
            title_name = self.title_names[self.prefixes.index(
                prefix)]
            artist_name = self.artist_names[self.prefixes.index(
                prefix)]
            source_name = self.source_names[self.prefixes.index(prefix)]

            # copy the image url to a column called image_url
            df['image_url'] = df[image_url_name]
            # copy the embed url to a column called embed_url
            df['embed_url'] = df[embed_url_name]

            # copy the full name to a column called full_name
            df['source_name'] = source_name

            # copy the title to a column called title
            df['title'] = df[title_name]

            # copy the artist to a column called artist
            df['artist'] = df[artist_name]

            # only keep columns id, image_url, embed_url
            df = df[['id', 'image_url', 'embed_url',
                     "source_name", "title", "artist"]]

            # append to output_df
            output_df = output_df.append(df)

        # close the connection
        conn.close()

        return output_df

    def get_info_by_object_ids(self, table_name, object_ids=[]):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # convert object_ids to string
        object_ids = [str(object_id) for object_id in object_ids]

        # return all rows with object_id is in object_ids
        df = pd.read_sql_query(
            f"SELECT * FROM {table_name} WHERE objectID IN ({','.join(object_ids)})", conn)

        image_url_name = self.image_url_names[self.table_names.index(
            table_name)]
        embed_url_name = self.embed_url_names[self.table_names.index(
            table_name)]

        # copy the image url to a column called image_url
        df['image_url'] = df[image_url_name]
        # copy the embed url to a column called embed_url
        df['embed_url'] = df[embed_url_name]

        # close the connection
        conn.close()

        return df

    def rename_columns(self):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            f'SELECT * FROM metropolitan LIMIT 5', conn)

        # rename column
        df.rename(columns={'objectID': 'id'}, inplace=True)

        # print columns
        print('columns:', df.columns)

        # close the connection
        conn.close()

    def load_csv_to_sqlite(self, csv_file_name, table_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_csv(csv_file_name)

        # save to sqlite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        # print the first 5 rows from the database
        print(pd.read_sql_query(f'SELECT * FROM {table_name} LIMIT 5', conn))

        # commit
        conn.commit()

        # close the connection
        conn.close()

    def load_sqlite_to_csv(self, table_name, csv_file_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)

        # save to sqlite database
        df.to_csv(csv_file_name, index=False)

        # print the first 5 rows from the database
        print(pd.read_csv(csv_file_name).head())

        # close the connection
        conn.close()

    def load_df_to_sqlite(self, df, table_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # print head
        print(df.head())

        # # convert all values so they can be saved to sqlite
        # df = df.applymap(lambda x: str(x) if isinstance(x, list) else x)

        # if instance of list, convert to comma separated string
        df = df.applymap(lambda x: ','.join(x) if isinstance(x, list) else x)

        # save to sqlite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        # print the first 5 rows from the database
        print(pd.read_sql_query(f'SELECT * FROM {table_name} LIMIT 5', conn))

        # commit
        conn.commit()

        # close the connection
        conn.close()

from database.database import Database

db = Database('database.db', images_directory='.')

# db.load_csv_to_sqlite('metropolitan.csv', 'metropolitan')

# print(db.list_all_tables())

images = db.get_images('metropolitan')

print(images.head())

info = db.get_info_from_id('MTRP-001a2270-0cb3-4c51-8b78-ee6bc58a8674')
print(info)

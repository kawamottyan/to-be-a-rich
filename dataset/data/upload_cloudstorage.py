from google.cloud import storage

key_name ="../key/storage_key.json"
bucket_name = "keiba_csv_upload_bucket"
#race_file_upload = 'race_takamatsu.csv'
#race_file_name = '../data/main/race_data.csv'

def upload(key_name,bucket_name, file_upload, file_name):
    client = storage.Client.from_service_account_json(key_name)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_upload)
    blob.upload_from_filename(file_name)

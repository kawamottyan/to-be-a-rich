from google.cloud import storage
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../key/keiba-owner-gcp-key.json'
key_name ="../key/keiba-owner-gcp-key.json"
#race_file_upload = 'race_takamatsu.csv'
#race_file_name = '../data/main/race_data.csv'


def create_bucket(bucket_name):
    """Create a new bucket in specific location with storage class"""
    storage_client = storage.Client().from_service_account_json(key_name)
    bucket = storage_client.bucket(bucket_name)
    new_bucket = storage_client.create_bucket(bucket, location="asia-northeast1")
    print(f"Created bucket: {new_bucket.name}")
    return new_bucket

def upload(bucket_name, file_upload, file_name):
    client = storage.Client.from_service_account_json(key_name)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_upload)
    blob.upload_from_filename(file_name)

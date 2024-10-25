import firebase_admin
from firebase_admin import credentials, firestore, storage
import requests
import os
import time

# Initialize Firebase Admin
cred = credentials.Certificate('')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'caca-c9b2tk.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

# Function to save images
def save_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        image_path = os.path.join('/home/ronak/images', file_name)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved as {file_name}")
    else:
        print(f"Failed to download image from {url}")

# Function to fetch new documents from Firestore and save images
def fetch_and_save_images():
    collection_ref = db.collection('imageLink')
    docs = collection_ref.stream()

    for doc in docs:
        data = doc.to_dict()
        image_url = data.get('image')
        image_name = data.get('name')

        # Save image if both URL and name exist
        if image_url and image_name:
            save_image(image_url, f'{image_name}.jpg')

# Continuously check for new images
while True:
    print("Checking for new images...")
    fetch_and_save_images()
    time.sleep(60)  # Wait for 60 seconds before checking again

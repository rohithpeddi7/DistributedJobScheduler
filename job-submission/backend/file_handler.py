import firebase_admin
from firebase_admin import credentials, storage
from uuid import uuid4
import io


cred = credentials.Certificate("firebase-creds.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'dockerfile-f6553.firebasestorage.app'
})
bucket = storage.bucket()

async def add_file(file):
    
    file_content = await file.read()
    destination_blob_name = f"uploads/{uuid4()}+{file.filename}"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(io.BytesIO(file_content), content_type=file.content_type)

    blob.make_public()

    return {
        "filename": file.filename,
        "firebase_path": destination_blob_name,
        "public_url": blob.public_url
    }

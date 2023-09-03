import cloudinary.uploader
import boto3
from botocore.exceptions import NoCredentialsError
import os

# Cloudinary Configuration
cloud_name = "durdi1oak"
api_key = "164254991127435"
api_secret = "i8Lzr2SSRJCAlHS_6l0NVqrDkc4"

# AWS S3 Configuration
aws_access_key_id = "AKIA3CDQKC32YVT7XJXH"
aws_secret_access_key = "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"
aws_bucket_name = "xtraroms"
aws_s3_region_name = "eu-north-1"

# Initialize Cloudinary
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)

# Initialize AWS S3 Client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_s3_region_name
)

# List all files in your S3 bucket
s3_files = s3.list_objects(Bucket=aws_bucket_name)

# Migrate each file to Cloudinary with the correct public ID
for s3_file in s3_files.get('Contents', []):
    s3_object_key = s3_file['Key']

    try:
        # Generate the S3 URL for the file
        s3_url = f"https://{aws_bucket_name}.s3.{aws_s3_region_name}.amazonaws.com/{s3_object_key}"

        # Extract the filename from the S3 object key
        filename = os.path.basename(s3_object_key)

        # Remove the file extension to use as the public ID
        public_id = os.path.splitext(filename)[0]

        # Upload the S3 file to Cloudinary with the correct public ID
        target_folder = "media/images/"  # Modify this to your desired folder
        cloudinary_response = cloudinary.uploader.upload(
            s3_url,
            folder=target_folder,  # Specify the target folder in Cloudinary
            public_id=public_id  # Use the extracted filename as the public ID
        )

        # Print a success message
        print(f"Uploaded {s3_object_key} to Cloudinary as {cloudinary_response['url']}")

    except NoCredentialsError:
        print("AWS credentials not available")

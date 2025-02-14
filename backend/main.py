from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ✅ Missing Import
from pydantic import BaseModel
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

app = FastAPI()

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class BucketRequest(BaseModel):
    bucket_name: str

def create_bucket(bucket_name: str):
    """
    Creates an S3 bucket in the specified AWS region.
    """
    if not AWS_REGION:
        raise HTTPException(status_code=400, detail="AWS_REGION must be set in your .env file.")

    try:
        # Initialize S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )

        # Configure CreateBucketConfiguration only if not in us-east-1
        if AWS_REGION == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
            )

        return {"message": f"Bucket '{bucket_name}' created successfully in region '{AWS_REGION}'!"}

    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create-bucket/")
async def create_s3_bucket(request: BucketRequest):
    return create_bucket(request.bucket_name)

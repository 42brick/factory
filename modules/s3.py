"""
s3_connect, download / upload / delete
bolee, suschoi 2022.07.21
"""

import os
import boto3
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path("[.env 파일 상대경로]")
load_dotenv(dotenv_path=dotenv_path)

AWS_ACCESS_KEY_ID = os.getenv("[access key]")
AWS_SECRET_ACCESS_KEY = os.getenv("[secret key]")
AWS_DEFAULT_REGION = "ap-northeast-2"
AWS_BUCKET_NAME = "42brick-s3"

def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name=AWS_DEFAULT_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!") 
        return s3
        
s3 = s3_connection()
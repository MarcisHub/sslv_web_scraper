#!/usr/bin/env python3

""" This module downloads the latest file from an AWS S3 bucket """
import os
import boto3
import logging
from logging import handlers
from logging.handlers import RotatingFileHandler
import shutil
import sys


log = logging.getLogger('file_downloader')
log.setLevel(logging.INFO)
ws_log_format = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] "
    " [%(levelname)-5.5s] %(name)s : "
    "%(funcName)s: %(lineno)d: %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(ws_log_format)
log.addHandler(ch)

fh = handlers.RotatingFileHandler('file_downloader.log',
                                  maxBytes=(1048576*5),
                                  backupCount=7)
fh.setFormatter(ws_log_format)
log.addHandler(fh)


S3_LAMBDA_BUCKET_NAME = "lambda-ogre-scraped-data-marcitis"
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

try:
    s3 = boto3.client('s3', region_name="eu-west-1",
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
except Exception as e:
    log.error(f"Error connecting to AWS S3: {e}")
    sys.exit(1)


def download_file_from_s3(remote_file_name: str) -> None:
    """ Downloads a file from an AWS S3 bucket to the current directory """
    curr_dir = os.getcwd()
    if remote_file_name is None:
        log.error("No file name retrieved from S3. Skipping download.")
        return
    local_path_fn = os.path.join(curr_dir, remote_file_name)
    log.info(f"Local path file name: {local_path_fn}")
    try:
        log.info(f"Trying to download {remote_file_name} from S3 bucket: {S3_LAMBDA_BUCKET_NAME}")
        s3.download_file(S3_LAMBDA_BUCKET_NAME, remote_file_name, local_path_fn)
        log.info(f"File {remote_file_name} downloaded successfully.")
    except Exception as err:
        log.error(f"File download failed: {err}")


def get_last_file_name(s3_bucket_name: str) -> str:
    """ Returns the file name of the object based on the LastModified attribute """
    log.info(f"Getting last object from S3 bucket: {s3_bucket_name}")
    try:
        objs = s3.list_objects_v2(Bucket=s3_bucket_name).get('Contents', [])
        if objs:
            last_added = max(objs, key=lambda x: x['LastModified'])['Key']
            log.info(f"Found last S3 bucket object: {last_added}")
            return last_added
        else:
            log.warning(f"No objects found in S3 bucket: {s3_bucket_name}")
            return None
    except Exception as e:
        log.error(f"Error occurred while listing objects in S3 bucket: {e}")
        return None


def move_file_to(folder: str, src_file_name: str, dst_file_name: str) -> None:
    """ Moves a file into the specified folder """
    if not os.path.exists(folder):
        os.makedirs(folder)
    src_path = os.path.join(os.getcwd(), src_file_name)
    dst_path = os.path.join(folder, dst_file_name)
    try:
        shutil.move(src_path, dst_path)
        log.info(f"File {src_file_name} moved to {dst_path}")
    except Exception as e:
        log.error(f"Error moving {src_file_name} to {dst_path}: {e}")


def download_latest_lambda_file() -> None:
    """ Main entry point """
    last_modified_file_name = get_last_file_name(S3_LAMBDA_BUCKET_NAME)
    if last_modified_file_name:
        download_file_from_s3(last_modified_file_name)
        move_file_to('local_lambda_raw_scraped_data', last_modified_file_name, last_modified_file_name)
    else:
        log.warning("No file found in S3 bucket. Skipping download and move operations.")


if __name__ == "__main__":
    download_latest_lambda_file()
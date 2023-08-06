import boto3
import mimetypes
from six.moves.urllib.parse import urlencode
from io import BytesIO
import pandas as pd
from PIL import Image
import pickle
import json
import h5py
import s3fs
import numpy as np
import os
import logging
import re
from botocore.exceptions import ClientError

client = boto3.client('s3') #low-level functional API
s3_resource = boto3.resource('s3')

def s3_upload_file(bucketName, key, localFilePath, contentType=' ',tagging = ' ',storageClass='STANDARD'):
    """
    Arguments:
    ------------------------------------------------------------------------------------------------------------------------------------
    bucketName    : Type - string     | The Object's bucket_name identifier | **[REQUIRED]**  |
    key           : Type - string     | S3 The Object's key identifier      | **[REQUIRED]**  | Example., "example-folder/filename.csv" |
    localFilePath : Type - string     | File path in local directory        | **[REQUIRED]**  |
    contentType   : Type - string     | Media type of the given oobject     | Example., for .csv file contentType is 'text/csv'
    tagging       : Type - dictionary | Input Tags for the given object     | Example., {"key1":"value1","key2":"value2"}
    storageClass  : Type - string     | S3 storage class of the object      | [Optional]
    ------------------------------------------------------------------------------------------------------------------------------------
    Output        : Returns "Success" if upload has been done.
    """
    if key[0] == "/":
        return "Please Don't include '/' at the intial of key"
    if contentType == ' ':
        contentType = mimetypes.guess_type(localFilePath, strict=True)[0]
    if tagging == ' ':
        s3_resource.Object(bucketName, key).upload_file(Filename=localFilePath, ExtraArgs={'StorageClass': storageClass,'ContentType':contentType})
    else:
        s3_resource.Object(bucketName, key).upload_file(Filename=localFilePath, ExtraArgs={'StorageClass': storageClass,'ContentType':contentType,'Tagging': urlencode(tagging)})
    return "Success"


def s3_read_csv(bucketName, key):
    """
    Arguments:
    ---------------------------------------------------------------------------------------
    bucketName  : Type - string | The bucket name containing the object | **[REQUIRED]**  |
    key         : Type - string | Key of the object to get              | **[REQUIRED]**  |
    ---------------------------------------------------------------------------------------
    """
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket=bucketName, Key=key)
    return pd.read_csv(obj['Body'])

def s3_read_image(bucketName, key):
    """
    Arguments:
    ---------------------------------------------------------------------------------------
    bucketName  : Type - string | The bucket name containing the object | **[REQUIRED]**  |
    key         : Type - string | Key of the object to get              | **[REQUIRED]**  |
    ---------------------------------------------------------------------------------------
    """
    obj = client.get_object(Bucket=bucketName, Key=key)['Body'].read()
    return Image.open(BytesIO(obj))


def s3_read_pickle(bucketName, key):
    """
    Arguments:
    ---------------------------------------------------------------------------------------
    bucketName  : Type - string | The bucket name containing the object | **[REQUIRED]**  |
    key         : Type - string | Key of the object to get              | **[REQUIRED]**  |
    ---------------------------------------------------------------------------------------
    """
    return pickle.loads(s3_resource.Bucket(bucketName).Object(key).get()['Body'].read())


def s3_read_json(bucketName, key):
    """
    Arguments:
    ---------------------------------------------------------------------------------------
    bucketName  : Type - string | The bucket name containing the object | **[REQUIRED]**  |
    key         : Type - string | Key of the object to get              | **[REQUIRED]**  |
    ---------------------------------------------------------------------------------------
    """
    obj = client.get_object(Bucket=bucketName, Key=key)
    return json.loads(obj['Body'].read())

def s3_read_h5(s3FilePath):
    """
    Argument:
    --------------------------------------------------------------------------------
    s3FilePath  : Type - string | Object file path in s3         | **[REQUIRED]**  |
    --------------------------------------------------------------------------------
    """
    s3 = s3fs.S3FileSystem()
    return h5py.File(s3.open(s3FilePath))


def s3_create_empty_folder(bucket_name,folder_path):
    """
    Arguments:
    -------------------------------------------------------------------------------------------
    bucketName  : Type - string | The bucket name for containing the folder | **[REQUIRED]**  |
    folder_path : Type - string |  The Folder Path                          | **[REQUIRED]**  |
    -------------------------------------------------------------------------------------------
    """
    if folder_path[0] == "/":
        return "Please Don't include '/' at the intial of folder_path"
    if folder_path[-1] != "/":
        return "Please include '/' at the end of folder_path"
    client.put_object(Bucket=bucket_name, Key=folder_path)
    return "Success"

def s3_read_multiple_images(bucketName,key_path,max_images=' '):
    """
    Arguments:
    -------------------------------------------------------------------------------------------
    bucketName    : Type - string     | The Object's bucket_name identifier | **[REQUIRED]**  |
    key           : Type - string     | S3 folder that contains objects     | **[REQUIRED]**  |
    max_images    : Type - integer    | Number of images to be extracted    | Option          |
    -------------------------------------------------------------------------------------------
    Output        : Returns List which contains objects as array.
    """
    bucket = s3_resource.Bucket(bucketName)
    keys=[]
    for obj in bucket.objects.filter(Prefix=key_path):
        keys.append(obj.key)
    img_list = []
    for i in keys:
        if not i.endswith("/"):
            im1 = Image.open(bucket.Object(i).get()['Body'])
            img_list.append(np.array(im1))
    if max_images != ' ':
        img_list = img_list[:max_images]
    return img_list

def upload_folder_to_s3(bucketName, inputDir, s3Path,tagging=' ',storageClass='STANDARD'):
    """
    Arguments:
    ---------------------------------------------------------------------------------------------------------------------------------------------------
    bucketName    : Type - string     | The Object's bucket_name identifier         | **[REQUIRED]**  |
    inputDir      : Type - string     | Local Input directory path                  | **[REQUIRED]**  |
    s3Path        : Type - string     | S3 folder path to upload inputDir's objects | **[REQUIRED]**  | Example., "example-folder/example-subfolder/" |
    tagging       : Type - dictionary | Input Tags for the given object             | [Optional]      | Example., {"key1":"value1","key2":"value2"}
    storageClass  : Type - string     | S3 storage class of the object              | [Optional]
    ---------------------------------------------------------------------------------------------------------------------------------------------------
    Output        : Returns "Success" if upload has been done.
    """

    try:
        s3bucket = s3_resource.Bucket(bucketName)

        if s3Path[0] == "/":
            return "Please Don't include '/' at the intial of s3Path"
        if s3Path[-1] != "/":
            return "Please include '/' at the end of s3Path"

        for path, subdirs, files in os.walk(inputDir):
            for file in files:
                dest_path = path.replace(inputDir,"")
                __s3file = os.path.normpath(s3Path + '/' + dest_path + '/' + file)
                __local_file = os.path.join(path, file)
                if tagging == ' ':
                    s3bucket.upload_file(__local_file, __s3file)
                else:
                    s3bucket.upload_file(__local_file, __s3file, ExtraArgs={'StorageClass': storageClass,'Tagging': urlencode(tagging)})
        return "Success"
    except Exception as e:
        print(" ... Failed!! Quitting Upload!!")
        print(e)
        raise e


def create_bucket(BucketName, BlockPublicAcls=' ',IgnorePublicAcls=' ',BlockPublicPolicy=' ',RestrictPublicBuckets=' '):
    """
    Arguments:

    BucketName                : Type - string     | The name of bucket                                                                                              | **[REQUIRED]**
    BlockPublicAcls           : Type - string     | Block public access to buckets and objects granted through new ACLs                                             |
    IgnorePublicAcls          : Type - string     | Block public access to buckets and objects granted through any ACLs                                             |
    BlockPublicPolicy         : Type - string     | Block public access to buckets and objects granted through new public bucket or access point policies           |
    RestrictPublicBuckets     : Type - string     | Block public and cross-account access to buckets and objects through any public bucket or access point policies |

    Output                    : Returns 'Success' if bucket created successfully.

    """
    try:
        if BlockPublicAcls==' ' and IgnorePublicAcls==' ' and BlockPublicPolicy==' ' and RestrictPublicBuckets==' ' :
            client.create_bucket(Bucket=BucketName)
            client.put_public_access_block(Bucket=BucketName,PublicAccessBlockConfiguration={'BlockPublicAcls': True,'IgnorePublicAcls': True,'BlockPublicPolicy': True,'RestrictPublicBuckets': True})
        else:
            client.create_bucket(Bucket=BucketName)
            client.put_public_access_block(Bucket=BucketName,PublicAccessBlockConfiguration={'BlockPublicAcls': BlockPublicAcls,'IgnorePublicAcls': IgnorePublicAcls,'BlockPublicPolicy': BlockPublicPolicy,'RestrictPublicBuckets': RestrictPublicBuckets})
    except ClientError as e:
        logging.error(e)
        return False
    return 'Success'

def folder_path(bucket,prefix):
    """
    Arguments:
    -----------------------------------------------------------------------------------------------------------
    bucket      : Type - string | S3 Bucket name containing the folder                    | **[REQUIRED]**  |
    prefix      : Type - string | Folder name inside bucket containing sub-folders        |   [OPTIONAL]    |
    -----------------------------------------------------------------------------------------------------------
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name=bucket)
    x=[]
    for obj in bucket.objects.filter(Prefix=prefix):
        x.append(obj.key)
    y=[]
    for i in x:
        if re.search("[a-zA-Z]$",i) != None:
            y.append(i)
    return set([re.sub("/[^/]*$","/",path) for path in y])
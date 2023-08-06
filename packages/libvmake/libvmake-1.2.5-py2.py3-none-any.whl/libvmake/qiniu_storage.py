from libvmake.utils import get_gist_token, get_qiniu_config, private, get_global_config
import time
import os
import sys
from urllib.parse import urlparse
import requests
try:
    from qiniu import Auth, put_file, etag
    from qiniu import BucketManager
    from qiniu.services.cdn.manager import create_timestamp_anti_leech_url
except ModuleNotFoundError:
    os.system(f'{sys.executable} -m pip install --no-input qiniu')
    from qiniu import Auth, put_file, etag
    from qiniu import BucketManager
    from qiniu.services.cdn.manager import create_timestamp_anti_leech_url

bucket_manager = None

def init(access_key: str, secret_key: str) -> BucketManager:
    q = Auth(access_key, secret_key)
    bucket_manager = BucketManager(q)
    return bucket_manager

@private
def init_ex()->BucketManager:
    qinu_config = get_qiniu_config()
    return init(qinu_config['access_key'], qinu_config['secret_key'])

def get_bucket_manager()->BucketManager:
    global bucket_manager
    if bucket_manager is None:
        bucket_manager = init_ex()
    return bucket_manager

def state(bucket_manager: BucketManager, bucket_name, key):
    """
    Returns:
        dict: 文件信息，eg： {'fsize': 1442, 'hash': 'xxx', 'md5': 'de90e7c216e56311d6d5ef06e14b53d6', 'mimeType': 'text/plain; charset=utf-8', 'putTime': 16227471415028191, 'type': 0}
    """
    return bucket_manager.stat(bucket_name, key)[0]

def list(bucket_manager: BucketManager, bucket_name: str, prefix=None, marker=None, limit=100, delimiter=None) -> list:
    """列举文件
    Returns:
        list: 文件列表，eg： [{'key': 'rar.zip', 'hash': 'xxx', 'fsize': 4276035, 'mimeType': 'application/zip', 'putTime': 16225032506724340, 'type': 0, 'status': 0, 'md5': 'c378e96d7900fff047ec2ce62dfe91b8'}]
    """
    return bucket_manager.list(bucket_name, prefix, marker, limit, delimiter)[0]['items']


def fetch(bucket_manager: BucketManager, bucket_name: str, url: str, key: str):
    """下到url到bucket
    Returns:
        dict: 下载的文件信息， eg： {'fsize': 1442, 'hash': 'xxx', 'key': 'test.md', 'mimeType': 'text/plain; charset=utf-8', 'overwritten': True, 
'version': ''}
    """
    return bucket_manager.fetch(url, bucket_name, key)[0]


def get_timestamp_url(url):
    parsed_url = urlparse(url)
    deadline = int(time.time()) + 3600
    encrypt_key = ''
    timestamp_url = create_timestamp_anti_leech_url(f'{parsed_url.scheme}://{parsed_url.netloc}', parsed_url.path, '', encrypt_key, deadline)
    return timestamp_url


def upload(bucket_manager: BucketManager, local_file: str, bucket_name: str, key: str, expire_time=3600):
    """
    Returns:
        dict: 上传的文件信息， eg： {'hash': 'xxx', 'key': 'test.md'}
    """
    token = bucket_manager.auth.upload_token(bucket_name, key, expire_time, {})
    return put_file(token, key, local_file, version='v2')[0]


def download(bucket_manager: BucketManager, bucket_domain: str, key: str, dest_file: str, protocol='http') -> bool:
    base_url = f'{protocol}://{bucket_domain}/{key}'
    private_url = bucket_manager.auth.private_download_url(base_url, expires=3600)
    r = requests.get(private_url, allow_redirects=True)
    if r.status_code == 200:
        with open(dest_file, 'wb') as f:
            f.write(r.content)
        return True
    else:
        return False

# schema: http / https
def download_public(bucket_domain: str, key: str, dest_file: str, schema: str = 'http'):
    url = f'{schema}://{bucket_domain}/{key}'
    _url = get_timestamp_url(url)
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        with open(dest_file, 'wb') as f:
            f.write(r.content)
        return True
    else:
        return False


def delete(bucket_manager: BucketManager, bucket_name: str, key: str) -> bool:
    return bucket_manager.delete(bucket_name, key)[1].ok()

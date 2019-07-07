from __future__ import absolute_import

from flask import current_app
from google.cloud import storage
import six


def _get_storage_client():
    #print(current_app.config['PROJECT_ID'])
    return storage.Client(
        project=current_app.config['PROJECT_ID'])


def upload_file(file_stream, filename, content_type):
    print ('reached in upload_file')
    #client = _get_storage_client()
    client = storage.Client(current_app.config['PROJECT_ID'])
    #print (client)
    print ('client name printed above')
    print (current_app.config['CLOUD_STORAGE_BUCKET'])
    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    print (bucket)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    print('file uploaded successfully')
    print(url)

    for entry in blob.acl:
        print('{}: {}'.format(entry['role'], entry['entity']))

    bucket.default_object_acl.user('allUsers').revoke_read()
    blob.acl.group('allUsers').revoke_read()
    blob.acl.user("abc@pqr.com").grant_read()
    blob.acl.user("asdf@qwe.com").grant_owner()
    blob.acl.save()
    print('after update of acl')
    for entry in blob.acl:
        print('{}: {}'.format(entry['role'], entry['entity']))
    return url
# [END upload_file]
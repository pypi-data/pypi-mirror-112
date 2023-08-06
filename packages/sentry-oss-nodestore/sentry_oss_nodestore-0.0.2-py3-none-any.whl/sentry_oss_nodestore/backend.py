"""
sentry_oss_nodestore.backend
~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2021 by yuanxiao
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import datetime
import math
from base64 import urlsafe_b64encode
from time import sleep
from uuid import uuid4
import zlib
import os
import oss2

from sentry.nodestore.base import NodeStorage


def retry(attempts, func, *args, **kwargs):
    for _ in range(attempts):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            sleep(0.1)
            raise
    raise


class OSSNodeStorage(NodeStorage):

    def __init__(self, bucket_name=None, endpoint=None, oss_access_key_id=None, oss_secret_access_key=None, max_retries=3):
        # self.max_retries = max_retries
        # self.bucket_name = bucket_name
        # self.client = boto3.client(
        #     's3', endpoint_url=endpoint, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.prefix = "nodedatas/"
        self.max_retries = max_retries
        self.bucket_name = bucket_name
        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录RAM控制台创建RAM账号。
        auth = oss2.Auth(oss_access_key_id, oss_secret_access_key)
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        # bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)

    def delete(self, id):
        """
        >>> nodestore.delete('key1')
        """
        # self.client.delete_object(Bucket=self.bucket_name, Key=id)
        key = id
        try:
            self.bucket.delete_object(os.path.join(self.prefix, key))
        except Exception as e:
            print(f"{datetime.datetime.now()} oss delete error ----", e)

    def delete_multi(self, id_list):
        """
        Delete multiple nodes.
        Note: This is not guaranteed to be atomic and may result in a partial
        delete.
        >>> delete_multi(['key1', 'key2'])
        """
        # self.client.delete_objects(Bucket=self.bucket_name, Delete={
        #     'Objects': [{'Key': id} for id in id_list]
        # })
        try:
            block_size = 1000  # oss每次最多删除1000个
            loop_count = math.ceil(len(id_list)/block_size)
            for index in range(loop_count):
                id_block = id_list[index*block_size, (index+1)*block_size]
                real_id_block = [os.path.join(self.prefix, key)
                                 for key in id_block]
                try:
                    self.bucket.delete_objects(real_id_block)
                except Exception as e:
                    print(
                        f"{datetime.datetime.now()} oss delete batch error ----", e)
        except Exception as e1:
            print(f"{datetime.datetime.now()} oss delete_multi error ----", e)

    def _get_bytes(self, id):
        """
        >>> nodestore._get_bytes('key1')
        b'{"message": "hello world"}'
        """
        # result = retry(self.max_retries, self.client.get_object,
        #                Bucket=self.bucket_name, Key=id)
        # return zlib.decompress(result['Body'].read())
        # result = bucket.get_object(key)
        # content_got = b''
        # for chunk in result:
        #     content_got += chunk
        # assert result.client_crc == result.server_crc
        result = retry(self.max_retries, self.bucket.get_object,
                       key=os.path.join(self.prefix, id), headers=None)
        return zlib.decompress(result.read())

    def _set_bytes(self, id, data, ttl=None):
        """
        >>> nodestore.set('key1', b"{'foo': 'bar'}")
        """
        # retry(self.max_retries, self.client.put_object, Body=zlib.compress(data), Bucket=self.bucket_name, Key=id)
        retry(self.max_retries, self.bucket.put_object,
              data=zlib.compress(data),  key=os.path.join(self.prefix, id), headers=None)

    def generate_id(self):
        return urlsafe_b64encode(uuid4().bytes)

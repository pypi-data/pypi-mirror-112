#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2020/8/21'
# qq | WX:2456056533

佛祖保佑  永无bug!

"""

import random
import string
import aiohttp
import os
import time
import asyncio
import numpy as np
import cv2
from aiohttp import ClientTimeout
from aiohttp.client_exceptions import ServerTimeoutError

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from clife_svc.errors.error_code import FileException, ParameterException, UploadImgException, TimeoutException
from clife_svc.libs.log import klogger


class ClientRequest:

    _COS_CLIENT = ''
    HTTP_TIMEOUT = None
    COS_REGION = None
    COS_SECRET_ID = None
    COS_SECRET_KEY = None
    COS_BUCKET = None
    COS_DIR = None
    COS_BUCKET_HOST = None
    # 请求超时时间
    __http_sess_timeout = None

    def __init__(self, conf_item: dict):
        self.HTTP_TIMEOUT = int(conf_item.get('http.timeout', 5))
        self.COS_REGION = conf_item.get('cos.region', '')
        self.COS_SECRET_ID = conf_item.get('cos.secret.id', '')
        self.COS_SECRET_KEY = conf_item.get('cos.secret.key', '')
        self.COS_BUCKET = conf_item.get('cos.bucket', '')
        self.COS_DIR = conf_item.get('cos.dir', 'ai')
        self.COS_BUCKET_HOST = conf_item.get('cos.bucket.host', 'cos.clife.net')
        self.__http_sess_timeout = ClientTimeout(total=self.HTTP_TIMEOUT)

    async def _create_txy_client(self):
        '''
        腾讯云上传client对象
        '''
        try:
            config = CosConfig(Region=self.COS_REGION, Secret_id=self.COS_SECRET_ID,
                               Secret_key=self.COS_SECRET_KEY,
                               Token=None)
            client = CosS3Client(config)
            return client
        except Exception as e:
            raise UploadImgException(error_code=9951, msg='_create_txy_client error:{}'.format(e))

    @staticmethod
    async def _request_get(session, url, params, resp_type):
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                if resp_type == 'json':
                    return await resp.json()
                elif resp_type == 'text':
                    return await resp.text()
                else:
                    return await resp.read()
            else:
                klogger.error(
                    'error of ClientRequest._request_get,resp.status:{},resp.text:{}'.format(resp.status,
                                                                                             await resp.text()))

    @staticmethod
    async def _request_post(session, url, data, resp_type):
        async with session.post(url, data=data) as resp:
            if resp.status == 200:
                if resp_type == 'json':
                    return await resp.json()
                elif resp_type == 'text':
                    return await resp.text()
                else:
                    return await resp.read()
            else:
                klogger.error(
                    'error of ClientRequest._request_post,resp.status:{},resp.text:{}'.format(resp.status,
                                                                                              await resp.text()))

    async def _async_request(self, method, url, params=None, data=None, headers=None, cookies=None, resp_type='json'):
        '''

        :param method:
        :param url:
        :param params:
        :param data:
        :param headers:
        :param cookies:
        :param resp_type: json | text | byte
        :return:
        '''
        try:
            async with aiohttp.ClientSession(headers=headers, cookies=cookies, timeout=self.__http_sess_timeout) as sess:
                if method == 'GET':
                    return await self._request_get(sess, url, params, resp_type=resp_type)
                elif method == 'POST':
                    return await self._request_post(sess, url, data, resp_type=resp_type)
                else:
                    raise ParameterException(error_code=9982, msg='async_request method must in [GET,POST]')

        except ServerTimeoutError as aiohttp_time_out:
            raise TimeoutException(error_code=9940, msg='aiohttp_time_out:{},url:{}'.format(aiohttp_time_out, url))

    async def download_img(self, img_url, retry=2):
        '''
        图片下载
        :param img_url:
        :param retry:
        :return: img_byte | str
        '''
        while retry > 0:
            retry -= 1
            if 'http' in img_url:
                klogger.info('start download img:{}'.format(img_url))
                start = time.time()
                resp_byte = await self._async_request('GET', img_url, resp_type='byte')
                if resp_byte:
                    klogger.info('download img cost:{}s'.format(round(time.time() - start, 2)))
                    klogger.info('success download img')
                    return resp_byte
            else:
                # 本地文件路径格式直接返回
                klogger.info('img path:{}'.format(img_url))
                return ''

    async def get_img_np(self, img_url):
        '''
        图片下载
        :param img_url:
        :return: img np.asarray
        '''
        if img_url:
            resp = await self.download_img(img_url)
            if resp:
                image_array = np.frombuffer(resp, dtype=np.uint8)
                image_np = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                return image_np
            else:
                image_np = cv2.imread(img_url)
                if image_np is None:
                    raise FileException(error_code=9971, msg='img_file not exist')
                return image_np

    @staticmethod
    async def _rename_file(file: str):
        '''文件更名'''
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        salt += str(int(time.time()))
        return salt + '_' + file

    async def upload_img(self, img_path: str, retry=2):
        '''
        上传图片
        :param img_path 待上传的图片路径
        :param retry 失败重试次数
        '''

        while retry > 0:
            retry -= 1
            start = time.time()
            if not self._COS_CLIENT:
                self._COS_CLIENT = await self._create_txy_client()

            if not os.path.isfile(img_path):
                raise ParameterException(error_code=9987, msg='img not exist:'.format(img_path))

            file_name = os.path.split(img_path)[1]
            file_name = await self._rename_file(file_name)

            cloud_path = '/' + self.COS_DIR + '/' + file_name

            client_resp = self._COS_CLIENT.upload_file(
                Bucket=self.COS_BUCKET,
                LocalFilePath=img_path,
                Key=cloud_path,
                PartSize=10,
                MAXThread=10
            )
            '''
            client_resp:dict
            {'Content-Length': '0', 'Connection': 'keep-alive', 'Date': 'Thu, 27 Aug 2020 07:19:34 GMT', 
            'ETag': '"d2110b267778c3fd81854ff0283c01d4"', 'Server': 'tencent-cos', 'x-cos-hash-crc64ecma': '3062988045414607577', 
            'x-cos-request-id': 'NWY0NzVlODFfNThhYTk0MGFfNDQ1OV8zOTFkODUz'}

            '''
            if client_resp and isinstance(client_resp, dict):
                etag = str(client_resp.get('ETag', ''))
                if etag:
                    img_url = 'http://' + self.COS_BUCKET_HOST + cloud_path
                    klogger.info('upload img cost:{}s'.format(round(time.time() - start, 2)))
                    klogger.info('upload img success:{}'.format(img_url))
                    return img_url
            else:
                klogger.warning('error upload img,retry:{}'.format(retry))
                continue

        raise UploadImgException(error_code=9952, msg='client.put_object error')

    @staticmethod
    def case_get_img_np(img_url):
        '''测试从腾讯云下载图片'''
        loop = asyncio.get_event_loop()
        image_np = loop.run_until_complete(ClientRequest.get_img_np(img_url))
        print(image_np)

    @staticmethod
    def case_upload_img(img_url):
        loop = asyncio.get_event_loop()
        a = loop.run_until_complete(ClientRequest.upload_img(img_url))
        print(a)


if __name__ == '__main__':
    ClientRequest.case_get_img_np(img_url='http://cos.clife.net/10101/3cb34041583e4adebe241e8612d67eb2.png')
    # ClientRequest.case_upload_img(img_url=r'F:\star\hand.jpg')

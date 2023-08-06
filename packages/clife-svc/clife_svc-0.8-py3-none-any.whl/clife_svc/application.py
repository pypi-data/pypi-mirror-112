#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'andy.hu'
__mtime__ = '2021/07/09'

"""
import time
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Set,
    Union,
)

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import (BaseHTTPMiddleware, RequestResponseEndpoint)
from starlette.requests import Request as HttpRequest
from starlette.responses import Response as HttpResponse

from clife_svc.disconf import Disconf
from clife_svc.errors.error_code import ApiException, api_exception_handler
from clife_svc.libs.http_request import ClientRequest
from clife_svc.libs.log import init_conf_log
from clife_svc.libs.log import init_svc_log
from clife_svc.libs.log import klogger


class App(object):
    '''
    http接口服务上下文对象，单实例对象
    '''
    __instance = None
    __conf_item = None
    __fast_api = FastAPI(title='ai-service', default_response_class=ORJSONResponse)
    __ai_router = APIRouter()
    __ClientRequest = None
    __app_name = None
    __log_path = None

    def __new__(cls, app_name: str, log_root_path: str, *conf: str):
        '''
        构造函数
        :param app_name 项目名称
        :param log_root_path 项目输出的日志根路径
        :param conf: 配置文件名称列表
        '''
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__log_path = log_root_path + '/' + app_name + '/'
            init_conf_log(cls.__log_path)
            cls.__conf_item = Disconf('clife-ai', '0.0.1-SNAPSHOT', conf).get_config_dict()
            cls.__ClientRequest = ClientRequest(cls.__conf_item)
            cls.__app_name = app_name
            init_svc_log(cls.__log_path, log_level='DEBUG')
        return cls.__instance

    def init_api(self) ->FastAPI:
        '''
        在App中初始化服务接口
        :return: FastAPI，作为服务器运行入口对象
        '''
        self.__fast_api.add_exception_handler(ApiException, api_exception_handler)
        init_middlewares(self.__fast_api)
        self.__ai_router.add_api_route('/time', index, methods=['GET'])
        self.__fast_api.include_router(self.__ai_router)
        self.__fast_api.add_exception_handler(Exception, app_exception)
        return self.__fast_api

    def get_conf(self, key: str):
        '''
        获取配置数据
        :param key:
        :return:
        '''
        try:
            return self.__conf_item[key]
        except KeyError:
            klogger.warning('config key not exist:{}'.format(key))
            return ''

    def get_all_conf(self) ->dict:
        '''
        获取所有配置数据
        :return:
        '''
        return self.__conf_item

    def add_api(self, path: str, endpoint: Callable[..., Any], methods: Optional[Union[Set[str], List[str]]] = None):
        '''
        增加服务接口，此函数需要在init_api前调用
        :param path:接口访问路径
        :param endpoint:接口实现函数
        :param methods:接口访问方式，如GET、POST等
        :return:
        '''
        self.__ai_router.add_api_route(path, endpoint, methods=methods)

    async def download_img(self, img_url, retry=2):
        '''
        下载图片
        :param img_url:图片地址
        :param retry:失败重试次数
        :return:图片数据字节数组
        '''
        return await self.__ClientRequest.download_img(img_url, retry)

    async def get_img_np(self, img_url):
        '''
        下载图片
        :param img_url:图片地址
        :return:图片数据np数组
        '''
        return await self.__ClientRequest.get_img_np(img_url)

    async def upload_img(self, img_path: str, retry=2):
        '''

        :param img_path:
        :param retry:
        :return:
        '''
        return await self.__ClientRequest.upload_img(img_path, retry)


class Interceptor(BaseHTTPMiddleware):
    '''

    '''
    async def dispatch(self, request: HttpRequest, call_next: RequestResponseEndpoint) -> HttpResponse:
        klogger.info('Request url:{}'.format(request.url))
        klogger.info('Request query_params:{}'.format(request.query_params))
        start = time.time()
        response = await call_next(request)
        cost_time = time.time() - start
        klogger.info('Request cost:{}s'.format(round(cost_time, 2)))
        return response


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(Interceptor)


async def index(q: Optional[str] = None):
    '''k8s 探针 http监控服务请求地址'''
    if q:
        return {'error_code': 0, 'msg': 'success',
                'data': {'time': time.strftime('%Y-%m-%d-%H-%M', time.localtime()), 'q': q}}

    return {'error_code': 0, 'msg': 'success', 'data': {'time': time.strftime('%Y-%m-%d-%H-%M', time.localtime())}}


async def app_exception(request: Request, exc: Exception):
    '''拦截所有未知 非HTTPException 异常'''
    klogger.info('Request url:{}'.format(request.url))
    klogger.info('Request path_params:{}'.format(request.path_params))
    klogger.info('Request query_params:{}'.format(request.query_params))
    klogger.info('Request exception:{}'.format(exc))

    return JSONResponse({
        "error_code": 99999,
        "msg": 'sorry for error:{}'.format(exc),
        "data": {},
    }, status_code=500)


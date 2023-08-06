#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'andy.hu'
__mtime__ = '2021/07/09'

"""
from clife_svc.libs.log import klogger

import requests
import os
import sys

_ENVIRONMENT = int(os.environ.get("ENVIRONMENT", 0))

if _ENVIRONMENT == 0:
    # 开发环境
    # disconf_url = 'http://disconf.clife.net:8099/disconf-web/api'
    # 采用IP配置,不使用域名原因：1window无权修改hosts,2发布预发布环境需要联系运维添加ip域名映射
    disconf_url = 'http://10.6.14.85:8099/disconf-web/api'
    env_name = 'rd'  # 环境,只能是一个

elif _ENVIRONMENT == 1:
    # 预发布环境
    disconf_url = 'http://119.29.116.47/disconf-web/api'
    env_name = 'itest'  # 环境,只能是一个

elif _ENVIRONMENT == 2:
    # 生产环境
    disconf_url = 'http://10.186.39.90:8099/disconf-web/api'
    env_name = 'res'  # 环境,只能是一个

else:
    # 开发环境
    disconf_url = 'http://10.6.14.85:8099/disconf-web/api'
    env_name = 'rd'  # 环境,只能是一个

#_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
_ROOT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
klogger.info('root_path:{}'.format(_ROOT_DIR))

disconf_path = os.path.join(_ROOT_DIR, 'local.properties')  # disconf下载配置文件到根路径


class Disconf:

    '''
    从 disconf 下载配置文件
    '''

    def __init__(self, apps, version, keys: tuple):
        ''' 构造函数
        :param apps: disconf配置app，多个使用逗号分隔
        :param version: 配置版本号
        :param keys: 配置文件名，缺省时只加载ai-commons.properties,tf-serving.properties
        '''

        klogger.info('ENVIRONMENT:{}'.format(_ENVIRONMENT))
        klogger.info('disconf_url:{}'.format(disconf_url))
        klogger.info('env_name:{}'.format(env_name))

        self.sess = requests.session()
        self.version = version
        self.apps = apps
        # 默认的配置文件名称
        self.config = 'ai-commons.properties,tf-serving.properties'
        for var in list(keys):
            self.config = self.config + ',' + var

    @staticmethod
    def disconf2dict(disconf_path) -> dict:
        '''
        读取本地disconf文件转dict
        :param disconf_path 本地配置文件路径
        '''

        with open(disconf_path, 'r') as f:
            lines = f.readlines()

        disconf_item = {}
        for line in lines:
            if line:
                line = line.replace('\n', '')
                kv_line = line.split('=', 1)
                if len(kv_line) == 2:
                    k = kv_line[0]
                    v = kv_line[1]
                    if k:
                        disconf_item[k] = v
        return disconf_item

    @staticmethod
    def save_item(item, path):
        '''
        保存配置数据字典至本地文件
        :param item: 配置数据字典
        :param path: 存储文件路径
        :return:
        '''

        with open(path, 'w', encoding='utf-8') as f:
            for k in item:
                f.write(k + '=' + item[k] + '\n')

        klogger.info('save disconf path:{}'.format(path))

    @staticmethod
    def __format_value(value) -> dict:
        # 格式化配置文件内容value
        value = value.replace('↵', '\n')
        value = value.split('\n')
        fields = [v for v in value if '=' in v and not v.startswith('#')]
        item_value = {}
        for field in fields:
            f = field.split('=', 1)
            if len(f) == 2:
                k = f[0]
                v = f[1]  # v值可为空
                if k:
                    k = ''.join(k)  # 去除空格
                    if v: v = ''.join(v)
                    item_value[k] = v
        return item_value

    def config_file(self, app, version, env, key) -> dict:
        '''
        从配置中心获取配置文件
        :param app: disconf配置app
        :param version: disconf配置版本
        :param env: disconf配置环境
        :param key: disconf配置文件的key（即配置文件名称）
        :return: 配置数据字典
        '''

        url = disconf_url + '/config/file'
        params = {
            'app': app,
            'version': version,
            'env': env,
            'key': key
        }
        try:
            resp = self.sess.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                try:
                    return self.__format_value(resp.text)
                except Exception as e:
                    klogger.error('error format_value：{}'.format(e))
                    raise e
            else:
                klogger.error('get disconf error,status_code:{},resp.text:{}'.format(resp.status_code, resp.text))
        except Exception as e:
            klogger.error('get disconf error:{}'.format(e))
            raise e

    def get_files(self, app_names: list, version: str, env_name: str, disconf_conf_name: list, local_path: str) -> dict:
        '''
        批量获取disconf配置文件内容并保存至本地
        :param app_names: disconf配置app名称
        :param version: disconf配置版本
        :param env_name: disconf配置环境
        :param disconf_conf_name: 配置文件名称
        :param local_path: 配置数据字典本地存储路径
        :return: 配置数据字典
        '''

        config_items = {}
        for app_name in app_names:
            for conf_key in disconf_conf_name:
                item = self.config_file(app_name, version, env_name, conf_key)
                if item:
                    config_items.update(item)

        self.save_item(config_items, local_path)
        klogger.info('download disconf succcess')
        return config_items

    def get_config_dict(self) ->dict:
        '''
        获取当前项目下的所有配置数据字典
        :return:
        '''

        def split2list(v):
            v = v.replace('，', ',')
            return [a for a in v.split(',') if a]

        try:
            if not isinstance(self.apps, list):
                app_names = split2list(self.apps)

            if not isinstance(self.config, list):
                disconf_conf_name = split2list(self.config)

            klogger.info('start download disconf file')
            disconf_item = self.get_files(app_names, self.version, env_name, disconf_conf_name, disconf_path)

            self.sess.close()
            if not disconf_item:
                klogger.info('error download disconf from disconf_url:{}'.format(disconf_url))
                klogger.info('error disconf_item:{}'.format(disconf_item))
                klogger.info('start load local disconf')
                disconf_item = Disconf.disconf2dict(disconf_path)
            for item in disconf_item:
                klogger.info('disconf_item:{}'.format(item + '=' + disconf_item[item]))

            return disconf_item
        except Exception as e:
            klogger.error('error download disconf:{}'.format(e))
            raise e

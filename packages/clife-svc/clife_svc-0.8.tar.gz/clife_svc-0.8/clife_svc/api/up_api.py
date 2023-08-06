#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2020/8/7'
# qq | WX:2456056533

佛祖保佑  永无bug!

"""
import os
import asyncio
import re
from typing import List

import aiofiles
from fastapi import APIRouter, UploadFile, File

from clife_svc.app import APP_DIR
from clife_svc.libs.log import klogger

up_router = APIRouter()


async def _save_file(dir, file, mode='wb'):
    file_name = file.filename
    # 文件写入安全检测
    file_name = re.sub(r'[?\\*|“<>:./]', '.', file_name)
    file_path = os.path.join(dir, file_name)
    klogger.info('upload {}'.format(file_name))
    async with aiofiles.open(file_path, mode) as f:
        while True:
            chunck = await file.read(64 * 1024 ** 2)  # 1024 ** 2 == 1MB
            if chunck:
                await f.write(chunck)
            else:
                break


@up_router.post('/upload')
async def upload_model_files(files: List[UploadFile] = File(...)):
    '''文件上传接口'''
    tasks = []
    for file in files:
        task = asyncio.ensure_future(_save_file(APP_DIR, file))
        tasks.append(task)
        # await _save_file(file)
    await asyncio.wait(tasks)
    return {'error_code': 0, 'msg': 'upfile success', 'data': {}}

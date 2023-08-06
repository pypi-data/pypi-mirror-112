import asyncio
from typing import Optional

import uvicorn

from build.lib.clife_svc.errors.error_code import ParameterException
from clife_svc.application import App

app = App('clife_svc_test', '/www/logs', 'cv-kube.properties')


async def detect(client_params: Optional[dict] = None) -> str:
    res = {'code': 0, 'msg': 'success'}
    image_np = await app.get_img_np('http://cos.clife.net/10101/3cb34041583e4adebe241e8612d67eb2.png')
    print(image_np)
    await asyncio.sleep(3)
    # raise ParameterException()
    return res

if __name__ == '__main__':
    app.add_api('/detect', detect, methods=['POST'])
    uvicorn.run(app.init_api(), host='0.0.0.0', port=30000, debug=True)

from hacktcha.model import HacktchaModel
from hacktcha.conf import cfg
import os
import aiofiles
import tempfile
from fastai.vision.all import *
import aiohttp
from sanic import response

import logging

logger = logging.getLogger(__name__)

class HacktchaServer(object):
    def __init__(self) -> None:
        super().__init__()
        self._tmp_dir = tempfile.mkdtemp()

        self.hacktcha = None

    async def init(self, *args):
        logging.basicConfig(level=logging.INFO)
        logger.info("init %s", self.__class__.__name__)

        model_name = cfg.remote_model.split("/")[-1]
        model = os.path.join(cfg.cache_dir, model_name)
        model = os.path.expanduser(model)

        if not os.path.exists(model):
            await self._download_model(cfg.remote_model, model)

        vocab = "0123456789"
        nletters = 4

        self.hacktcha = HacktchaModel.from_model(model, vocab, nletters)

    async def ocr(self, request):
        filename = request.files["file"][0].name
        tmp_file = os.path.join(self._tmp_dir, request.files["file"][0].name)
        async with aiofiles.open(tmp_file, 'wb') as f:
            await f.write(request.files["file"][0].body)

        try:
            text = self.hacktcha.predict(tmp_file)
            logger.info("%s predicts %s", filename, text)
            return response.text(text)
        except Exception as e:
            logger.exception(e)
            return response.text("",status=500)

    async def _download_model(self, url:str, model:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    f = await aiofiles.open(model, mode="wb")
                    await f.write(await response.read())
                    await f.close()

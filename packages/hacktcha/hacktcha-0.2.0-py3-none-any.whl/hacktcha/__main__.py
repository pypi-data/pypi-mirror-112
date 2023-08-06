import sys

from sanic.app import Sanic

from hacktcha.model import HacktchaModel
# to allow unpickle the model. If the model is trained in a notebook which content is same as `hacktcha.py`, then the model is pickled under namespace `__main__`, then we'll have to unpickle it under same level
from hacktcha.model import LabellingWrapper # noqa
from hacktcha.model import HacktchaLoss # noqa
from hacktcha.model import MyRandomSplitter # noqa

import fire
import os

from hacktcha.generator.eastmoney import EastmoneyCaptchaImage
from hacktcha.server import HacktchaServer


def train(domain:str, arch: str, save_to:str, pretrain:str=None, fine_tune:str=None):
    """train the model and save the model to save_to

    the model will be save as save_to/hacktcha-arch-n_letters-len(vocab)-{accuracy}.pth
    if pretrain is provided, then the training process would be:
        1. train the model with pretrain images and on top of this model
        2. train the model with fine_tune images

    otherwise, there're would be one-shot training.

    Args:
        domain (str): the name of domain that hacktcha supported
        arch (str): for example, resnet18, vgg16_bn
        pretrain (str, optional): path of images used for pre-train. Defaults to None.
        fine_tune (str, optional): path of images used for fine-tune. Defaults to None.
    """
    if domain == "eastmoney":
        vocab = "0123456789"
        nletters = 4
    else:
        print(f"{domain} not supported yet")
        sys.exit(-1)

    images = (pretrain, fine_tune)
    hacktcha = HacktchaModel(vocab, nletters, arch, images)
    hacktcha.train(save_to)

def generate(domain:str, epoch:int=1, total:int=1e9, save_to:str="./sample"):
    """generate fake captcha images

    Args:
        domain (str): choose generator according to domain
        epoch (int, optional): how many epoch (iterate through all composition). Defaults to 1.
        total (int, optional): if specified, then generate files up to total
    """
    save_to = os.path.expanduser(save_to)
    if not os.path.isabs(save_to):
        save_to = os.path.join(os.getcwd(), save_to)

    if domain == "eastmoney":
        captcha = EastmoneyCaptchaImage(save_to)
        captcha.run(epoch, total)

def serve(port:int=4225):
    server = HacktchaServer()
    app = Sanic("Hacktcha server")
    app.add_route(server.ocr, "/ocr", methods=["POST"])

    app.register_listener(server.init, "before_server_start")
    app.run(
        host="0.0.0.0",
        port=port,
        register_sys_signals = True)


fire.Fire({
    "serve": serve,
    "train": train,
    "gen": generate
})

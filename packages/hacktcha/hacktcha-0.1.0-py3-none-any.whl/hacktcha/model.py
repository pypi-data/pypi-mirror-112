from math import sqrt
from pathlib import Path
from typing import List, Tuple, Callable
import numpy as np
from fastai.vision.all import *
from torch import nn
import tempfile
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MyRandomSplitter:
    def __init__(self, valid_pct:float=0.2, seed:int=None):
        self.valid_pct = valid_pct
        self.seed = seed

    def __call__(self, o):
        if self.seed is not None: torch.manual_seed(self.seed)
        rand_idx = L(list(torch.randperm(len(o)).numpy()))
        cut = int(self.valid_pct * len(o))
        return rand_idx[cut:],rand_idx[:cut]
    
class HacktchaLoss(BaseLoss):
    def __init__(self, nclasses:int, nletters:int, axis=-1, **kwargs):
        self.func = None
        self._nclasses = nclasses
        self._nletters = nletters

    def __call__(self, inp, *y):
        preds = inp.split(self._nclasses, dim = 1)
        
        _loss = nn.CrossEntropyLoss()(preds[0], y[0])
        for i in range(self._nletters):
            _loss += nn.CrossEntropyLoss()(preds[i], y[i])
    
        return _loss

    def decodes(self, x):
        preds = x.split(self._nclasses, dim = 1)
        return [preds[i].argmax(dim=1) for i in range(self._nletters)]

class LabellingWrapper():
    def __init__(self, pos: int):
        self._pos = pos
        
    def __call__(self, filepath: Path):
        """get label from file name

        It's assumed that the filename, or parts of it contains the label. The filename should be in either "1234.jpg" or "1234_xxx.jpg" format. The latter form is used when there's multiple image belongs to same label

        Args:
            filepath (Path): [description]

        Returns:
            [type]: [description]
        """
        label = filepath.parts[-1].split(".")[0]
    
        if label.find("_"):
            label = label.split("_")[0]
            
        return label[self._pos]

class HacktchaModel:
    def __init__(self, vocab:str, nletters:int, arch: Callable=None, image_path:Tuple[str, str] = None):
        self._nletters = nletters
        self._vocab = vocab
        self._bs = 64
        self._nclasses = len(self._vocab)
        self._arch = arch
        self._lr = 3e-3
        
        if image_path is not None:
            if len(image_path) == 1:
                self._fine_tune_images = image_path[0]
                self._pretrain_images = None
            else:
                self._pretrain_images = image_path[0]
                self._fine_tune_images = image_path[1]

        self._dls = None
        self._learner:Learner = None

        blocks = (ImageBlock(cls=PILImageBW), *([CategoryBlock] * self._nletters))

        self._datasets = DataBlock(
            blocks=blocks, 
            n_inp=1, 
            get_items=get_image_files, 
            get_y= [LabellingWrapper(i) for i in range(self._nletters)],
            batch_tfms=[*aug_transforms(do_flip=False, size=108), Normalize()],
        splitter = MyRandomSplitter(seed=42))


    def create_learner(self, image_path:str, has_pretrain:bool=False):
        """create a cnn_learner. 
        
        Args:
            has_pretrain (bool): if True then loads pretrained model
        """
        if has_pretrain: # this is fine tune stage
            nfiles = len(os.listdir(image_path))
            self._bs = min(self._bs, int((sqrt(nfiles))))

        self._dls = self._datasets.dataloaders(source=image_path, bs=self._bs)

        self._learner = cnn_learner(
            self._dls, 
            self._arch, 
            n_out = (self._nclasses * self._nletters), 
            loss_func=HacktchaLoss(self._nclasses, self._nletters), 
            lr=self._lr,
            metrics=self.accuracy,
            cbs = [SaveModelCallback, EarlyStoppingCallback(patience=3)])

        if has_pretrain:
            self._learner.load("model")

    def accuracy(self, preds, *y):
        """calcualte accuracy of the prediction

        Args:
            preds ([type]): [description]
        """
        preds = preds.split(self._nclasses, dim=1)

        r0 = (preds[0].argmax(dim=1) == y[0]).float().mean()
        for i in range(1, self._nletters):
            r0 += (preds[i].argmax(dim=1) == y[i]).float().mean()

        return r0/self._nletters

    def train(self, save_to: str, epoch: int=100):
        # do the training on general captcha images dataset
        if self._pretrain_images is not None:
            logger.info("pretrain with images at %s", self._pretrain_images)
            self.create_learner(self._pretrain_images)        
            lr, _ = self._learner.lr_find()

            self._learner.fine_tune(epoch, lr)

            self._learner.save("tmp", pickle_protocol = 4)

        # fine_tune on specific images found on specific website
        logger.info("fine tune with images at %s", self._fine_tune_images)
        self.create_learner(self._fine_tune_images, self._pretrain_images is not None)
        lr, _ = self._learner.lr_find()
        
        self._learner.fine_tune(epoch, lr)
        loss, acc = self._learner.validate(ds_idx=1)

        model_file = os.path.join(save_to, f"hacktcha-{self._arch.__name__}-{self._nletters}-{self._nclasses}-{acc:.2f}.pkl")
        self._learner.export(model_file)
    
    @staticmethod
    def from_model(model: str, vocab:str, nletters: int):
        hacktcha = HacktchaModel(vocab, nletters)
        hacktcha._learner = load_learner(model)
        
        return hacktcha
    
    def predict(self, filepath:str):
        letters, _, _ = self._learner.predict(filepath)
        
        return ''.join(letters)
    
    def test(self, test_images_dir:str):
        missed = 0
        test_images = Path(test_images_dir).ls()
        for test_image in test_images:
            letters = self.predict(str(test_image))
            
            if letters != test_image.stem:
                missed  += 1
                print(f"pred {letters}, actual: {test_image.stem}")
                
        return missed / len(test_images)

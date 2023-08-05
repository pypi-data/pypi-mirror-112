import numpy as np
import onnxruntime as rt
from PIL import Image

from .keys import alphabetChinese as alphabet
from .util import StrLabelConverter, ResizeNormalize

converter = StrLabelConverter(''.join(alphabet))


def softmax(x):
    x_row_max = x.max(axis=-1)
    x_row_max = x_row_max.reshape(list(x.shape)[:-1] + [1])
    x = x - x_row_max
    x_exp = np.exp(x)
    x_exp_row_sum = x_exp.sum(axis=-1).reshape(list(x.shape)[:-1] + [1])
    softmax_ = x_exp / x_exp_row_sum
    return softmax_


class CRNNHandle:
    def __init__(self, model_path):
        self.sess = rt.InferenceSession(model_path)

    def predict(self, image):
        """
        预测
        """
        scale = image.size[1] * 1.0 / 32
        w = image.size[0] / scale
        w = int(w)
        transformer = ResizeNormalize((w, 32))
        image = transformer(image)
        image = image.transpose(2, 0, 1)
        transformed_image = np.expand_dims(image, axis=0)
        preds = self.sess.run(["out"], {"input": transformed_image.astype(np.float32)})
        preds = preds[0]
        length = preds.shape[0]
        preds = preds.reshape(length, -1)
        preds = np.argmax(preds, axis=1)
        preds = preds.reshape(-1)
        sim_pred = converter.decode(preds, length, raw=False)
        return sim_pred

    def predict_rbg(self, im):
        """
        预测
        """
        scale = im.size[1] * 1.0 / 32
        w = im.size[0] / scale
        w = int(w)
        img = im.resize((w, 32), Image.BILINEAR)
        img = np.array(img, dtype=np.float32)
        img -= 127.5
        img /= 127.5
        image = img.transpose(2, 0, 1)
        transformed_image = np.expand_dims(image, axis=0)
        preds = self.sess.run(["out"], {"input": transformed_image.astype(np.float32)})
        preds = preds[0]
        length = preds.shape[0]
        preds = preds.reshape(length, -1)
        preds = np.argmax(preds, axis=1)
        preds = preds.reshape(-1)
        sim_pred = converter.decode(preds, length, raw=False)
        return sim_pred

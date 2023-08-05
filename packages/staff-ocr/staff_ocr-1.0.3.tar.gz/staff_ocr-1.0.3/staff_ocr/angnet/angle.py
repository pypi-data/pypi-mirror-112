import numpy as np
import onnxruntime as rt
from PIL import Image


class AngleNetHandle:
    def __init__(self, model_path, size_h=32, size_w=192):

        self.sess = rt.InferenceSession(model_path)
        self.size_h = size_h
        self.size_w = size_w

    def predict_rbg(self, im_):
        """
        预测
        """
        scale = im_.size[1] * 1.0 / self.size_h
        w = im_.size[0] / scale
        w = int(w)
        img = im_.resize((w, self.size_h), Image.BILINEAR)

        if w < self.size_w:
            img_new = Image.new('RGB', (self.size_w, self.size_h), 255)
            img_new.paste(img, (0, 0, w, self.size_h))
        else:
            img_new = img.crop((0, 0, self.size_w, self.size_h))

        img = np.array(img_new, dtype=np.float32)

        img -= 127.5
        img /= 127.5
        image = img.transpose((2, 0, 1))
        transformed_image = np.expand_dims(image, axis=0)

        preds = self.sess.run(["out"], {"input": transformed_image.astype(np.float32)})

        pred = np.argmax(preds[0])

        return pred

    def predict_rbgs(self, imgs_):
        nlen = len(imgs_)
        res_sum = sum([self.predict_rbg(im_) for im_ in imgs_])
        return res_sum < nlen // 2

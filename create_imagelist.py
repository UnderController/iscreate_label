from core.framedata import get_label_data
from core.imgpprocess import SaveImage, PreProcess
import os
import cv2
import glob

if __name__ == '__main__':
    for image_path in glob.glob("data/501-600/*.jpeg"):
        print image_path
        img = cv2.imread(image_path)
        prep = PreProcess(img)
        n_img = prep.group1()
        img_path = os.path.split(image_path)
        img_name__ = os.path.splitext(img_path[1])
        img_name_ = img_path[0] + '/' + img_name__[0]
        print img_name_
        cv2.imwrite(img_name_ + '_n.jpg', n_img)
        # exit()

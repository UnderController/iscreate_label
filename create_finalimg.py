import glob
import cv2
import os

if __name__ == '__main__':
    for image_path in glob.glob("data/tran/*draw_L.png"):
        print "dealing... ", image_path
        img = cv2.imread(image_path)

        # C++
        # prep = PreProcess(img)

        img_path = os.path.split(image_path)
        img_name__ = img_path[1].split('.')
        img_name_ = img_name__[0] + '.L.png'
        cv2.imwrite(img_name_, n_img)

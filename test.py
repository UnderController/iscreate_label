from core.framedata import get_label_data
from core.imgpprocess import SaveImage, PreProcess
import cv2


if __name__ == '__main__':
    img = cv2.imread("1324_small.jpg")
    PreProcess(img)

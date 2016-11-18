from core.framedata import get_label_data
from core.imgpprocess import SaveImage
import cv2


if __name__ == '__main__':
    img = cv2.imread("save.png")
    SaveImage(img)

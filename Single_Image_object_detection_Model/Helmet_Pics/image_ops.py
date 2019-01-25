import cv2
import numpy as np
import os

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized



#Load the original Image.

PATH_TO_TEST_IMAGES_DIR = '.'
TEST_IMAGE_PATHS = [ os.path.join('{}.jpg'.format(i)) for i in range(1,119) ]

print TEST_IMAGE_PATHS



for image_path in TEST_IMAGE_PATHS:

  print image_path

  image = cv2.imread(image_path)

  #cv2.imshow('Orig image', image)

  height = np.size(image, 0)
  width = np.size(image, 1)

  print height
  print width

  #Convert the image to Gray Scale.
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  #Show Image
  #cv2.imshow('Gray image', gray_image)

  gray_resize_image = image_resize(gray_image, height=150)

  cv2.imshow('Resize_Gray_Image', gray_resize_image)

  ret, thresh = cv2.threshold(gray_resize_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

  cv2.imshow('Segmented Image', thresh)

  #cv2.imshow('Segmented Image', image)

  picName = image_path + "_grayresized"
  #picName = image_path

  cv2.imwrite(picName, gray_resize_image)

  cv2.waitKey(0)
  cv2.destroyAllWindows()

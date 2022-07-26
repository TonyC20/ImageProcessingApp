from PIL import Image, ImageFilter, ImageOps
import numpy as np


def filter_scan(im: Image.Image, threshold: int) -> Image.Image:
    """
    takes in an image and creates puts it through a scan filter
    :param im: the image to be filtered
    :param threshold: threshold for scan
    :return: filtered image
    """
    im_data = np.asarray(im.convert('L'))
    im_data[im_data > threshold] = 255

    # filter_components edges
    mod_im = Image.fromarray(im_data)
    mod_im = mod_im.filter(ImageFilter.EDGE_ENHANCE)
    return mod_im


def rotate(im: Image.Image, angle: float) -> Image.Image:
    """
    takes in an image and rotates it
    :param im: the image to be rotated
    :param angle: the angle to rotate the image
    :return: the rotated image
    """
    im = im.convert('RGBA')
    return im.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))


def flip(im: Image.Image, horizontal: bool = True) -> Image.Image:
    """
    takes in an image and flips it
    :param im: the image to be flipped
    :param horizontal: whether to flip horizontally or vertically (default is horizontal)
    :return: the flipped image
    """
    if horizontal:
        return ImageOps.mirror(im)
    else:
        return ImageOps.flip(im)


def crop(im: Image.Image, left: int, top: int, right: int, bottom: int) -> Image.Image:
    """
    takes in an image and crops it based off of the passed in parameters in percentages
    :param im: the image to be cropped
    :param left: percent to cut from the left
    :param top: percent to cut from the top
    :param right: percent to cut from the right
    :param bottom: percent to cut from the bottom
    :return: the cropped image
    """
    return im.crop((
        int(left * im.width/100),
        int(top * im.height/100),
        int(im.width * (1 - right/100)),
        int(im.height * (1 - bottom/100))
    ))


def sharpen(im: Image.Image) -> Image.Image:
    """
    takes in an image and puts it through a "sharpen" filter
    :param im: the image to be filtered
    :return: the filtered image
    """
    return im.filter(ImageFilter.SHARPEN)


def blur(im: Image.Image, intensity: int) -> Image.Image:
    """
    takes in an image and puts it through a "blur" filter based on passed in intensity
    :param im: the image to be filtered
    :param intensity: the amount of blur
    :return: the filtered image
    """
    return im.filter(ImageFilter.GaussianBlur(1 + 2*intensity))


def smooth(im: Image.Image, intensity: int) -> Image.Image:
    """
    takes in an image and puts it through a smooth filter
    :param im: the image to be filtered
    :param intensity: the amount of smooth
    :return: the filtered image
    """
    for _ in range(intensity):
        im = im.filter(ImageFilter.SMOOTH)
    return im


def emboss(im: Image.Image) -> Image.Image:
    """
    takes in an image and puts it through an "emboss" filter
    :param im: the image to be filtered
    :return: the filtered image
    """
    return im.convert('L').filter(ImageFilter.EMBOSS).convert('RGBA')


def greyscale(im: Image.Image):
    """
    takes in an image and converts it to grayscale
    :param im: the image to be converted
    :return: the converted image
    """
    return im.convert('L').convert('RGBA')


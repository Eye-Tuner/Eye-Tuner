"""
PIL patcher
Import this module first before importing PIL.

Written by D. H. Kim
"""


def pillow_patch():
    from PIL import Image
    Image.fromstring = Image.frombytes
    Image.Image.tostring = Image.Image.tobytes
    return Image


pillow_patch()

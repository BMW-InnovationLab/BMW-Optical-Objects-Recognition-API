"""
This file contains all needed methods to preprocess the image
"""

import cv2

every_possible_rotation = [
    cv2.ROTATE_90_CLOCKWISE,
    cv2.ROTATE_90_COUNTERCLOCKWISE,
    cv2.ROTATE_180,
]
bounding_box_order = ["left", "top", "right", "bottom"]


def rotate_image(image, rotation):
    """
    Rotate the image givent eh cv2 rotation code
    """
    return cv2.rotate(image, rotation)


def denoise_image(image, d=9, sigmaColor=75, sigmaSpace=75):
    """
    Denoise the image while keeping edges clean
    """
    return cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)


def convert_to_binary(image):
    """
    Normalizes the image by transforming to grayscale then
    applying adaptiveThreshold with correct parameters for barcode.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    __, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return thresh


def decoded_to_json(decoded_message):
    """
    wrap the decoded data in json format
    """
    response_list = []

    for msg in decoded_message:

        response = {}
        response["text"] = msg.data
        coordinates = msg.rect
        coord_list = []
        coord_list.append(coordinates.left)
        coord_list.append(coordinates.top)
        coord_list.append(coordinates.left+coordinates.width)
        coord_list.append(coordinates.top+coordinates.height)
        response["box"] = coord_list
        response["score"] = 1
        response_list.append(response)

    return response_list

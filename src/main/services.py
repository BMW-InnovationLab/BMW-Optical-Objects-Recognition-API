"""
This file contains all needed methods to decoded the optical objects (Text fields, Data Matrices and QR codes)
"""

import pytesseract
import pylibdmtx.pylibdmtx
import pyzbar.pyzbar
import numpy as np
from img_utils import *
from ocr_utils import *


def ocr_service(image):
    """
    This method will take an image and return the extracted text from the image
    """

    # convert image to grayscale for better accuracy
    processed_img = image.convert('L')

    # Get data including boxes, confidences, line and page numbers
    extracted = pytesseract.image_to_data(
        processed_img, output_type='data.frame')

    # extract text with positive confidence only
    valid_df = extracted.loc[extracted["conf"] > 0, :]

    # process text
    extracted_text = process_extracted_text(valid_df)

    # calculate the bounding box data based on pytesseract results
    bounding_box = get_text_bounding_box(valid_df)

    # wrap each prediction in json format
    response = ocr_to_json(extracted_text, bounding_box, valid_df)

    return response


def data_matrix_service(image):
    """
    This method will take an image and decode the extracted data matrix code from the image
    """

    # convert the iamge into an numpy array for easier processing
    image = np.array(image.convert('RGB'))

    # process the image to remove noise
    denoised = denoise_image(image)

    # convert the image into a binary one for faster decoding
    binarized = convert_to_binary(denoised)

    # decode the datamatrix
    decoded = pylibdmtx.pylibdmtx.decode(binarized)

    if decoded:
        return decoded_to_json(decoded)

    for rotation in every_possible_rotation:

        # Try several rotations for possible detection
        rotated = rotate_image(binarized, rotation)

        # decode the rotated datamatrix
        decoded = pylibdmtx.pylibdmtx.decode(rotated)

        if decoded:
            return decoded_to_json(decoded)

    return None


def qr_service(image):
    """
    This method will take an image and decode the extracted QR code from the image
    """

    # convert the iamge into an numpy array for easier processing
    image = np.array(image.convert('RGB'))

    # process the image to remove noise
    denoised = denoise_image(image)

    # convert the image into a binary one for faster decoding
    binarized = convert_to_binary(denoised)

    # decode the qr code
    decoded = pyzbar.pyzbar.decode(binarized)

    if decoded:
        return decoded_to_json(decoded)

    for rotation in every_possible_rotation:

        # Try several rotations for possible detection
        rotated = rotate_image(image, rotation)

        # decode the rotated qr code
        decoded = pyzbar.pyzbar.decode(rotated)

        if decoded:
            return decoded_to_json(decoded)

    return None

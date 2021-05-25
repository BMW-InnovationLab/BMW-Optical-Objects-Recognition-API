"""
This file contains all needed methods to pre-process the extracted text
"""

import unicodedata
import re

bounding_box_order = ["left", "top", "right", "bottom"]


def process_extracted_text(dataframe):
    """
    Removes special characters and unwanted spaces from the extracted text
    """
    extracted_text = " ".join(dataframe["text"].values)
    extracted_text = str(unicodedata.normalize('NFKD', extracted_text).encode('ascii', 'ignore').decode()).replace("\n", " ").replace(
        "...", ".").replace("..", ".").replace('”', ' ').replace('“', ' ').replace("'", ' ').replace('\"', '').replace("alt/1m", "").strip()
    extracted_text = re.sub(
        '[^A-Za-z0-9.!?,;%:=()\[\]$€&/\- ]+', '', extracted_text)
    extracted_text = " ".join(extracted_text.split())

    return extracted_text


def get_text_bounding_box(dataframe):
    """
    Calculate bounding box of text starting from the first detected block and ending with the last detected block
    """
    coordinates = {}
    index = dataframe.index.values
    coordinates["left"] = dataframe.loc[index[0], "left"]
    coordinates["top"] = dataframe.loc[index[0], "top"]
    coordinates["bottom"] = dataframe.loc[index[-1],
                                          "top"] + dataframe.loc[index[-1], "height"]
    coordinates["right"] = dataframe.loc[index[-1],
                                         "left"] + dataframe.loc[index[-1], "width"]
    bounding_box = [coordinates[el].item() for el in bounding_box_order]

    return bounding_box


def ocr_to_json(extracted_text, bounding_box, dataframe):
    """
    wrap the extracted text in json format
    """
    response = {}
    response["text"] = extracted_text
    response["box"] = bounding_box
    response["score"] = dataframe["conf"].mean()/100.0

    return [response]

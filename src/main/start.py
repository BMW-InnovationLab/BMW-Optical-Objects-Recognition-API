import sys
from typing import List
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form, File, UploadFile, Header, HTTPException
from services import ocr_service, data_matrix_service, qr_service
from datetime import datetime
import pytz
from PIL import Image

tz = pytz.timezone("Europe/Berlin")

app = FastAPI(version='1.0', title='BMW InnovationLab Optical Objects Recognition Automation',
              description="<b>API for reading text, Data Matrices and QR Codes</b></br></br>"
              "<b>Contact the developers:</b></br>"
              "<b>Anis Ismail:</b></br>"
              "<b>BMW Innovation Lab: <a href='mailto:innovation-lab@bmw.de'>innovation-lab@bmw.de</a></b>")


# app.mount("/public", StaticFiles(directory="/main/public"), name="public")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.post('/models/{model_name}/ocr')
async def optical_character_recognition(
    model_name: str,
    image: UploadFile = File(
        ..., description="Image to perform optical character recognition:"),
):
    """
        Takes an image and returns extracted text informations.

        The image is passed to the OCR-Service for text extraction

        :param model: Model name or model hash

        :param image: Image file

        :return: Text fields with the detected text inside

    """
    # run ocr_service
    response = None
    try:
        image = Image.open(image.file)
        response = ocr_service(image)
    except:
        raise HTTPException(
            status_code=500, detail='Unexpected Error during Inference (Determination of Texts)')

    if not response:
        raise HTTPException(
            status_code=400, detail='Inference (Determination of Texts) is not Possible')

    return response


@app.post('/models/{model_name}/data_matrix')
async def data_matrix_recognition(
    model_name: str,
    image: UploadFile = File(
        ..., description="Image to perform Data Matrix decoding:"),
):
    """
        Takes an image and returns decoded data matrices.

        The image is passed to the Data-Matrix-Service for text extraction

        :param model: Model name or model hash

        :param image: Image file

        :return: Text fields with the decoded data matrices inside

    """
    # run data_matrix_service
    response = None
    try:
        image = Image.open(image.file)
        response = data_matrix_service(image)
    except:
        raise HTTPException(
            status_code=500, detail='Unexpected Error during Inference (Determination of Data Matrices)')

    if not response:
        raise HTTPException(
            status_code=400, detail='Inference (Determination of Data Matrices) is not Possible')

    return response


@app.post('/models/{model_name}/qr_code')
async def qr_code_recognition(
    model_name: str,
    image: UploadFile = File(
        ..., description="Image to perform QR Code decoding:"),
):
    """
        Takes an image and returns decoded QR codes.

        The image is passed to the QR-Service for text extraction

        :param model: Model name or model hash

        :param image: Image file

        :return: Text fields with the decoded QR codes inside

    """
    # run qr_service
    response = None
    try:
        image = Image.open(image.file)
        response = qr_service(image)
    except:
        raise HTTPException(
            status_code=500, detail='Unexpected Error during Inference (Determination of QR Codes)')

    if not response:
        raise HTTPException(
            status_code=400, detail='Inference (Determination of QR Codes) is not Possible')

    return response

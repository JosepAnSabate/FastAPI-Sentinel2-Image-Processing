# FastAPI Sentinel2 Image Processing

This repository contains a basic FastAPI application for processing Sentinel-2 satellite images.

## Requirements
- FastAPI
- Rasterio
- NumPy
- Matplotlib
- PIL

## Endpoints

### Get Image Attributes

- **Endpoint:** `/attributes/`
- **Method:** POST
- **Description:** Upload a Sentinel-2 image file and retrieve its attributes.

### Generate Thumbnail Image

- **Endpoint:** `/thumbnail/`
- **Method:** POST
- **Description:** Generate a thumbnail image from a Sentinel-2 image file as a PNG.

### Generate Thumbnail Image

- **Endpoint:** `/thumbnail2/`
- **Method:** POST
- **Description:** Generate a thumbnail image from a Sentinel-2 image file as a PNG.

### Compute NDVI and Apply Color Palette

- **Endpoint:** `/ndvi/`
- **Method:** POST
- **Description:** Calculate the Normalized Difference Vegetation Index (NDVI) from a Sentinel-2 image file and apply a color palette.

## Usage

1. Install the required dependencies: `pip install fastapi rasterio numpy Pillow  python-multipart uvicorn`.
2. Start the FastAPI server: `uvicorn main:app --reload`.
3. Access the endpoints using a tool like API testing tool or go to `http://127.0.0.1:8000/docs`.



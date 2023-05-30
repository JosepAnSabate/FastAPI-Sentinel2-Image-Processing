from fastapi import FastAPI, File, UploadFile
import rasterio
import numpy as np
from PIL import Image
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/attributes/")
async def get_image_attributes(image: UploadFile = File(...)):
    # Save the uploaded image locally
    image_path = "uploaded_image.tif"
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Read the image using Rasterio
    dataset = rasterio.open(image_path)

    # Extract image attributes
    width = dataset.width
    height = dataset.height
    num_bands = dataset.count
    crs = dataset.crs.to_dict()
    bounding_box = dataset.bounds

    # Close the dataset
    dataset.close()

    # Convert the bounding box coordinates to a list
    bounding_box = list(bounding_box)

    # Prepare the response as a JSON object
    response = {
        "image_size": {"width": width, "height": height},
        "num_bands": num_bands,
        "coordinate_reference_system": crs,
        "bounding_box": bounding_box,
        "uploaded_file": image.filename,
        "file_size": image.file.seek(0, 2),
    }

    return response


@app.post("/thumbnail/")
async def generate_thumbnail(image: UploadFile = File(...)):
    # Save the uploaded image locally
    image_path = "uploaded_image.tif"
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Open the image using rasterio
    with rasterio.open(image_path) as dataset:
        # Read the three bands, bands 4, 3, and 2 for RGB)
        bands = dataset.read([4, 3, 2])
    
    # Reshape the bands into an RGB image
    image_data = np.transpose(bands, (1, 2, 0))

    # Normalize the pixel values to the range [0, 255]
    image_data = (image_data / image_data.max()) * 255
    # Convert the RGB image to PIL Image
    image_pil = Image.fromarray(np.uint8(image_data))
   
    # Create an in-memory buffer to save the image as PNG
    image_pil.save("output.png", format="PNG")
    
    return FileResponse('output.png', media_type="image/png")

@app.post("/thumbnail2/")
async def generate_thumbnail2(image: UploadFile = File(...)):
    # Save the uploaded image locally
    image_path = "uploaded_image.tif"
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Open the image using rasterio
    with rasterio.open(image_path) as dataset:
        # Read the three RGB bands (e.g., bands 4, 3, and 2)
        rgb_bands = dataset.read([4, 3, 2])

    # Normalize the pixel values to the range [0, 1]
    rgb_bands = rgb_bands / 10000.0

    # Clip values exceeding the valid range [0, 1]
    rgb_bands = np.clip(rgb_bands, 0, 1)

    # Reshape the RGB bands into an RGB image
    rgb_image = np.transpose(rgb_bands, (1, 2, 0))

    # Scale the pixel values to the range [0, 255]
    rgb_image = (rgb_image * 255).astype(np.uint8)


    # Convert the image to PIL Image
    image_pil = Image.fromarray(rgb_image.astype(np.uint8))

    # Save the PIL Image as a PNG file
    image_pil.save('rgb_image.png')

    return FileResponse('rgb_image.png', media_type="image/png")


@app.post("/ndvi/")
async def compute_ndvi(image: UploadFile = File(...)):
    # Save the uploaded image locally
    image_path = "uploaded_image.tif"
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Open the image using Rasterio
    with rasterio.open(image_path) as dataset:
        # Read the red and near-infrared bands
        red_band = dataset.read(4)  # Red band
        nir_band = dataset.read(8)  # Near-infrared band

    # Define the color palette for NDVI visualization
    palette = np.array([
        [128, 0, 0],     # Dark Red for NDVI < -0.2 (No vegetation)
        [255, 0, 0],     # Red for -0.2 <= NDVI < 0 (Low vegetation)
        [255, 255, 255], # White for 0 <= NDVI < 0.5 (Moderate vegetation)
        [0, 255, 0],     # Green for 0.5 <= NDVI < 0.8 (High vegetation)
        [0, 128, 0]      # Dark Green for NDVI >= 0.8 (Very high vegetation)
    ], dtype=np.uint8)
    # Calculate NDVI
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    scaled_ndvi = ((ndvi + 1) * 2).astype(np.uint8)

    # Apply the color palette to the NDVI image
    ndvi_color_image = Image.fromarray(scaled_ndvi, mode='P')
    ndvi_color_image.putpalette(palette.flatten())

    # Save the NDVI image as PNG
    ndvi_color_image.save('ndvi_image.png')

    return FileResponse('ndvi_image.png', media_type="image/png")
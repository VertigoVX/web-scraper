# Web Scraper for OSM Tiles
This Python program downloads and processes OpenStreetMap (OSM) tiles for a specified region (Uganda) and zoom levels. The tiles are upscaled and saved in JPEG format with specified quality.

# Features
- Download OSM Tiles: Fetch tiles from OpenStreetMap for given zoom levels.
- Image Processing: Upscale the downloaded images and save them in JPEG format.
- Multi-threaded Execution: Use multiple threads to speed up the download and processing tasks.
  
# Prerequisites
- Python 3.x
- Required Python packages: requests, Pillow
- 
You can install the required packages using pip:

```bash
pip install requests pillow
```
# Usage
Clone the Repository:

```bash
git clone https://github.com/VertigoVX/webScraper.git
cd webScraper
```

# Run the Script:

Execute the Python script to start downloading and processing OSM tiles:

```bash
python webScraper.py
```

# Parameters:

Currently this code functions as a means to download OSM map tiles for Uganda, this can be changed to whichever country or region you wish to download. The download_uganda_tiles function takes the following parameters:

- min_zoom: Minimum zoom level to download.
- max_zoom: Maximum zoom level to download.
- upscale_factor: Factor by which to upscale the images.
- quality: JPEG quality for the saved images (0 to 100).
- heap_size: Size of the batch to process concurrently.

# Example usage:

```python
download_uganda_tiles(min_zoom=5, max_zoom=15, upscale_factor=2, quality=85, heap_size=50)
```
# License
This project is licensed under the MIT License. 

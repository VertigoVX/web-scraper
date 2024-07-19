import os
import math
import requests
import heapq
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Set a custom User-Agent
headers = {
    'User-Agent': 'webScraper/1.0 ('enter user email')'
}

# Create the osm_tiles directory if it doesn't exist
os.makedirs('osm_tiles', exist_ok=True)


def download_and_process_tile(args):
    priority, (x, y, zoom, upscale_factor, quality) = args
    url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

        # Open the image using Pillow
        img = Image.open(BytesIO(response.content))

        # Convert to RGB mode if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Upscale the image
        new_size = tuple(dim * upscale_factor for dim in img.size)
        img = img.resize(new_size, Image.LANCZOS)

        # Save the processed image
        filename = f"uganda_tile_{zoom}_{x}_{y}.jpg"
        filepath = os.path.join('osm_tiles', filename)
        img.save(filepath, 'JPEG', quality=quality, optimize=True)

        print(f"Downloaded, processed, and saved {filepath}")
        return priority, filepath
    except requests.exceptions.RequestException as e:
        print(f"Failed to download tile at {url}: {e}")
        return priority, None
    except IOError as e:
        print(f"Failed to process image from {url}: {e}")
        return priority, None


def lon_to_x(lon, zoom):
    return int((lon + 180) / 360 * 2 ** zoom)


def lat_to_y(lat, zoom):
    return int(
        (1 - math.log(math.tan(lat * math.pi / 180) + 1 / math.cos(lat * math.pi / 180)) / math.pi) / 2 * 2 ** zoom)


def download_uganda_tiles(min_zoom, max_zoom, upscale_factor=2, quality=85, heap_size=30):
    # Approximate bounding box for Uganda
    min_lat, max_lat = -1.5, 4.5
    min_lon, max_lon = 29.5, 35.5

    task_heap = []
    priority = 0

    for zoom in range(min_zoom, max_zoom + 1):
        min_x = lon_to_x(min_lon, zoom)
        max_x = lon_to_x(max_lon, zoom)
        min_y = lat_to_y(max_lat, zoom)
        max_y = lat_to_y(min_lat, zoom)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                heapq.heappush(task_heap, (priority, (x, y, zoom, upscale_factor, quality)))
                priority += 1

        print(f"Added tasks for zoom level {zoom}")

    total_tasks = len(task_heap)
    completed_tasks = 0

    with ThreadPoolExecutor(max_workers=8) as executor:
        while task_heap:
            batch = []
            for _ in range(min(heap_size, len(task_heap))):
                batch.append(heapq.heappop(task_heap))

            futures = [executor.submit(download_and_process_tile, task) for task in batch]
            results = [future.result() for future in as_completed(futures)]

            # Sort the results to maintain order
            results.sort(key=lambda x: x[0])
            for _, filepath in results:
                if filepath:
                    completed_tasks += 1
                    print(f"Completed: {filepath} ({completed_tasks}/{total_tasks})")

            # Add a small delay to avoid overwhelming the server
            time.sleep(1)

    print("All tasks completed.")


# Usage
download_uganda_tiles(5, 15, upscale_factor=2, quality=85, heap_size=50)

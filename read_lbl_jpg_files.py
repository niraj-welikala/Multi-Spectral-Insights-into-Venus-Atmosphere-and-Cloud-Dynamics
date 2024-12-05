import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import re
from datetime import datetime

def read_lbl(lbl_path):
    """Read and parse LBL file"""
    try:
        with open(lbl_path, 'r') as f:
            content = f.read()
            
        # Extract key metadata using simple regex
        metadata = {}
        patterns = {
            'product_id': r'PRODUCT_ID\s*=\s*"([^"]*)"',
            'start_time': r'START_TIME\s*=\s*"([^"]*)"',
            'filter_name': r'FILTER_NAME\s*=\s*"([^"]*)"',
            'exposure_duration': r'EXPOSURE_DURATION\s*=\s*([\d.]+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                value = match.group(1)
                # Convert exposure duration to float
                if key == 'exposure_duration':
                    value = float(value)
                metadata[key] = value
                
        return metadata
            
    except Exception as e:
        print(f"Error reading LBL file: {e}")
        return None

def read_jpg(jpg_path):
    """Read JPG file"""
    try:
        # Read image
        img = Image.open(jpg_path)
        # Convert to numpy array
        img_array = np.array(img)
        return img_array
            
    except Exception as e:
        print(f"Error reading JPG file: {e}")
        return None

def display_data(image, metadata):
    """Display image and metadata"""
    plt.figure(figsize=(10, 8))
    plt.imshow(image, cmap='gray')
    plt.title(f"Venus Express VMC Image\nFilter: {metadata.get('filter_name', 'Unknown')}")
    plt.show()
    
    print("\nMetadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

# Example usage
if __name__ == "__main__":
    # Replace with your actual file paths
    lbl_path = "/Users/n_welikala/cvprojects/venus/data/vmc/raw/0557/V0557_0000_UV2.LBL"
    jpg_path = "/Users/n_welikala/cvprojects/venus/data/vmc/raw/0557/V0557_0000_UV2.JPG"
    
    # Read files
    metadata = read_lbl(lbl_path)
    image = read_jpg(jpg_path)
    
    # Display results
    if metadata and image is not None:
        display_data(image, metadata)

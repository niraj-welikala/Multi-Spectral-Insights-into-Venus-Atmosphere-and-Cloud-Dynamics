import os
from collections import defaultdict
import shutil

def extract_uv2_images(raw_dir, base_dir):
    """
    Extract UV2 images and their LBL files to a filtered directory
    
    Parameters:
    raw_dir: str, path to raw data directory
    base_dir: str, path to base VMC directory
    """
    # Create filtered directory structure
    filtered_dir = os.path.join(base_dir, 'filtered')
    os.makedirs(filtered_dir, exist_ok=True)
    
    output_dir = os.path.join(filtered_dir, 'uv2')
    os.makedirs(output_dir, exist_ok=True)
    
    uv2_files = defaultdict(list)
    
    # Walk through raw data directory
    for root, _, files in os.walk(raw_dir):
        orbit = os.path.basename(root)
        
        # Find UV2 files and their corresponding LBL files
        for file in files:
            if '_UV2.' in file:  # Match UV2 files
                orbit_dir = os.path.join(output_dir, orbit)
                os.makedirs(orbit_dir, exist_ok=True)
                
                # Copy file to new location
                src = os.path.join(root, file)
                dst = os.path.join(orbit_dir, file)
                shutil.copy2(src, dst)
                uv2_files[orbit].append(file)
    
    # Print summary
    print("\nUV2 Image Extraction Summary:")
    print("-" * 50)
    
    total_jpg = 0
    total_lbl = 0
    
    for orbit in sorted(uv2_files.keys()):
        jpg_count = len([f for f in uv2_files[orbit] if f.endswith('.JPG')])
        lbl_count = len([f for f in uv2_files[orbit] if f.endswith('.LBL')])
        
        print(f"\nOrbit {orbit}:")
        print(f"  JPG files: {jpg_count}")
        print(f"  LBL files: {lbl_count}")
        
        total_jpg += jpg_count
        total_lbl += lbl_count
    
    print(f"\nTotal UV2 files extracted:")
    print(f"Total JPG files: {total_jpg}")
    print(f"Total LBL files: {total_lbl}")

if __name__ == "__main__":
    raw_dir = "/Users/n_welikala/cvprojects/venus/data/vmc/raw"
    base_dir = "/Users/n_welikala/cvprojects/venus/data/vmc"
    extract_uv2_images(raw_dir, base_dir)
    

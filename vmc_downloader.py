#Niraj Welikala 03.12.24
#For an initial analysis, I estimate needing
#At least 50-100 images for training
#10-20 images for validation 
#10-20 images for testing

# venus_downloader.py
import os
import requests
from urllib.parse import urljoin
import re
import time
from typing import List, Tuple

class VenusExpressDownloader:
    def __init__(self, base_url: str = "https://archives.esac.esa.int/psa/ftp/VENUS-EXPRESS/VMC/VEX-V-VMC-3-RDR-EXT1-V3.0/BROWSE/",
                 base_output_dir: str = "/Users/n_welikala/cvprojects/venus/data/vmc/raw"):
        self.base_url = base_url
        self.base_output_dir = base_output_dir
        self.session = requests.Session()
    
    def get_orbit_directories(self) -> List[str]:
        """Get list of orbit directories (e.g., 0550/, 0551/, etc.)"""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            dir_pattern = r'href="(\d{4}/)"'
            directories = re.findall(dir_pattern, response.text)
            
            return sorted(directories)
            
        except requests.RequestException as e:
            print(f"Error fetching orbit directories: {e}")
            return []
    
    def get_files_in_directory(self, directory: str) -> List[Tuple[str, str]]:
        """Get pairs of JPG and LBL files in a directory"""
        url = urljoin(self.base_url, directory)
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            jpg_pattern = r'href="([^"]+\.JPG)"'
            lbl_pattern = r'href="([^"]+\.LBL)"'
            
            jpg_files = re.findall(jpg_pattern, response.text)
            lbl_files = re.findall(lbl_pattern, response.text)
            
            pairs = []
            for jpg in jpg_files:
                base_name = os.path.splitext(jpg)[0]
                matching_lbl = next((lbl for lbl in lbl_files if os.path.splitext(lbl)[0] == base_name), None)
                if matching_lbl:
                    pairs.append((jpg, matching_lbl))
            
            return pairs
            
        except requests.RequestException as e:
            print(f"Error fetching files in directory {directory}: {e}")
            return []
    
    def download_file(self, directory: str, filename: str, output_dir: str) -> bool:
        """Download a single file"""
        url = urljoin(self.base_url + directory, filename)
        output_path = os.path.join(output_dir, filename)
        
        if os.path.exists(output_path):
            print(f"Skipping existing file: {filename}")
            return True
        
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            print(f"Downloaded: {filename}")
            return True
            
        except requests.RequestException as e:
            print(f"Error downloading {filename}: {e}")
            return False
    
    def download_orbit_data(self, directory: str, max_pairs: int = None) -> int:
        """Download all paired JPG and LBL files from an orbit directory"""
        output_dir = os.path.join(self.base_output_dir, directory.strip('/'))
        os.makedirs(output_dir, exist_ok=True)
        
        pairs = self.get_files_in_directory(directory)
        if max_pairs:
            pairs = pairs[:max_pairs]
        
        success_count = 0
        for jpg, lbl in pairs:
            if self.download_file(directory, jpg, output_dir):
                if self.download_file(directory, lbl, output_dir):
                    success_count += 1
            
            time.sleep(0.5)  # Be nice to the server
        
        return success_count

def list_downloaded_files(base_dir):
    """List all downloaded files and count them"""
    total_jpg = 0
    total_lbl = 0
    
    print("\nDownloaded files by orbit:")
    for root, dirs, files in os.walk(base_dir):
        jpg_files = [f for f in files if f.endswith('.JPG')]
        lbl_files = [f for f in files if f.endswith('.LBL')]
        
        if jpg_files or lbl_files:
            orbit = os.path.basename(root)
            print(f"\nOrbit {orbit}:")
            print(f"  JPG files: {len(jpg_files)}")
            print(f"  LBL files: {len(lbl_files)}")
            
            total_jpg += len(jpg_files)
            total_lbl += len(lbl_files)
    
    print(f"\nTotal files downloaded:")
    print(f"Total JPG files: {total_jpg}")
    print(f"Total LBL files: {total_lbl}")
    

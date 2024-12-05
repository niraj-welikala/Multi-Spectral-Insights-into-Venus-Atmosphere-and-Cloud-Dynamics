import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage import exposure, filters  # Changed from restoration to filters
from pathlib import Path

class VMCImageProcessor:
    def __init__(self, filtered_dir, processed_dir):
        self.filtered_dir = Path(filtered_dir)
        self.processed_dir = Path(processed_dir)
        os.makedirs(self.processed_dir, exist_ok=True)
    
    def load_image(self, file_path):
        """Load an image and convert to numpy array"""
        return np.array(Image.open(file_path))
    
    def preprocess_image(self, image):
        """Apply basic preprocessing steps"""
        # Convert to float for processing
        img_float = image.astype(float)
        
        # Apply contrast stretching
        p2, p98 = np.percentile(img_float, (2, 98))
        img_contrast = exposure.rescale_intensity(img_float, in_range=(p2, p98))
        
        # Denoise using Gaussian filter
        img_denoised = filters.gaussian(img_contrast, sigma=0.5)  
        
        # Normalize to 0-1 range
        img_normalized = exposure.rescale_intensity(img_denoised)
        
        return img_normalized
    
    def process_all_images(self):
        """Process all UV2 JPG images in the filtered directory"""
        # Create output directory structure
        for orbit_dir in self.filtered_dir.glob("*"):
            if orbit_dir.is_dir():
                output_orbit_dir = self.processed_dir / orbit_dir.name
                os.makedirs(output_orbit_dir, exist_ok=True)
                
                # Process each JPG in the orbit directory
                for jpg_file in orbit_dir.glob("*UV2.JPG"):
                    print(f"Processing {jpg_file.name}")
                    
                    # Load and process image
                    img = self.load_image(jpg_file)
                    processed_img = self.preprocess_image(img)
                    
                    # Save processed image
                    output_path = output_orbit_dir / f"proc_{jpg_file.name}"
                    plt.imsave(output_path, processed_img, cmap='gray')
    
    def show_comparison(self, orbit, image_number):
        """Show original vs processed image comparison"""
        # Construct file paths
        orig_path = self.filtered_dir / orbit / f"V{orbit}_{image_number:04d}_UV2.JPG"
        proc_path = self.processed_dir / orbit / f"proc_V{orbit}_{image_number:04d}_UV2.JPG"
        
        if not orig_path.exists() or not proc_path.exists():
            print("Image files not found!")
            return
        
        # Load images
        orig_img = self.load_image(orig_path)
        proc_img = self.load_image(proc_path)
        
        # Display comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        ax1.imshow(orig_img, cmap='gray')
        ax1.set_title('Original Image')
        ax1.axis('off')
        
        ax2.imshow(proc_img, cmap='gray')
        ax2.set_title('Processed Image')
        ax2.axis('off')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    filtered_dir = "/Users/n_welikala/cvprojects/venus/data/vmc/filtered/uv2"
    processed_dir = "/Users/n_welikala/cvprojects/venus/data/vmc/processed/uv2"
    
    processor = VMCImageProcessor(filtered_dir, processed_dir)
    processor.process_all_images()

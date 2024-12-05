import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from skimage import feature, filters, segmentation, color, morphology
from skimage.feature import blob_dog
import cv2

class VMCFeatureDetector:
    def __init__(self, processed_dir):
        self.processed_dir = Path(processed_dir)
    
    def load_image(self, orbit, image_number):
        """Load a processed image and convert to grayscale"""
        image_path = self.processed_dir / orbit / f"proc_V{orbit}_{image_number:04d}_UV2.JPG"
        # Read image and convert to grayscale if it's RGB
        image = plt.imread(image_path)
        if len(image.shape) == 3:  # If image is RGB
            image = color.rgb2gray(image)
        return image
    
    def detect_edges(self, image):
        """Detect cloud edges using Canny edge detection"""
        # Compute automatic sigma based on image statistics
        sigma = np.std(image) * 2
        
        # Apply Canny edge detection
        edges = feature.canny(
            image,
            sigma=sigma,
            low_threshold=0.1,
            high_threshold=0.3
        )
        return edges
    
    def detect_blobs(self, image):
        """Detect blob-like cloud features"""
        blobs = blob_dog(
            image,
            min_sigma=3,
            max_sigma=30,
            threshold=.1
        )
        return blobs
    
    def detect_regions(self, image):
        """Segment image into regions using multiple thresholds"""
        # Apply median filter to reduce noise
        smoothed = filters.median(image, morphology.disk(3))
        
        # Create multiple thresholds for different intensity levels
        thresholds = filters.threshold_multiotsu(smoothed, classes=4)
        
        # Create segmentation using these thresholds
        regions = np.digitize(smoothed, bins=thresholds)
        
        # Optional: clean up small regions
        cleaned = morphology.remove_small_objects(regions, min_size=50)
        
        return cleaned
    
    def analyze_image(self, orbit, image_number):
        """Perform comprehensive feature analysis on an image"""
        # Load image
        image = self.load_image(orbit, image_number)
        
        # Perform different types of feature detection
        edges = self.detect_edges(image)
        blobs = self.detect_blobs(image)
        regions = self.detect_regions(image)
        
        # Visualize results
        fig, axes = plt.subplots(2, 2, figsize=(15, 15))
        
        # Original
        axes[0, 0].imshow(image, cmap='gray')
        axes[0, 0].set_title('Original Processed Image')
        axes[0, 0].axis('off')
        
        # Edges
        axes[0, 1].imshow(edges, cmap='gray')
        axes[0, 1].set_title('Cloud Edge Detection')
        axes[0, 1].axis('off')
        
        # Blobs
        axes[1, 0].imshow(image, cmap='gray')
        axes[1, 0].set_title('Cloud Feature Detection')
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r, color='red', linewidth=1, fill=False)
            axes[1, 0].add_patch(c)
        axes[1, 0].axis('off')
        
        # Regions
        axes[1, 1].imshow(regions, cmap='nipy_spectral')
        axes[1, 1].set_title('Cloud Region Segmentation')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        return {
            'edges': edges,
            'blobs': blobs,
            'regions': regions
        }

if __name__ == "__main__":
    processed_dir = "/Users/n_welikala/cvprojects/venus/data/vmc/processed/uv2"
    detector = VMCFeatureDetector(processed_dir)
    
    # Analyze a sample image
    results = detector.analyze_image('0550', 0)

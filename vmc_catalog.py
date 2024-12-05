import os
from collections import defaultdict

def catalog_images(data_dir):
    """Analyze the downloaded VMC images by orbit and filter"""
    orbit_catalog = defaultdict(lambda: defaultdict(int))
    
    # Walk through directories
    for root, _, files in os.walk(data_dir):
        # Only process JPG files
        jpg_files = [f for f in files if f.endswith('.JPG')]
        
        if jpg_files:
            orbit = os.path.basename(root)
            
            # Count filter types in this orbit
            for jpg in jpg_files:
                # Extract filter type (last 3 chars before .JPG)
                filter_type = jpg[-7:-4]  # e.g., UV2, N12, N22, VI2
                orbit_catalog[orbit][filter_type] += 1
    
    # Print analysis
    print("\nImage Catalog by Orbit:")
    print("-" * 50)
    
    total_by_filter = defaultdict(int)
    
    for orbit in sorted(orbit_catalog.keys()):
        print(f"\nOrbit {orbit}:")
        for filter_type, count in sorted(orbit_catalog[orbit].items()):
            print(f"  {filter_type}: {count} images")
            total_by_filter[filter_type] += count
    
    print("\nTotal Images by Filter Type:")
    print("-" * 50)
    for filter_type, count in sorted(total_by_filter.items()):
        print(f"{filter_type}: {count} images")

if __name__ == "__main__":
    data_dir = "/Users/n_welikala/cvprojects/venus/data/vmc/raw"
    catalog_images(data_dir)

import ftplib
import os
import rasterio
from rasterio.io import MemoryFile
from datetime import datetime

def get_latest_bom():
    host = "ftp.bom.gov.au"
    path = "/anon/gen/gms/"
    file_id = "IDE00430"
    temp_raw = "raw_bom.tif"
    
    print("Connecting to BoM FTP...")
    try:
        ftp = ftplib.FTP(host)
        ftp.login()
        ftp.cwd(path)
        files = [f for f in ftp.nlst() if file_id in f and f.endswith(".tif")]
        latest = sorted(files)[-1]
        
        with open(temp_raw, "wb") as f:
            ftp.retrbinary(f"RETR {latest}", f.write)
        ftp.quit()
        return temp_raw
    except Exception as e:
        print(f"FTP Error: {e}")
        return None

def convert_to_cog(input_path, output_path):
    print(f"Converting {input_path} to Cloud Optimized GeoTIFF (COG)...")
    try:
        with rasterio.open(input_path) as src:
            # Prepare profile for COG: Tiled, LZW compression, and Power-of-2 overviews
            profile = src.profile.copy()
            profile.update(
                driver='GTiff',
                interleave='pixel',
                tiled=True,
                blockxsize=256,
                blockysize=256,
                compress='lzw',
                nodata=0
            )
            
            with rasterio.open(output_path, 'w', **profile) as dst:
                dst.write(src.read())
        return True
    except Exception as e:
        print(f"Conversion Error: {e}")
        return False

if __name__ == "__main__":
    raw_file = get_latest_bom()
    if raw_file:
        success = convert_to_cog(raw_file, "latest_cloud.tif")
        if success:
            print("Process complete. Ready for GitHub Push.")
            os.remove(raw_file)

import ftplib
import os

def download_latest_from_bom():
    host = "ftp.bom.gov.au"
    path = "/anon/gen/gms/"
    file_id = "IDE00430"
    # Save the file with a FIXED name so the URL never changes
    local_file = "latest_cloud.tif"
    
    try:
        ftp = ftplib.FTP(host)
        ftp.login()
        ftp.cwd(path)
        files = [f for f in ftp.nlst() if file_id in f and f.endswith(".tif")]
        latest = sorted(files)[-1]
        
        with open(local_file, "wb") as f:
            ftp.retrbinary(f"RETR {latest}", f.write)
        ftp.quit()
        print(f"Successfully downloaded {latest} as {local_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_latest_from_bom()

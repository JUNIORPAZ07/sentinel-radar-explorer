import os
import boto3
import datetime
from pystac_client import Client
from dotenv import load_dotenv

# 1. Unlock the Vault
load_dotenv()
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('CDSE_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('CDSE_SECRET_KEY'),
    endpoint_url='https://eodata.dataspace.copernicus.eu',
    region_name='default'
)

print("🔐 Authenticated with S3. Searching the new V1 endpoint for Bay Area data...")

# 2. THE FIX: Using the new v1 endpoint
catalog = Client.open("https://stac.dataspace.copernicus.eu/v1")

bbox = [-123.00, 37.10, -121.50, 38.40] 
today = datetime.date.today()
last_season = today - datetime.timedelta(days=90)
time_range = f"{last_season}/{today}"

# THE FIX: Using the correct new collection name
search = catalog.search(
    collections=["sentinel-1-grd"], 
    bbox=bbox,
    datetime=time_range,
    query={"sar:instrument_mode": {"eq": "IW"}}
)

items = list(search.items())

if len(items) == 0:
    print("❌ Still 0. Something else is wrong.")
else:
    # Get the newest image
    latest_item = items[0]
    print(f"📡 SUCCESS! Found newest image from: {latest_item.datetime}")
    print("📂 Locating the exact radar matrix file...")

    tiff_s3_uri = None
    
    # 3. Search the STAC item's assets for the VV polarization TIFF
    for key, asset in latest_item.assets.items():
        if 'vv' in key.lower() or ('vv' in asset.href.lower() and 'tif' in asset.href.lower()):
            tiff_s3_uri = asset.href
            break
            
    if tiff_s3_uri:
        # Clean the s3:// prefix for boto3 download
        tiff_key = tiff_s3_uri.replace("s3://eodata/", "")
        local_filename = "bay_area_radar_matrix.tiff"
        
        print(f"⬇️ Downloading {local_filename} (This might take a minute...)")
        
        try:
            s3.download_file('eodata', tiff_key, local_filename)
            print("✅ Download Complete! The matrix is ready for AI preprocessing.")
        except Exception as e:
            print(f"❌ Download failed: {e}")
    else:
        print("❌ Found the image record, but couldn't locate the .tiff asset inside it.")
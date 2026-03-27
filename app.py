import datetime
import streamlit as st
from pystac_client import Client

# 1. Page Config MUST be the very first Streamlit command
st.set_page_config(page_title="Sentinel-1 Radar Explorer", layout="wide")

# 2. Main Title and Description
st.title("🌍 Sentinel-1 SAR Data Explorer")
st.write("A tool to query the Copernicus Data Space Ecosystem for Synthetic Aperture Radar imagery.")

# 3. Calculate Default Dates (Last 30 Days)
today = datetime.date.today()
last_month = today - datetime.timedelta(days=30)

# 4. Sidebar Inputs
st.sidebar.header("Search Parameters")
start_date = st.sidebar.date_input("Start Date", last_month)
end_date = st.sidebar.date_input("End Date", today)

# 5. Execute Search Logic
if st.sidebar.button("Search Archive"):
    st.info("Connecting to Copernicus STAC API...")
    try:
        catalog = Client.open("https://catalogue.dataspace.copernicus.eu/stac")
        time_range = f"{start_date}/{end_date}"
        
        # Target area bounding box
        bbox = [-122.40, 37.90, -122.30, 38.00] 
        
        search = catalog.search(
            collections=["SENTINEL-1"],
            bbox=bbox,
            datetime=time_range,
            query={"sar:instrument_mode": {"eq": "IW"}}
        )
        
        items = list(search.items())
        
        if items:
            st.success(f"Found {len(items)} radar images in the archive!")
            for item in items:
                with st.expander(f"Image ID: {item.id}"):
                    st.write(f"**Date:** {item.datetime}")
                    st.code(f"S3 Path: {item.assets['PRODUCT'].href}", language="bash")
        else:
            st.warning("No images found for this date range.")
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
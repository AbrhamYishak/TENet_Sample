import requests
import os
import zipfile
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
from dotenv import load_dotenv
import h3
from metadata.views import updateMetadata,getLastupdate
load_dotenv()
BASE_FOLDER = os.path.join(os.path.dirname(os.getcwd()),"alaska_all_data")
print(BASE_FOLDER)
url = "https://healthsites.io/api/v3/facilities/"
FCCurl = "https://bdc.fcc.gov/api/public/map"
headers = {
    "username": os.environ.get("FCC_USERNAME"),
    "hash_value": os.environ.get("FCC_API")
}

params = {
    "api-key": os.environ.get("HEALTHSITE_API"),
    "page": 1,
    "extent": "-179.15, 51.21, -129.97, 71.44",
}
def load_data():
    try:
        result = requests.get(url=f"{FCCurl}/listAsOfDates",headers=headers)
        dates = result.json()["data"]
        latest_date = max(d["as_of_date"] for d in dates if d["data_type"] == "availability")
        if latest_date != getLastupdate():
            res = requests.get(  
                f"{FCCurl}/downloads/listAvailabilityData/{latest_date}",
                headers=headers)
            results = res.json()
            updateMetadata(latest_date)
            data = results.get("data")
            alaskaData = [item for item in data if item["state_name"] == "Alaska"]
            for i in alaskaData:
                fileID = i["file_id"]
                DownloadUrl = f"{FCCurl}/downloads/downloadFile/availability/{fileID}/1"
                res = requests.get(url=DownloadUrl,headers=headers)
                with open("alaska.zip", "wb") as f:
                    f.write(res.content)
                with zipfile.ZipFile("alaska.zip", "r") as zip_ref:
                    zip_ref.extractall("alaska_data")
        else:
            print("no update")
    except Exception as e:
        print(f"the error is {e}")
    
def get_health_data():
    try:
        result = requests.get(url, params=params)
        data = result.json()
        healthData = [{"lat":item.get("centroid").get("coordinates")[1], "lon":item.get("centroid").get("coordinates")[0],"name":(item.get("attributes")).get("name")} for item in data]
        return healthData
    except Exception as e:
        print(f"the error is {e}")


def get_internet_data():
    load_data()
    all_geometries = []
    count = 0
    for folder in os.listdir(BASE_FOLDER):
        folder_path = os.path.join(BASE_FOLDER, folder)

        if os.path.isdir(folder_path) and count < 10:
            for file in os.listdir(folder_path):
                if file.endswith(".csv") and count < 10:
                    file_path = os.path.join(folder_path, file)

                    df = pd.read_csv(file_path)

                    if "h3_res8_id" in df.columns and count < 10:
                        for h in df["h3_res8_id"].dropna():
                            coords = h3.cell_to_boundary(h)
                            polygon = Polygon(coords)
                            all_geometries.append(polygon)
                            count+=1


    return gpd.GeoDataFrame(geometry=all_geometries, crs="EPSG:4326").__geo_interface__
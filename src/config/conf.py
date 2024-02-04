FIREBASE_CREDS = "/application/firebase_creds.json"
FIREBASE_URL = "maplemaps-2ab75.appspot.com"

LOCAL_FILE_PATH_BUILDER = "/application/assets"
WORLD_MAPS_FILE_PATH = f"{LOCAL_FILE_PATH_BUILDER}/world_maps"
MAPS_FILE_PATH = f"{LOCAL_FILE_PATH_BUILDER}/maps"
MOBS_FILE_PATH = f"{LOCAL_FILE_PATH_BUILDER}/mobs"
MAP_ASSETS_FILE_PATH = f"{LOCAL_FILE_PATH_BUILDER}/map_assets"

REGION = "GMS"
VERSION = "247"
"""
NOTE override the version for WZ assets - they have not been updated at the same frequency as the general API
"""
WZ_VERSION = "244"

BASE_URL_ENDPOINT_BUILDER = f"https://maplestory.io/api/{REGION}/{VERSION}"
BASE_URL_ENDPOINT_WZ_BUILDER = f"https://maplestory.io/api/wz/img/{REGION}/{WZ_VERSION}"
BASE_URL_ENDPOINT_STORE_BUILDER = f"https://store.maplestory.io/api/json/{REGION}/{VERSION}"

ALL_WORLDMAP_ENDPOINT = f"{BASE_URL_ENDPOINT_BUILDER}/map/worldmap"
ALL_MAP_ENDPOINT = f"{BASE_URL_ENDPOINT_BUILDER}/map"
ALL_MOB_ENDPOINT = f"{BASE_URL_ENDPOINT_BUILDER}/mob"
MAP_ASSETS_ENDPOINT = f"{BASE_URL_ENDPOINT_WZ_BUILDER}/Map/MapHelper.img/worldMap/mapImage"

ALL_WZ_IMAGE_ASSETS_ENDPOINT = f"{BASE_URL_ENDPOINT_STORE_BUILDER}/images.json"
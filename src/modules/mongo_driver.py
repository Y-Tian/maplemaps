import os
from datetime import datetime
import time

from pymongo import MongoClient

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
if not MONGO_CONNECTION_STRING:
    raise Exception(f"MONGO_CONNECTION_STRING is not set! Please set it in your dev_env.vars file...")

MONGO_CLIENT = MongoClient(MONGO_CONNECTION_STRING)

MAP_DATA_DB = MONGO_CLIENT["MapData"]
WORLD_MAPS_COLL = MAP_DATA_DB["world_maps"]
MAP_COLL = MAP_DATA_DB["maps"]
MOB_COLL = MAP_DATA_DB["mobs"]

def generic_push_metadata(target_coll, search_index_payload: dict, all_metadata: dict, upsert=True):
    timestamps = {
        "timestamp": datetime.now(),
        "timestamp_epoch": time.time()
    }

    all_metadata = {**all_metadata, **timestamps}

    target_coll.update_one(search_index_payload, {"$set": all_metadata}, upsert=upsert)
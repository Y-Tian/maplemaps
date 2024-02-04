from modules.mongo_driver import generic_push_metadata, MAP_COLL, MOB_COLL

search_index = {
    "map_id": 450016110
}

maps_cursor = MAP_COLL.find(search_index)
for map_details in maps_cursor:
    map_id = map_details.get("id")

    mob_derived_data = {}

    map_raw_details = map_details.get("raw")

    mobs = map_raw_details.get("mobs")
    for mob in mobs:
        mob_id = mob.get("id")
        mob_details = MOB_COLL.find_one({"mob_id": mob_id})
        mob_raw_details = mob_details.get("raw")

        mob_derived_data[str(mob_id)] = mob_raw_details

    upsert_index = {
        "map_id": map_id
    }

    derived_metadata = {
        "derived": {
            "mobs": mob_derived_data
        }
    }

    new_metadata = {**map_details, **derived_metadata}

    # print(new_metadata.keys())

    generic_push_metadata(MAP_COLL, upsert_index, new_metadata)

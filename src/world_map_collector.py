import requests
import base64

import config.conf as conf
from modules.mongo_driver import generic_push_metadata, WORLD_MAPS_COLL

session = requests.session()

all_world_maps: list = session.get(conf.ALL_WORLDMAP_ENDPOINT).json()
size_all_world_maps = len(all_world_maps)
for index, world_map_id in enumerate(all_world_maps):
    if index % 20 == 0:
        print(f"Processing {index}/{size_all_world_maps}...")

    world_map_details_endpoint = (
        f"{conf.ALL_WORLDMAP_ENDPOINT}/{world_map_id}"
    )

    world_map_details: dict = session.get(world_map_details_endpoint).json()

    parent_world_map_name = world_map_details.get("parentWorld")
    world_map_name = world_map_details.get("worldMapName")
    target_world_map = f"{parent_world_map_name}_{world_map_name}"

    target_file_name_builder = f"{target_world_map}.jpg"

    base_image_payload = world_map_details.get("baseImage")
    if base_image_payload:
        base_image_payload = base_image_payload.pop()
    else:
        print(f"Missing the base image - skipping {target_world_map}...")
        continue

    base64_image_data = base_image_payload.get("image")
    if base64_image_data:
        decoded_image_data = base64.b64decode(base64_image_data)
        size_decoded_image = len(decoded_image_data)

        target_file = f"{conf.WORLD_MAPS_FILE_PATH}/{target_file_name_builder}"
        with open(target_file, "wb") as fw:
            fw.write(decoded_image_data)

        search_index_payload = {"target_file_name_builder": target_file_name_builder}

        # NOTE: regional world maps contain 'links' to area maps - index this for faster reads on the web app
        is_region_map = len(world_map_details.get("links", [])) > 0

        mongo_metadata_payload_builder = {
            "target_file_name_builder": target_file_name_builder,
            "is_region_map": is_region_map,
            "raw": world_map_details,
        }

        """
        NOTE push coordinate data for each map's 'dot' to MongoDB
        """
        generic_push_metadata(
            WORLD_MAPS_COLL, search_index_payload, mongo_metadata_payload_builder
        )
    else:
        print(f"Missing image data - skipping {target_world_map}...")
        continue

print(f"Completed processing {size_all_world_maps} items!")

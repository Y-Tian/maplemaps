import requests
from PIL import Image, ImageDraw, ImageFilter
import os
import sys

import config.conf as conf
from modules.mongo_driver import MAP_COLL, MOB_COLL

session = requests.session()

search_index_payload = {
    # "map_id": 50000
    # "map_id": 450016110
    # "map_id": 450003320
    # "map_id": 327022000
    # "map_id": 450005230
    # "map_id": 306030100
    # "map_id": 220080100
}

maps_detail_cursor = MAP_COLL.find(search_index_payload)
size_of_cursor = maps_detail_cursor.explain().get("executionStats", {}).get("nReturned")

for index, map_details in enumerate(maps_detail_cursor):
    if index % 20 == 0:
        print(f"Processed {index}/{size_of_cursor}...")

    raw_details = map_details.get("raw")

    map_mobs = raw_details.get("mobs")

    # NOTE: ignore non-hunting maps
    if not map_mobs:
        continue

    map_image_local_cache_file_path = map_details.get("target_full_file_path")

    target_full_file_path = map_image_local_cache_file_path.replace("/raw/", "/generated/")
    target_full_file_path = target_full_file_path.lower()
    
    cached_map_render = os.path.isfile(target_full_file_path)
    if cached_map_render:
        # print(f"{target_full_file_path} is already cached!")
        continue

    platform_background_image = Image.open(map_image_local_cache_file_path)
    # NOTE: copy to not override the original cached image
    platform_background_image = platform_background_image.copy()

    curr_platform_background_width, curr_platform_background_height = platform_background_image.size

    # print(f"Curr dimensions: ({curr_platform_background_width},{curr_platform_background_height})")

    minimap_coordinate_system = raw_details.get("miniMap")

    if not minimap_coordinate_system:
        continue
    map_precise_width = minimap_coordinate_system.get("width")
    map_precise_height = minimap_coordinate_system.get("height")

    # print(f"Original dimensions: ({map_precise_width},{map_precise_height})")

    # scale_x = curr_platform_background_width/map_precise_width
    # scale_y = curr_platform_background_height/map_precise_height

    diff_x = (curr_platform_background_width - map_precise_width)
    diff_y = (curr_platform_background_height - map_precise_height)

    # print(f"Diff calculations: ({diff_x},{diff_y})")

    map_precise_center_x = minimap_coordinate_system.get("centerX")
    map_precise_center_y = minimap_coordinate_system.get("centerY")

    # print(f"Original center coords: ({map_precise_center_x},{map_precise_center_y})")

    shifted_center_x = int(map_precise_center_x + diff_x)
    shifted_center_y = int(map_precise_center_y + diff_y)

    # print(f"Shifted center coords: ({shifted_center_x},{shifted_center_y})")

    for map_mob in map_mobs:
        mob_id = map_mob.get("id")

        mob_spawn_x = map_mob.get("x")
        mob_spawn_y = map_mob.get("y")
        
        mob_search_index = {
            "mob_id": mob_id
            # "mob_id": 100000
        }

        mob_details = MOB_COLL.find_one(mob_search_index)
        if not mob_details:
            continue

        mob_image_local_cache_file_path = mob_details.get("target_full_file_path")

        mob_layer_image = Image.open(mob_image_local_cache_file_path)

        mob_width, mob_height = mob_layer_image.size


        """
        NOTE the mob's centerpoint is its top left corner
        - the given spawn point data references the bottom middle of the mob
        """
        # NOTE: works for map_id 450016110
        # precise_mob_spawn_x = int(shifted_center_x + mob_spawn_x - (mob_width))
        # precise_mob_spawn_y = int(shifted_center_y + mob_spawn_y - (mob_height/4))

        # NOTE: works for map_id 306030100, 220080100
        # precise_mob_spawn_x = int(shifted_center_x + mob_spawn_x - (mob_width/2))
        # precise_mob_spawn_y = int(shifted_center_y + mob_spawn_y - (mob_height))

        # NOTE: works for map_id 450003320
        # precise_mob_spawn_x = int(shifted_center_x + mob_spawn_x - (mob_width/2))
        # precise_mob_spawn_y = int(shifted_center_y + mob_spawn_y - (mob_height*0.75))

        # NOTE: generic method
        precise_mob_spawn_x = int(shifted_center_x + mob_spawn_x)
        precise_mob_spawn_y = int(shifted_center_y + mob_spawn_y)

        coordinate_tuple = (precise_mob_spawn_x, precise_mob_spawn_y)

        platform_background_image.paste(mob_layer_image, coordinate_tuple, mob_layer_image.convert('RGBA'))

    os.makedirs(os.path.dirname(target_full_file_path), exist_ok=True)
    platform_background_image.save(target_full_file_path, quality=95)
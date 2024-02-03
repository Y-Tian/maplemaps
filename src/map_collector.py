import config.conf as conf
import os
import requests
from modules.mongo_driver import generic_push_metadata, MAP_COLL


class MapCollector():
    def __init__(self) -> None:
        self.session = requests.session()

    def _dump_raw_map_render(self, map_id: str, map_name: str, street_name: str):
        target_dir_builder = f"raw/{street_name.replace(' ', '_')}"
        # NOTE: non-whitespaced filenames
        target_file_name_builder = f"{map_name.replace(' ', '_')}_{map_id}.png"

        target_full_file_path = f"{conf.MAPS_FILE_PATH}/{target_dir_builder}/{target_file_name_builder}"
        target_full_file_path = target_full_file_path.lower()
        
        cached_map_render = os.path.isfile(target_full_file_path)
        if cached_map_render:
            # print(f"{target_full_file_path} is already cached!")
            return
        
        byte_data = self.session.get(f"{conf.ALL_MAP_ENDPOINT}/{map_id}/render/layer").content
        # NOTE: map doesn't exist
        if len(byte_data) <= 0:
            return

        os.makedirs(os.path.dirname(target_full_file_path), exist_ok=True)
        with open(target_full_file_path, "wb") as fw:
            fw.write(byte_data)

        try:
            raw_map_details = self.session.get(f"{conf.ALL_MAP_ENDPOINT}/{map_id}").json()
        except Exception as e:
            print(f"Exception occurred while trying to get raw map details - {e}")

            return

        search_index_payload = {
            "target_full_file_path": target_full_file_path
        }

        mongo_metadata_payload_builder = {
            "target_full_file_path": target_full_file_path,
            "map_id": map_id,
            "map_name": map_name,
            "map_street_name": street_name,
            "raw": raw_map_details
        }

        generic_push_metadata(
            MAP_COLL, search_index_payload, mongo_metadata_payload_builder
        )

    def cache_all_map_renders(self):
        all_maps_data: list = self.session.get(conf.ALL_MAP_ENDPOINT).json()
        for index, map_data in enumerate(all_maps_data):
            if index % 20 == 0:
                print(f"Processed {index}/{len(all_maps_data)}...")

            map_name = map_data.get("name", "")
            map_street_name = map_data.get("streetName", "")
            map_id = map_data.get("id")

            self._dump_raw_map_render(map_id, map_name, map_street_name)

        # NOTE: dev testing for cfes2
        # self._dump_raw_map_render("Chicken Festival 3", "Lachelein Night Market", "450003320")

mc_client = MapCollector()
mc_client.cache_all_map_renders()
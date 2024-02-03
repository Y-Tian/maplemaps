import config.conf as conf
import os
import sys
import requests

class MapAssetsCollector():
    def __init__(self) -> None:
        self.session = requests.session()
        self.MAX_INT = sys.maxsize

    def _dump_raw_map_asset_render(self, asset_id: str):
        target_dir_builder = f"raw"
        target_file_name_builder = f"{asset_id}.png"

        target_full_file_path = f"{conf.MAP_ASSETS_FILE_PATH}/{target_dir_builder}/{target_file_name_builder}"
        target_full_file_path = target_full_file_path.lower()
        
        cached_map_render = os.path.isfile(target_full_file_path)
        if cached_map_render:
            # print(f"{target_full_file_path} is already cached!")
            return
        
        res = self.session.get(f"{conf.MAP_ASSETS_ENDPOINT}/{asset_id}")
        if res.status_code == 404:
            raise Exception(f"Out of map assets! Current index at {asset_id}")

        byte_data = res.content

        # NOTE: map doesn't exist
        if len(byte_data) <= 0:
            return

        os.makedirs(os.path.dirname(target_full_file_path), exist_ok=True)
        with open(target_full_file_path, "wb") as fw:
            fw.write(byte_data)

    def cache_all_map_assets_renders(self):
        """
        NOTE indexing for wz map assets is not known 
        - loop from 0 to MAX_INT until it throws a HTTP 404
        """
        for index in range(self.MAX_INT):
            if index % 20 == 0:
                print(f"Processed {index} items...")

            self._dump_raw_map_asset_render(f"{index}")

mac_client = MapAssetsCollector()
mac_client.cache_all_map_assets_renders()
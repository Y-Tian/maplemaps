import config.conf as conf
import os
import requests
from modules.mongo_driver import generic_push_metadata, MAP_COLL, MOB_COLL


class MobCollector():
    def __init__(self) -> None:
        self.session = requests.session()

    def _dump_raw_mob_render(self, mob_id: str):
        target_dir_builder = "raw"
        # NOTE: non-whitespaced filenames
        target_file_name_builder = f"{mob_id}.png"

        target_full_file_path = f"{conf.MOBS_FILE_PATH}/{target_dir_builder}/{target_file_name_builder}"
        target_full_file_path = target_full_file_path.lower()
        
        cached_mob_render = os.path.isfile(target_full_file_path)
        if cached_mob_render:
            return
        
        """
        NOTE /render/stand shows an animated version of the mob
        """
        # byte_data = self.session.get(f"{conf.ALL_MOB_ENDPOINT}/{mob_id}/render/stand").content
        byte_data = self.session.get(f"{conf.ALL_MOB_ENDPOINT}/{mob_id}/icon").content
        # NOTE: map doesn't exist
        if len(byte_data) <= 0:
            return

        os.makedirs(os.path.dirname(target_full_file_path), exist_ok=True)
        with open(target_full_file_path, "wb") as fw:
            fw.write(byte_data)

        try:
            raw_mob_details = self.session.get(f"{conf.ALL_MOB_ENDPOINT}/{mob_id}").json()
        except Exception as e:
            print(f"Exception occurred while trying to get raw map details - {e}")

            return

        search_index_payload = {
            "mob_id": mob_id
        }

        mongo_metadata_payload_builder = {
            "mob_id": mob_id,
            "raw": raw_mob_details
        }

        generic_push_metadata(
            MOB_COLL, search_index_payload, mongo_metadata_payload_builder
        )

    def cache_required_mob_renders(self):
        search_index_payload = {}

        maps_detail_cursor = MAP_COLL.find(search_index_payload)
        size_of_cursor = maps_detail_cursor.explain().get("executionStats", {}).get("nReturned")

        for index, map_details in enumerate(maps_detail_cursor):
            if index % 20 == 0:
                print(f"Processed {index}/{size_of_cursor}...")

            raw_details = map_details.get("raw")

            map_mobs = raw_details.get("mobs")

            for map_mob in map_mobs:
                mob_id = map_mob.get("id")

                self._dump_raw_mob_render(mob_id)


mc_client = MobCollector()
mc_client.cache_required_mob_renders()
import os
import time
import requests


class Translation:

    unique_id_to_return_single_map = {}

    def __init__(
        self,
        url=os.getenv("TRANSLATION_URL"),
        username=os.getenv("TRANSLATION_USERNAME"),
        password=os.getenv("TRANSLATION_PASSWORD"),
    ):
        self.url = url.replace("/sync", "/async")
        self.result_url = url.replace("/sync", "/result")
        self.username = username
        self.password = password

    def run(self, in_texts):
        return_single = False

        if isinstance(in_texts, str):
            in_texts = [in_texts]
            return_single = True

        unique_id = requests.post(
            self.url, json={"data": in_texts}, auth=(self.username, self.password)
        ).json()["unique_id"]
        self.unique_id_to_return_single_map[unique_id] = return_single

        return unique_id

    def get_result(self, unique_id):
        while True:
            result = requests.post(
                self.result_url,
                json={"unique_id": unique_id},
                auth=(self.username, self.password),
            ).json()
            if result.get("prediction"):
                if self.unique_id_to_return_single_map[unique_id]:
                    del self.unique_id_to_return_single_map[unique_id]
                    return result["prediction"][0]

                return result["prediction"]

            time.sleep(1)

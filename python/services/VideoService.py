import os
import requests
import json
from utils.Logger import logger

class VideoService:
    def __init__(self, base_url, app_token):
        self.base_url = base_url
        self.app_token = app_token

    def get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "X-App-Token": self.app_token,
        }
        return headers

    def get_videos(self):
        # TODO: conseguir a lista de ids de videos para transcrição
        return [3487]

    def get_videos_url(self, ids):
        logger.info(f"Getting video url for video ids={ids}...")
        url = f"{self.base_url}/bot/get-urls"
        payload = json.dumps({"ids": ids})
        headers = self.get_headers()

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 201:
            logger.info(f"Got video url for video ids={ids}")
            return response.json()
        else:
            logger.error(f"Error getting video url for video ids={ids}")
            return None

    def download_video(self, url, file_name):
        logger.info(f"Downloading {file_name}...")

        try:
            # Adicionar timeout para evitar travamento indefinido
            response = requests.get(url, allow_redirects=True, timeout=30)

            # Check for status code and content length
            if response.status_code != 200:
                logger.error(f"Failed to download {file_name}. HTTP Status Code: {response.status_code}")
                return False
            
            if not response.content:
                logger.error(f"Failed to download {file_name}. No content received.")
                return False

            file_path = f"./temp/videos/{file_name}"
            with open(file_path, "wb") as file:
                file.write(response.content)

            logger.info(f"Downloaded {file_name}!")  # Usar info em vez de log

            return True

        except requests.Timeout:
            logger.error(f"Timeout while downloading {file_name}")
            return False

        except requests.RequestException as e:
            logger.error(f"RequestException while downloading {file_name}: {str(e)}")
            return False

        except Exception as e:
            logger.error(f"Unexpected error while downloading {file_name}: {str(e)}")
            return False

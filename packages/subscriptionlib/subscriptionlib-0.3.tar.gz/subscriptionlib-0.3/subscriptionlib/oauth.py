from logger import logger
import requests


class Oauth:
    def __init__(self, domain_url, client_id, client_secret):
        self.domain_url = domain_url
        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_token(self, refresh_token="1000.0ab3bd344147e2cf2b8d4640e2dc5bd9.7960cc1247b0ff6f995a0581e45df40a"):
        logger.info("Calling API to get access token using refresh token {}".format(refresh_token))
        url = self.domain_url
        data = {
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": url,
            "grant_type": "refresh_token"
        }

        request = requests.post(url, data)
        logger.info("API request's result {}".format(request.json()))
        return request.json()

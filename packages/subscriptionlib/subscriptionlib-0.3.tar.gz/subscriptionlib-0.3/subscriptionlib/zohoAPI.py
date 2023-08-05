import requests

from logger import logger


class ZohoAPI:
    def __init__(self, url, auth_token, org_id):
        self.auth_token = auth_token
        self.org_id = org_id
        self.url = url

    def get_customers(self):
        logger.info("Retrieving all customers")
        url = self.url
        headers = {
            "Authorization": "Zoho-oauthtoken " + self.auth_token,
            "X-com-zoho-subscriptions-organizationid": self.org_id,
            "Content-Type": "application/json;charset=UTF-8"
        }
        request = requests.get(url, headers=headers)

        logger.info("The customers {}".format(request.json()))

        return request.json()

    def get_customer(self, customer_id):
        logger.info("Retrieving customer with id: {}".format(customer_id))
        url = self.url + customer_id
        headers = {
            "Authorization": "Zoho-oauthtoken " + self.auth_token,
            "X-com-zoho-subscriptions-organizationid": self.org_id,
            "Content-Type": "application/json;charset=UTF-8"
        }
        request = requests.get(url, headers=headers)

        logger.info("The customer {}".format(request.json()))

        return request.json()

    def get_customer_active_subscription(self, customer_id):
        logger.info("Retrieving customer {} subscriptions".format(customer_id))
        url = self.url+'?filter_by=SubscriptionStatus.ACTIVE&customer_id='+customer_id
        print(url)
        headers = {
            "Authorization": "Zoho-oauthtoken " + self.auth_token,
            "X-com-zoho-subscriptions-organizationid": self.org_id,
            "Content-Type": "application/json;charset=UTF-8"
        }
        request = requests.get(url, headers=headers)
        logger.info("The subscriptions {}".format(request.json()))

        return request.json()

import json

import constant
import oauth
import zohoAPI


if __name__ == '__main__':
    # Instantiate authentication object
    auth = oauth.Oauth(domain_url=constant.OAUTH2_URI + constant.OAUTH2_ENDPOINT,
                       client_id=constant.CLIENT_ID,
                       client_secret=constant.CLIENT_SECRET)

    # Refresh the access token
    auth_response = auth.get_access_token()

    # Instantiate the zoho object
    zohoCust = zohoAPI.ZohoAPI(url=constant.CUSTOMER_ENDPOINT,
                               auth_token=auth_response.get("access_token"),
                               org_id=constant.ORGANIZATION_ID)

    zohoSub = zohoAPI.ZohoAPI(url=constant.SUB_ENDPOINT,
                              auth_token=auth_response.get('access_token'),
                              org_id=constant.ORGANIZATION_ID)


    # Retrieving the customer id and the license from the configuration file
    def read_config(file_path):
        with open(file_path, 'r') as f:
            config = json.load(f)

        return config

    
    customer_id = read_config('config.json').get('customer_id')
    license = read_config('config.json').get('license')

    # Calling the Zoho API to get our customer
    customer = zohoCust.get_customer(customer_id).get('customer')
    subscriptions = zohoSub.get_customer_active_subscription(customer_id)


    # Verifying that the customer has the matching license key
    def verify_customer():
        if customer.get("cf_license") == license:
            return True

        return False


    # Verifying that the customer has an active subscription
    def verify_subscription():
        if len(subscriptions.get('subscriptions')) > 0:
            return True

        return False


    print(customer)
    print(subscriptions)
    print(auth_response)
    if verify_subscription() and verify_customer():
        print(True)
    else:
        print(False)

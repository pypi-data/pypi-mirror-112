from google.cloud import bigquery
import os, json


class BigquerySource(object):
    ABSPATH = os.path.abspath(__file__)
    BASE_AUTH_DIR = os.path.dirname(ABSPATH) # auth/
    BASE_BASES_DIR = os.path.dirname(BASE_AUTH_DIR) # bases/
    SERVICES_ACCOUNT_CREDS_DIR = os.path.join(
            os.path.join(BASE_BASES_DIR, 'secrets'), 'service_account_credentials')
    
    # Constructor to ge credential information to create instances of the class
    def __init__(self,
                    path=None, # "personal_bq.json"
                    json_credential= None
                ):
        """
        path Optional (Default: None): json filename path with the service account credential if exists.
            e.g: "filename_path.json"
        json_credential (Default: Empty dict): An object containing the service account credential.
        Return: Instance of the GCP client required
        """
        self.path = path
        self.json_credential = json_credential
        self.client = None


        if self.path is not None:
            creds_path = os.path.join(self.SERVICES_ACCOUNT_CREDS_DIR, path)
            #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
            self.client = bigquery.Client.from_service_account_json(creds_path)
            print("Checking credential...", self.client)
        elif self.json_credential is not None:
            print("Checking credential...", self.client)
            tmp_creds_path = os.path.join(self.SERVICES_ACCOUNT_CREDS_DIR, "tmp_cred.json")
            #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
            try:
                with open(tmp_creds_path, 'w') as f:
                    f.write(json.dumps(self.json_credential, indent=4))
            except Exception as err:
                print(err)

            self.client = bigquery.Client.from_service_account_json(tmp_creds_path)
            print("We have received json credential. Pending to check it out...", self.client)

            if (isinstance, self.client):
                os.remove(tmp_creds_path)
                print("We have deleted json credential.", self.client)


if __name__ == "__main__":
    #personal_obj =  BigquerySource()
    pass
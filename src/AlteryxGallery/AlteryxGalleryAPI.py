from math import log
from typing import Dict, Any, Tuple
import httpx
import time
import logging
import logging.config


# Set up logging
# Set the logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')

# Create logger instance
logging.config.fileConfig('logging.conf')
# logging.basicConfig(level=logging.INFO)  # Adjust the log level as needed
logger = logging.getLogger(__name__)

class GalleryClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.http_client = httpx.Client()
        self.token = None
        self.token_expiry = None

    def authenticate(self, client_id: str, client_secret: str) -> bool:
        logger.info("Authenticating user...")
        auth_response = self.http_client.post(
            f"{self.base_url}/oauth2/token",
            data={"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"},
        )
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            self.token = auth_data.get("access_token")
            logger.debug(f"Token received at: {time.time()}")
            self.token_expiry = time.time() + auth_data.get("expires_in")
            self.client_id = client_id  # Store username
            self.client_secret = client_secret  # Store password
            logger.info("Authentication successful.")
            return True
        else:
            logger.error("Authentication failed.")
            return False

    def _ensure_authenticated(self) -> None:
        if not self.token or time.time() > self.token_expiry - 60:
            logger.info("Token is expired or about to expire. Renewing token...")
            if not self.authenticate(self.client_id, self.client_secret):
                raise Exception("Authentication failed")

    def _update_auth_header(self) -> None:
        self._ensure_authenticated()
        self.http_client.headers.update({"Authorization": f"Bearer {self.token}"})
        logger.debug("Authorization header updated with the token.")

    def _get(self, endpoint: str, params: Dict[str, Any] =None) -> Tuple[httpx.Response, Dict[str, Any]]:
        self._update_auth_header()
        logger.info(f"Making GET request to endpoint: {endpoint}")
        response = self.http_client.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        logger.debug("GET request successful.")
        return response, response.json()

    def get_data(self) -> dict:
        return self._get("data")

    def close(self) -> None:
        self.http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


    # Workflow Interaction Methods
    def get_all_workflows(self, **kwargs) -> Tuple[httpx.Response, Dict[str, Any]]:
        logger.info("Getting all workflows...")
        return self._get("v3/workflows", params=kwargs)
    

    # # Example usage:
# with AlteryxGalleryClient("https://your-alteryx-server/api/v3") as client:
#     if client.authenticate("your_username", "your_password"):
#         logger.info("Authentication successful!")
#         print(client.get_data())
#     else:
#         logger.error("Authentication failed!")


# TODO: Implement the following methods following the requirements of the Alteryx Gallery API
    # def subscription(self):
    #     """
    #     :return: workflows in a subscription
    #     """
    #     method = 'GET'
    #     url = self.api_location + '/workflows/subscription/'
    #     params = self.build_oauth_params()
    #     signature = self.generate_signature(method, url, params)
    #     params.update({'oauth_signature': signature})
    #     output = requests.get(url, params=params)
    #     output, output_content = output, json.loads(output.content.decode("utf8"))
    #     return output, output_content

    # def questions(self, app_id):
    #     """
    #     :return: Returns the questions for the given Alteryx Analytics App
    #     """
    #     method = 'GET'
    #     url = self.api_location + '/workflows/' + app_id + '/questions/'
    #     params = self.build_oauth_params()
    #     signature = self.generate_signature(method, url, params)
    #     params.update({'oauth_signature': signature})
    #     output = requests.get(url, params=params)
    #     output, output_content = output, json.loads(output.content.decode("utf8"))
    #     return output, output_content

    # def execute_workflow(self, app_id, **kwargs):
    #     """
    #     Queue an app execution job.
    #     :return:  Returns ID of the job
    #     """
    #     method = 'POST'
    #     url = self.api_location + '/workflows/' + app_id + '/jobs/'
    #     params = self.build_oauth_params()
    #     signature = self.generate_signature(method, url, params)
    #     params.update({'oauth_signature': signature})

    #     if 'payload' in kwargs:
    #         output = requests.post(url,
    #                                json=kwargs['payload'],
    #                                headers={'Content-Type': 'application/json'},
    #                                params=params)
    #     else:
    #         output = requests.post(url, params=params)

    #     output, output_content = output, json.loads(output.content.decode("utf8"))
    #     return output, output_content

    # def get_jobs(self, app_id):
    #     """
    #     :return: Returns the jobs for the given Alteryx Analytics App
    #     """
    #     method = 'GET'
    #     url = self.api_location + '/workflows/' + app_id + '/jobs/'
    #     params = self.build_oauth_params()
    #     signature = self.generate_signature(method, url, params)
    #     params.update({'oauth_signature': signature})
    #     output = requests.get(url, params=params)
    #     output, output_content = output, json.loads(output.content.decode("utf8"))
    #     return output, output_content

    # def get_job_status(self, job_id):
    #     """
    #     :return: Retrieves the job and its current state
    #     """
    #     method = 'GET'
    #     url = self.api_location + '/jobs/' + job_id + '/'
    #     params = self.build_oauth_params()
    #     signature = self.generate_signature(method, url, params)
    #     params.update({'oauth_signature': signature})
    #     output = requests.get(url, params=params)
    #     output, output_content = output, json.loads(output.content.decode("utf8"))
    #     return output, output_content

    # def get_job_output(self, job_id, output_id):
    #     """
    #     :return: Returns the output for a given job (FileURL)
    #     """
    #     method = 'GET'
    #     url = self.api_location + '/jobs/' + job_id + '/output/' + output_id + '/'
    #     params = self.build_oauth_params()
    #     signature = self.generate_signature(method, url, params)
    #     params.update({'oauth_signature': signature})
    #     output = requests.get(url, params=params)
    #     output, output_content = output, output.content.decode("utf8")
    #     return output, output_content

    # def get_app(self, app_id, app_name):
    #         """
    #         Retrieves the requested App from the Alteryx Gallery API and saves it to disk.

    #         :param app_id: The ID of the App to retrieve.
    #         :param app_name: The name of the App to save the file as.
    #         :return: The file path where the App is saved.
    #         """
    #         method = 'GET'
    #         url = self.api_location + '/admin/v1/' + app_id + '/package/'
    #         params = self.build_oauth_params()
    #         signature = self.generate_signature(method, url, params)
    #         params.update({'oauth_signature': signature})
    #         output = requests.get(url, params=params)
    #         output_content = output.content

    #         # Define the path and file name for the downloaded file
    #         # Save it in the 'workflow' directory
    #         file_path = f"{app_name}.yxzp"

    #         # Write the content to a file
    #         with open(file_path, 'wb') as file:
    #             file.write(output_content)
            
    #         # Optionally return the file_path if needed
    #         return file_path

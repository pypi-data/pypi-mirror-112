from dotenv import load_dotenv
import os
load_dotenv()

load_dotenv(verbose=True)

LOCAL_INFO = {
    "offline_filepath": os.getenv("LOCAL_INFO_OFFLINE_FILEPATH")
}

SERVER_CREDENTIALS = {
    "url": os.getenv("SERVER_CREDENTIALS_URL"),
}

CLIENT_CREDENTIALS = {
    "client_name": os.getenv("CLIENT_CREDENTIALS_CLIENT_NAME"),
    "app_name": os.getenv("CLIENT_CREDENTIALS_APP_NAME"),
}


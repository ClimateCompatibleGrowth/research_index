import os
from dotenv import load_dotenv


class Settings:
    load_dotenv()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._init_instance()
        return cls._instance

    def _init_instance(self):
        self.MG_HOST = os.getenv("MG_HOST")
        self.MG_PORT = os.getenv("MG_PORT")
        self.MG_PORT_ALT = os.getenv("MG_PORT_ALT")
        self.MG_USER = os.getenv("MG_USER")
        self.MG_PASS = os.getenv("MG_PASS")


settings = Settings()

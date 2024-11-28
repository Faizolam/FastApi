# from dotenv import find_dotenv, load_dotenv
# from pydantic_settings import BaseSettings
# import os
# # load_dotenv(find_dotenv(".env"))
# load_dotenv()
# DATABASE_HOSTNAME=os.getenv("DATABASE_HOSTNAME")
# print(DATABASE_HOSTNAME)

# class Setting(BaseSettings):
#     DATABASE_HOSTNAME:str=DATABASE_HOSTNAME

#     class confing:
#         env_file = ".env"

# settings = Setting()
# print(settings.DATABASE_HOSTNAME)

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    DATABASE_HOSTNAME:str
    DATABASE_PORT:str
    DATABASE_PASSWORD:str
    DATABASE_NAME:str
    DATABASE_NAME_TEST: str
    DATABASE_USERNAME:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int

    model_config = SettingsConfigDict(env_file=DOTENV)

settings = Settings()
print(settings.DATABASE_NAME_TEST)

# class PytestSettings(Settings):
#     DATABASE_NAME_TEST:str = "default_test"

# pytestSettings = PytestSettings()
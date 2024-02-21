# from dotenv import find_dotenv, load_dotenv
# from pydantic_settings import BaseSettings
# import os
# # load_dotenv(find_dotenv(".env"))
# load_dotenv()
# DATABASE_HOSTNAME=os.getenv("DATABASE_HOSTNAME")
# # print(DATABASE_HOSTNAME)
# # print(os.getenv("DATABSAE_URL"))

# class Setting(BaseSettings):
#     DATABASE_HOSTNAME:str

#     class confing:
#         env_file = ".env"

# settings = Setting()
# print(settings.DATABASE_HOSTNAME)

{
    "content": "something something beaches",
    "title": "top beaches in florida",
    "created_at": "2024-02-08T17:06:38.699439+05:30",
    "published": true,
    "id": 7,
    "owner_id": 9
}

{
        "title": "Whale Cave Inn",
        "content": "Nestled in a small traditional village in the heart of the picturesque countryside, the Whale Cave Inn offers a blend of luxury and coziness. Experience nature’s beauty while enjoying top-of-the-range service.",
        "published": true,
        "id": 11,
        "created_at": "2024-02-10T08:22:34.509942+05:30",
        "owner_id": 9,
        "owner": {
            "id": 9,
            "email": "olam@gmail.com",
            "created_at": "2024-01-08T13:16:27.855336+05:30"
        },
        "votes": 2
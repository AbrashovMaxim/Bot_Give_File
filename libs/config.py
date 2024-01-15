import yaml
import re

from typing import Union

class Config:
    def __init__(self) -> None:
        try:
            with open("config.yaml", "r", encoding="UTF-8") as f:
                self.data = yaml.safe_load(f)
                print("[CONFIG] Configuration file loaded - successfully!")
        except:
            self.data = {
                "BOTConfig": {
                    "TOKEN": "TOKEN_BOT",
                    "BOTChannel": "ID_COMMON_CHANNEL_BOT",
                    "URLChannel": "https://t.me/URL_CHANNEL_BOT/",
                    "NAMEFile": "FILE_NAME.pdf"
                },
                "Channels": {
                    0: {
                        "URLChannel": "https://t.me/URL_CHANNEL/",
                        "NAMEChannel": "NAME_CHANNEL",
                        "IDChannel": "ID_CHANNEL"
                    }
                }
            }
            with open("config.yaml", "w", encoding="UTF-8") as f:
                yaml.dump(self.data, f, default_flow_style=False, encoding='UTF-8')
            print("[CONFIG] Change configuration file - config.yaml!")
            exit(1)
        self.check_config()
    
    def check_config(self) -> None:
        try:
            if not(re.search("^[0-9]*:[a-zA-Z0-9_-]*$", self.data["BOTConfig"]["TOKEN"])):
                print(f"[CONFIG] Check TOKEN in BOTConfig")
                exit(1)
            
            if not(re.search("^[( ,.)а-яА-Яa-zA-Z0-9_-]*.[( ,.)а-яА-Яa-zA-Z0-9_-]*$", self.data["BOTConfig"]["NAMEFile"])):
                print(f"[CONFIG] Check NAMEFile in BOTConfig")
                exit(1)

            if not(check_int(self.data["BOTConfig"]["BOTChannel"])):
                print(f"[CONFIG] Check BOTChannel in BOTConfig")
                exit(1)

            for i in self.data["Channels"]:
                if not(self.data["Channels"][i]["IDChannel"]):
                    print(f"[CONFIG] Check IDChannel in Channels.{i}.IDChannel")
                    exit(1)

                if self.data["Channels"][i]["NAMEChannel"] == "":
                    print(f"[CONFIG] Check IDChannel in Channels.{i}.NAMEChannel")
                    exit(1)

        except Exception as e:
                print(f"[CONFIG] Problems in configuration file!\n{e}")
                exit(1)
    
    def get_token(self) -> str:
        return self.data["BOTConfig"]["TOKEN"]
    
    def get_channel(self) -> int:
        return self.data["BOTConfig"]["BOTChannel"]
    
    def get_url(self) -> str:
        return self.data["BOTConfig"]["URLChannel"]
    
    def get_file(self) -> str:
        return self.data["BOTConfig"]["NAMEFile"]
    
    def get_channels(self) -> dict:
        channels = {}
        for i in self.data["Channels"]:
            channels[self.data["Channels"][i]["IDChannel"]] = {
                "Name": self.data["Channels"][i]["NAMEChannel"],
                "Url": self.data["Channels"][i]["URLChannel"]
            }
        return channels
    
def check_int(value: Union[str, int]) -> bool:
    try: 
        _temp = int(value)
        return True
    except:
        return False

config = Config()
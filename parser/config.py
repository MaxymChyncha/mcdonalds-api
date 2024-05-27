import configparser

config = configparser.ConfigParser()
config.read("config.ini")

FILE_PATH = config.get("paths", "menu_file_dir")
MENU_FILE_NAME = "mcdonalds.json"

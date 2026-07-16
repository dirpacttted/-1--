import yaml
from dbmanager import DatabaseManager


def load_config():
	with open("config.yaml", "r", encoding="utf-8") as file:
			return yaml.safe_load(file)


def main():
	config = load_config()

	db = DatabaseManager(config["database"])

	db.connect()
	
	db.check_database_structure()

	db.close()


if __name__ == "__main__":
	main()
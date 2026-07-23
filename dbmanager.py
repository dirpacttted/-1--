import os
import mysql.connector

class DatabaseManager:
    def __init__(self, logger):
        self.logger = logger
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            port=int(os.getenv("DATABASE_PORT")),
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME"),
        )

        self.cursor = self.connection.cursor()

        self.logger.info("Подключение к базе данных выполнено")

    def check_database_structure(self):
        required_tables = [
            "configurations",
            "configurationversions",
            "metadataobjects",
            "dataseparationsettings",
        ]

        self.cursor.execute("SHOW TABLES")
        existing_tables = [table[0].lower() for table in self.cursor.fetchall()]

        if all(table in existing_tables for table in required_tables):
            self.logger.info("Структура базы данных проверена")
            return

        self.logger.info("Создание структуры базы данных...")

        with open("schema.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        commands = sql_script.split(";")

        for command in commands:
            if command.strip():
                self.cursor.execute(command)

        self.connection.commit()

        self.logger.info("Структура базы данных создана")

    def insert_configuration(self, configuration_data):
        insert_query = """
            INSERT INTO Configurations (name, synonym, default_download_path)
            VALUES (%s, %s, %s)
        """

        self.cursor.execute(insert_query, configuration_data)
        self.connection.commit()

        self.logger.info(f"Конфигурация '{configuration_data[0]}' сохранена")

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

            self.logger.info("Соединение с базой данных закрыто")
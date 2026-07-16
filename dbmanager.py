import mysql.connector


class DatabaseManager:

    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"]
        )

        self.cursor = self.connection.cursor()

        print("Подключение к базе данных выполнено.")

    def check_database_structure(self):

        required_tables = [
            "configurations",
            "configurationversions",
            "metadataobjects",
            "dataseparationsettings"
        ]

        self.cursor.execute("SHOW TABLES")

        existing_tables = [table[0] for table in self.cursor.fetchall()]

        if all(table in existing_tables for table in required_tables):
            print("Структура базы данных соответствует.")
        else:
            print("Структура отсутствует. Создаём таблицы...")

            with open("schema.sql", "r", encoding="utf-8") as file:
                sql_script = file.read()

            commands = sql_script.split(";")

            for command in commands:
                if command.strip():
                    self.cursor.execute(command)

            self.connection.commit()

            print("Структура создана.")

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

            print("Соединение с базой данных закрыто.")
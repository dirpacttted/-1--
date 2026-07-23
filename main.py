from logging import root
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from dbmanager import DatabaseManager
from logger import logger
from pathlib import Path


MDO_ROOT = Path("./SSL/src")

def find_mdo_files(directory: Path):
    """
    Поиск всех .mdo файлов внутри директории
    """
    return directory.rglob("*.mdo")


def process_mdo_file(file_path: Path):
    """
    Обработка одного MDO файла
    """
    logger.info(f"Загрузка файла: {file_path}")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        logger.info(f"Файл успешно загружен: {file_path.name}")

        processed = 0

        for child in root:
            if child.tag == "chartsOfCharacteristicTypes":
                logger.info(
                    f"Обрабатывается раздел {child.tag} "
                    f"из файла {file_path.name}"
                )

                processed += 1

        logger.info(
            f"В файле {file_path.name} обработано объектов: {processed}"
        )

        return processed

    except ET.ParseError as e:
        logger.error(
            f"Ошибка парсинга XML {file_path}: {e}"
        )

    except Exception as e:
        logger.exception(
            f"Ошибка обработки файла {file_path}: {e}"
        )

    return 0

def main():
    load_dotenv(dotenv_path=".env")
    logger.info("Переменные окружения загружены")

    db = DatabaseManager(logger)

    db.connect()
    db.check_database_structure()

    logger.info("Загрузка файла Configuration.mdo...")

    tree = ET.parse("./SSL/src/Configuration/Configuration.mdo")
    root = tree.getroot()

    logger.info("Конфигурация успешно загружена")

    total_processed = 0

    for child in root:
        if child.tag == "chartsOfCharacteristicTypes":
            logger.info(
                f"Обрабатывается раздел: {child.tag}"
            )

            total_processed += 1

    logger.info(
        f"Обработано объектов: {total_processed}"
    )
    logger.info(f"Поиск MDO файлов в {MDO_ROOT}")
    files_count = 0
    total_processed = 0
    for mdo_file in find_mdo_files(MDO_ROOT):
        files_count += 1
        logger.info(
						f"[{files_count}] Найден файл: {mdo_file}"
				)
        total_processed += process_mdo_file(mdo_file)
    logger.info(
				f"Всего найдено файлов: {files_count}"
		)
    logger.info(
				f"Всего обработано объектов: {total_processed}"
		)

    db.close()

    logger.info("Работа завершена")


if __name__ == "__main__":
    main()
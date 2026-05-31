import json


def json_to_dict_list(filename: str) -> list[dict]:
    """
    Читает JSON-файл и возвращает список словарей.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (TypeError, ValueError, IOError) as error:
        print(f"Ошибка при чтении JSON-файла: {error}")
        return []


def dict_list_to_json(dict_list: list[dict], filename: str) -> bool:
    """
    Сохраняет список словарей в JSON-файл.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(dict_list, file, ensure_ascii=False, indent=4)
        return True
    except (TypeError, ValueError, IOError) as error:
        print(f"Ошибка при записи JSON-файла: {error}")
        return False
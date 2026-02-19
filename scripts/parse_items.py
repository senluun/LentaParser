"""
Скрипт для парсинга JSON файла с товарами из каталога Ленты.

Этот модуль извлекает из полного JSON ответа API только необходимые поля:
- ID товара
- Название
- Обычная цена
- Промо цена
- Бренд
- Количество в наличии
- Доступность

Поддерживает фильтрацию только товаров в наличии.
Результат сохраняется в файл parsed_items.json.
"""

import json
import os
from pathlib import Path

# Определяем путь к корневой папке проекта (на уровень выше scripts/)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Создаем папку data, если её нет
DATA_DIR.mkdir(exist_ok=True)

def parse_spb_result(json_file, only_in_stock=True):
    """
    Парсит JSON файл с товарами и извлекает необходимые данные.
    
    Args:
        json_file (str): Путь к JSON файлу с данными каталога
        only_in_stock (bool): Если True, возвращает только товары в наличии (count > 0)
    
    Returns:
        list: Список словарей с распарсенными данными товаров
    """
    # Открываем и читаем JSON файл
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    parsed_items = []
    
    # Проходим по всем товарам в массиве 'items'
    for item in data.get('items', []):
        count = item.get('count', 0)
        
        # Пропускаем товары не в наличии, если включен фильтр
        if only_in_stock and count == 0:
            continue
        
        # Формируем упрощенную структуру данных товара
        parsed_item = {
            'id': item.get('id'),                                      # Уникальный ID товара
            'name': item.get('name'),                                  # Название товара
            'regular_price': item.get('prices', {}).get('priceRegular'),  # Обычная цена
            'promo_price': item.get('prices', {}).get('price'),        # Промо цена (если есть)
            'brand': extract_brand(item),                              # Бренд (извлекается из названия)
            'in_stock': count,                                         # Количество в наличии
            'available': count > 0                                     # Флаг доступности
        }
        parsed_items.append(parsed_item)
    
    return parsed_items


def extract_brand(item):
    """
    Извлекает бренд из названия товара.
    
    Бренд обычно указывается в верхнем регистре в начале названия товара.
    Функция ищет первое слово полностью в верхнем регистре длиной больше 1 символа.
    
    Args:
        item (dict): Словарь с данными товара
    
    Returns:
        str or None: Название бренда или None, если не найден
    """
    name = item.get('name', '')
    words = name.split()
    
    # Ищем первое слово в верхнем регистре (обычно это бренд)
    for word in words:
        if word.isupper() and len(word) > 1:
            return word
    return None


def save_to_json(data, output_file):
    """
    Сохраняет данные в JSON файл с красивым форматированием.
    
    Args:
        data (list or dict): Данные для сохранения
        output_file (str or Path): Путь к выходному файлу
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Данные сохранены в {output_file}")


if __name__ == "__main__":
    # Список файлов для обработки
    files_to_process = [
        {
            "input": DATA_DIR / "spb_result.json",      # СПб данные
            "output": DATA_DIR / "parsed_spb_items.json",
            "name": "Санкт-Петербург"
        },
        {
            "input": DATA_DIR / "msk_results.json",        # Москва данные
            "output": DATA_DIR / "parsed_msk_items.json",
            "name": "Москва"
        }
    ]
    
    total_processed = 0
    
    # Обрабатываем каждый файл
    for file_info in files_to_process:
        input_file = file_info["input"]
        output_file = file_info["output"]
        city_name = file_info["name"]
        
        # Проверяем существование входного файла
        if not input_file.exists():
            print(f" Файл {input_file} не найден, пропускаем {city_name}")
            continue
        
        print(f"\n=== Обработка данных для города: {city_name} ===")
        
        # Парсим данные
        # only_in_stock=True - только товары в наличии
        # only_in_stock=False - все товары (включая отсутствующие)
        parsed_data = parse_spb_result(input_file, only_in_stock=True)
        
        # Сохраняем результат
        save_to_json(parsed_data, output_file)
        
        # Выводим статистику
        in_stock_count = sum(1 for item in parsed_data if item['available'])
        print(f"Обработано товаров: {len(parsed_data)}")
        print(f"В наличии: {in_stock_count}")
        
        total_processed += len(parsed_data)
    
    print(f"\n=== Итого обработано товаров: {total_processed} ===")

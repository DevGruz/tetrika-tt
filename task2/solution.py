import asyncio
import csv
import string
import time
from collections import defaultdict

import httpx
from bs4 import BeautifulSoup


async def fetch_page(client, url):
    response = await client.get(url)
    response.raise_for_status()
    return response.text


async def parse_animals_from_page(client, base_url, letter):
    url = f"{base_url}/w/index.php?title=Категория:Животные_по_алфавиту&from={letter}"
    total_count = 0

    while url:
        html = await fetch_page(client, url)
        soup = BeautifulSoup(html, "html.parser")

        category_container = soup.find("div", class_="mw-category mw-category-columns")
        if not category_container:
            break

        category_groups = category_container.find_all("div", class_="mw-category-group")

        for group in category_groups:
            ul = group.find("ul")
            h3 = group.find("h3")
            if ul and h3 and letter == h3.text.strip():
                total_count += len(ul.find_all("li"))
            else:
                return letter, total_count

        next_link = soup.find("a", string="Следующая страница")
        url = f"{base_url}{next_link['href']}" if next_link else None

    return letter, total_count


async def scrape_animals_by_letter():
    base_url = "https://ru.wikipedia.org"
    alphabet = tuple("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ") + tuple(string.ascii_uppercase)
    animals_count = defaultdict(int)

    async with httpx.AsyncClient() as client:
        tasks = (
            parse_animals_from_page(client, base_url, letter) for letter in alphabet
        )
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for letter, result in results:
        if isinstance(result, Exception):
            print(f"Ошибка при обработке буквы {letter}: {result}")
            continue
        animals_count[letter] = result

    return animals_count


def save_to_csv(data, filename="beasts.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for letter, count in data.items():
            writer.writerow([letter, count])


async def main():
    start_time = time.time()
    print("Собираем данные с Википедии...")
    animals_count = await scrape_animals_by_letter()
    print("Сохраняем результаты в beasts.csv...")
    assert (
        sum(animals_count.values()) > 0
    ), f"Error: It was not possible to collect data on animals. The total number of animals is {sum(animals_count.values())}, which is less than or equal to 0"
    save_to_csv(animals_count)
    end_time = time.time()
    print(f"Готово! Время выполнения программы - {end_time - start_time:.2f} сек.")


if __name__ == "__main__":
    asyncio.run(main())

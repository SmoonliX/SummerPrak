import fake_useragent
import requests
from bs4 import BeautifulSoup


def extract_vacancies(url):
    ua = fake_useragent.UserAgent()

    headers = {"user-agent": ua.random}
    response = requests.get(url, headers=headers)

    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Извлекаем название вакансии
    vacancy_titles = [title.get_text() for title in soup.find_all('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk')]

    # Извлекаем опыт работы
    experience = [exp.get_text() for exp in soup.find_all('span', {'data-qa': 'vacancy-serp__vacancy-work-experience'})]

    # Извлекаем название компании
    companies = [company.get_text() for company in
                 soup.find_all('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp')]

    # Извлекаем город
    cities = [city.get_text() for city in
              soup.find_all('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni')]
    vacancies = []

    # Печатаем результат
    for title, exp, company, city in zip(vacancy_titles, experience, companies, cities):
        vacancies.append({
            'title': title.strip() if title is not None else "",
            'experience': exp.strip() if exp is not None else "",
            'company': company.strip() if company is not None else "",
            'city': city.strip() if city is not None else "",
        })

    return vacancies

# print(extract_vacancies('https://hh.ru/search/vacancy?text=python&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line'))

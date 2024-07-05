import requests
from bs4 import BeautifulSoup
import fake_useragent
import requests
from bs4 import BeautifulSoup




def extract_resumes(url):
    ua = fake_useragent.UserAgent()

    headers = {"user-agent": ua.random}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    resumes = []
    for resume in soup.find_all('div', {'data-qa': 'resume-serp__resume'}):
        title, link, age, experience, last_job, last_job_date = None, None, None, None, None, None

        title_tag = resume.find('a', {'data-qa': 'serp-item__title'})
        if title_tag:
            title = title_tag.get_text()
            link = "https://hh.ru" + title_tag['href']

        age_tag = resume.find('span', {'data-qa': 'resume-serp__resume-age'})
        if age_tag:
            age = age_tag.get_text().strip()

        experience_tag = resume.find('div', {'data-qa': 'resume-serp__resume-excpirience-sum'})
        if experience_tag:
            experience = experience_tag.get_text().strip()

        last_job_tag = resume.find('label', {'data-qa': 'last-experience-link'})
        if last_job_tag:
            last_job = last_job_tag.get_text().strip()

            last_job_date_tag = last_job_tag.find_next_sibling('span')
            if last_job_date_tag:
                last_job_date = last_job_date_tag.get_text().strip()


        if age is not None:
            age: str = age.replace("\xa0", "").replace("года", "").replace("год", "").replace("лет", "")
            age = int(age)
        resumes.append({
            'title': title if title is not None else "",
            'link': link if link is not None else "",
            'age': age if age is not None else -1 ,
            'experience': experience if experience is not None else "",
            'last_job': last_job if last_job is not None else "",
            'last_job_date': last_job_date if last_job is not None else "",
        })
    return resumes




import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import lxml
web_analysis = {'CareerCross': 'https://www.careercross.com/en/job-search/result/69419949'}

titles = []
urls = []
updates = []
locations = []
jobs = []
salaries = []
experiences = []
careers = []
english_level = []
japanese_level = []
educations = []
visas = []
skills = []

for w, j in web_analysis.items():

    page = 0

    while True:

        time.sleep(1)

        r = requests.get(j, params={"page": page + 1})
        if 'No jobs were found that matched your search.' in r.text or r.status_code != 200:
            break

        else:
            html = r.content
            soup = BeautifulSoup(html,"lxml")
            print('\033[1m' + '{0}, page {1}'.format(w, page + 1) + '\033[0m')

            if w == 'CareerCross':
                titles_r1 = [t.text.strip().replace('\n', '') for t in soup.find_all('a', {'class': 'job-details-url'})]  # title
                titles_r1 = list(map(lambda t: titles.append(t), titles_r1))
                full_url = [urljoin(j, r) for r in [l.get('href') for l in soup.find_all('a', {'class': "btn btn-lg-14 btn-primary"})]]  # url
                full_urls = list(map(lambda f: urls.append(f), full_url))
                i = 0
                for f in full_url:  # going to each page
                    time.sleep(1)
                    r = requests.get(f)
                    if r.status_code == 200:
                        print('#URL {0}: {1}'.format(i + 1, f))
                    else:
                        print('ERROR {0}: Skipping #URL{1}: {2}'.format(r.status_code, i + 1, f))
                        i = i + 1
                        continue
                    r_html = r.content
                    r_soup = BeautifulSoup(r_html, 'lxml')
                    updates.append(r_soup.find_all('span', {'id': "jsonld-date-posted"})[0].text.strip())  # date of update
                    locations.append(r_soup.find_all('span', {'id': 'jsonld-job-location'})[0].text.strip())  # location

                    try:
                        job = r_soup.find_all('span', {'id': 'jsonld-employment-type'})[0].text.strip()  # type of job
                    except IndexError:
                        jobs.append(np.nan)
                    else:
                        jobs.append(job)

                    salaries.append(r_soup.find_all('span', {'id': 'jsonld-base-salary'})[0].text.strip())  # salary
                    experiences.append(r_soup.find_all('span', {'id': "jsonld-experience-requirements"})[0].text.strip())  # experience
                    careers.append(r_soup.find_all('span', {'id': "jsonld-experience-requirements"})[1].text.strip())  # career
                    english_level.append(r_soup.find_all('span', {'id': "skill-english-text"})[0].text.strip())  # english
                    japanese_level.append(r_soup.find_all('span', {'id': "skill-japanese-text"})[0].text.strip())  # japanese
                    educations.append(r_soup.find_all('span', {'id': "jsonld-education-requirements"})[0].text.strip())  # education
                    visas.append(r_soup.find_all('span', {'id': "qualifications-visa-status"})[0].text.strip())  # visa

                    try:
                        skill = r_soup.find_all('span', {'id': 'qualifications-required-skills'})[0].text.strip()  # skill description

                    except IndexError:
                        try:
                            skill = \
                            [s.find_all('ul') for s in r_soup.find_all('span', {'id': "jsonld-description"})][0][
                                2].text.strip()
                            if len(skill) < 100:
                                skills.append([s.find_all('ul') for s in r_soup.find_all('span', {'id': "jsonld-description"})][0][1].text.strip())
                            else:
                                skills.append(skill)
                        except:
                            skills.append(r_soup.find_all('span', {'id': "jsonld-description"})[0].text.strip())
                    else:
                        skills.append(skill)
                    i = i + 1

            page += 1
columns = {'Title': titles, 'URL': urls, 'Update': updates, 'Location': locations, 'Type of job': jobs, 'Salary': salaries,
           'Experience needed': experiences, 'Career': careers, 'English Level': english_level, 'Japanese Level': japanese_level,
          'Education': educations, 'Visa': visas, 'Skill Description': skills}


df_analyst = pd.DataFrame(columns)

def make_clickable(val):
    return '<a href="{0}">{0}</a>'.format(val)


pd.reset_option('display.max_rows', None)
pd.reset_option('display.max_columns', None)
pd.reset_option('display.width', None)
pd.reset_option('display.max_colwidth', -1)

df_analyst.style.format({'URL' :make_clickable})
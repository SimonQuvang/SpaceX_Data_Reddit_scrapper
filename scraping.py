from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv

submission_ids = ['c61lqs', 'ci70t4', 'cxyt8x', 'dfd8ik', 'e11zs0', 'ellkmn', 'f9mmb0', 'fr73sy', 'ghgmyg', 'hf368o',
                  'i4j0bk', 'inkzwp', 'j545qo', 'jtvex0', 'kbjngb', 'lc7eij', 'm06c13', 'mk99yw']

session = HTMLSession()


def get_souce_of_update(temp_obj, links):
    for link in links:
        source_obj = {'link': link['href'], 'text': link.text}
        temp_obj['source'].append(source_obj)


def fetch(id):
    url = f'https://www.reddit.com/r/spacex/comments/{id}'
    request = session.get(url)
    html = BeautifulSoup(request.text, 'lxml')
    tables = html.select('table')
    for table in tables:
        table_header = table.select('thead strong')
        if len(table_header) < 1:
            continue

        table_body = table.select('tbody tr')
        for row in table_body:
            # defining the temp_obj here to make sure it gets cleaned up for every new row
            temp_obj = {
                "date": "",
                "source": []
            }
            # Getting the date of the update
            date = row.select('td:nth-child(1)')
            temp_obj["date"] = date[0].text

            # Getting the source of the update, including the link and text
            links = row.select('td a', href=True)
            get_souce_of_update(temp_obj, links)

            print(temp_obj)


if __name__ == '__main__':
    for id in submission_ids:
        fetch(id)

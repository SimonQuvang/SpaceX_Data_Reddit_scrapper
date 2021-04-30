from requests_html import HTMLSession
import chompjs

s = HTMLSession()
url = 'https://www.reddit.com/r/spacex/comments/'

submission_id = ['c61lqs', 'ci70t4', 'cxyt8x', 'dfd8ik', 'e11zs0', 'ellkmn', 'f9mmb0', 'fr73sy', 'ghgmyg', 'hf368o',
                 'i4j0bk', 'inkzwp', 'j545qo', 'jtvex0', 'kbjngb', 'lc7eij', 'm06c13', 'mk99yw']


def fetch(x):
    r = s.get(f'https://www.reddit.com/r/spacex/comments/{x}')
    print(r.html.find('#post-content'))


fetch(submission_id[0])

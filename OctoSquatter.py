import requests
import bs4

import datetime
import time
import calendar
import dateutil.parser

import repos
import generator

# the basic url for GitHub search
root_url = 'https://github.com/search?type=Repositories&utf8=%E2%9C%93'

query_string = '&q=' + input("Search: ")

while query_string == '&q=':
    print ("Search string cannot be empty!")
    query_string = '&q=' + input("Search: ")

lang = '&l=' + input("Language: ")

if lang == '&l=':
    lang = ''

pages = int(input("How many pages to parse: "))

repo_list = []

def get_repos(page):

    index_url = root_url + lang + query_string + "&p=" + repr(page)

    # query the page of results and itemize each repository
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text).select('li.repo-list-item')

    # check if result page is empty
    if len(soup) > 0:
        global repo_list
        for x in soup:
            project_title = x.select('h3.repo-list-name')[0].a['href']
            project_description = x.select('p.repo-list-description')
            last_update = datetime.datetime.strptime(x.time['datetime'], "%Y-%m-%dT%H:%M:%SZ")

            if project_description != []:
                project_description = project_description[0].get_text().strip()

            # convert time from UTC to Unix time format
            last_update_time_unix = calendar.timegm(datetime.datetime.strptime(x.time['datetime'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
            time_diff = calendar.timegm((datetime.datetime.utcnow() - datetime.timedelta(weeks=52)).utctimetuple())

            # check if last updated over 52 weeks ago
            if last_update_time_unix < time_diff:
                repo_list.append(repos.proj(project_title, project_description, last_update))
    else:
        return 404

for x in range(1,pages+1):
    if get_repos(x) == 404:
        print (x, "empty page")
        break
    print ("Page number", x, "parsed.")

# generate html page with results
generator.display_page(repo_list)

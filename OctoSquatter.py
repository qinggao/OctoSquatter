import requests, bs4
import repos, generator

import time, datetime, calendar
import dateutil.parser

import sys

# the basic url for GitHub search
root_url = 'https://github.com/search?type=Repositories&utf8=%E2%9C%93'

if sys.argv[1] in ("-h", "--help") :
    print ("Usage: OctoSquatter.py <keyword> <language> <pages>")
    quit()

def get_param():
    query_string = '&q=' + input("Search: ")

    while query_string == '&q=':
        print ("Search string cannot be empty!")
        query_string = '&q=' + input("Search: ")

    lang = '&l=' + input("Language: ")

    if lang == '&l=':
        lang = ''

    while True:
        try:
            pages = int(input("How many pages to parse: "))
        except ValueError:
            print ("Please enter a valid integer.")

if len(sys.argv) == 4:
    try:
        query_string = '&q=' + sys.argv[1]
        lang = '&l=' + sys.argv[2]
        pages = int(sys.argv[3])
    except ValueError:
        print ("Invalid arguments.")
        get_param()

else:
    get_param()

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
            project_path = x.select('h3.repo-list-name')[0].a['href']
            project_description = x.select('p.repo-list-description')
            last_update = datetime.datetime.strptime(x.time['datetime'], "%Y-%m-%dT%H:%M:%SZ")

            if project_description != []:
                project_description = project_description[0].get_text().strip()
            else:
                project_description = "(Description not available)"
                
            project_description_txt = project_description
            if len(project_description) > 55:
                project_description = project_description[0:47] + "..."

            # convert time from UTC to Unix time format
            last_update_time_unix = calendar.timegm(datetime.datetime.strptime(x.time['datetime'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
            time_diff = calendar.timegm((datetime.datetime.utcnow() - datetime.timedelta(weeks=52)).utctimetuple())

            # check if last updated over 52 weeks ago
            if last_update_time_unix < time_diff:
                repo_list.append(repos.proj(project_path, project_description, project_description_txt, last_update))
    else:
        return 404

for x in range(1,pages+1):
    if get_repos(x) == 404:
        print (x, "empty page")
        break
    print ("Page number", x, "parsed.")

# generate html page with results
generator.display_page(repo_list)

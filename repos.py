class proj():
    '''Stores repository information'''

    def __init__(self, repo_title, repo_description, repo_last_update):
        self.title = repo_title
        self.description = repo_description
        self.last_update = repo_last_update
        self.url = "http://www.github.com" + repo_title
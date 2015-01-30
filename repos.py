class proj():
    '''Stores repository information'''

    def __init__(self, repo_path, repo_description, repo_description_txt, repo_last_update):
        self.path = repo_path
        self.description = repo_description
        self.txt = repo_description_txt
        self.last_update = repo_last_update
        self.url = "http://www.github.com" + repo_path
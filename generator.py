import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Abandoned Projects</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        .project-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .project-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
    </style>
    <script type="text/javascript" charset="utf-8">
        
        // Animate in the projects when the page loads
        $(document).ready(function () {
          $('.project-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">GitHub Projects</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {project_tiles}
    </div>
  </body>
</html>
'''

# A single project entry html template
tile_content = '''
<div class="col-md-6 col-lg-4 project-tile text-center" title="{project_txt}">
    <a href={project_url}><h2>{project_path}</h2></a>
    <p>{project_description}</p>
    <p>{project_last_update}</p>
</div>
'''

def create_tiles_content(repos):
    # The HTML content for this section of the page
    content = ''
    for repo in repos:
        # Append the tile for the projects with its content filled in
        content += tile_content.format(
            project_path = repo.path,
            project_description = repo.description,
            project_txt = repo.txt,
            project_last_update = repo.last_update,
            project_url = repo.url
        )
    return content

def display_page(repos):
  # Create or overwrite the output file
  output_file = open('results.html', 'w')

  # Replace the placeholder for the project tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(project_tiles=create_tiles_content(repos))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible
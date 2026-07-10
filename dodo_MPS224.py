from pathlib import Path
import os
import subprocess
import shutil
import re
import json

module_code = 'MPS224'
top_dir = Path('.').resolve()

admin_dir          = top_dir / 'admin'
assignments_dir    = top_dir / 'assignments'
coderunner_dir     = top_dir / 'coderunner'
data_dir           = top_dir / 'data'
images_dir         = top_dir / 'images'
lectures_dir       = top_dir / 'lectures'
macros_dir         = top_dir / 'macros'
notebooks_dir      = top_dir / 'notebooks'
notebooks_html_dir = top_dir / 'notebooks_html'
planning_dir       = top_dir / 'planning'
tasks_dir          = top_dir / 'tasks'
trivia_dir         = top_dir / 'trivia'
videos_dir         = top_dir / 'videos'
web_dir            = top_dir / 'web'

web_data_dir           = web_dir / 'data'
web_demos_dir          = web_dir / 'demos'
web_images_dir         = web_dir / 'images'
web_js_dir             = web_dir / 'js'
web_labs_dir           = web_dir / 'labs'
web_lectures_dir       = web_dir / 'lectures'
web_notebooks_dir      = web_dir / 'notebooks'
web_notebooks_html_dir = web_dir / 'notebooks_html'
web_tasks_dir          = web_dir / 'tasks'

def list_used_notebooks():
    """ 
    List all the notebooks that are used (for a lecture or a lab,
    or as a solution for a task) by parsing the file notebooks.json
    """
    with open('web/data/notebooks.json') as f:
        notebooks = json.load(f)
    used_notebooks = set()
    for group in notebooks['groups']:
        for notebook in notebooks['groups'][group]:
            used_notebooks.add(notebook)

    used_notebooks = sorted(list(used_notebooks))
    return used_notebooks
    
def list_used_tasks():
    """
    List all the tasks that are used (for a lab) by parsing the file 
    tasks.json
    """
    with open('web/data/tasks.json') as f:
        tasks = json.load(f)

    used_tasks = set()
    for lab in tasks:
        for task in tasks[lab]:
            used_tasks.add(task)

    used_tasks = sorted(list(used_tasks))
    return used_tasks

def convert_notebook(name):
    subprocess.run(['jupyter', 'nbconvert',
                    '--to', 'html',
                    '--output-dir', notebooks_html_dir,
                    '--output', name,
                    name + '.ipynb'],
                   cwd = notebooks_dir, shell=True).check_returncode()

def task_notebooks_html():
    """HTML notebooks""",
    notebooks = list(notebooks_dir.glob('*.ipynb'))
    for f in notebooks:
        yield {
         'name' : f,
         'actions' : [(convert_notebook,[f.stem])],
         'targets' : [notebooks_html_dir / (f.stem + '.html')],
         'file_dep': [f]
        }

def task_web_notebooks():
    """Copy notebooks to the web directory"""
    for f in list_used_notebooks():
        yield {
            'name' : f,
            'actions' : [(shutil.copy2,[notebooks_dir / (f + '.ipynb'), web_notebooks_dir])],
            'targets' : [web_notebooks_dir / (f + '.ipynb')],
            'file_dep': [notebooks_dir / (f + '.ipynb')]
        }

def task_web_notebooks_html():
    """Copy HTML notebooks to the web directory"""
    for f in list_used_notebooks():
        yield {
            'name' : f,
            'actions' : [(shutil.copy2,[notebooks_html_dir / (f + '.html'), web_notebooks_html_dir])],
            'targets' : [web_notebooks_html_dir / (f + '.html')],
            'file_dep': [notebooks_html_dir / (f + '.html')]
        }

def task_web_tasks():
    """Copy tasks to the web directory"""
    for f in list_used_tasks():
        yield {
            'name' : f,
            'actions' : [(shutil.copy2,[tasks_dir / (f + '.html'), web_tasks_dir])],
            'targets' : [web_tasks_dir / (f + '.html')],
            'file_dep': [tasks_dir / (f + '.html')]
        }

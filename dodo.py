from pathlib import Path
import os
import subprocess
import shutil
import re
import json

module_code = 'MAS100'
top_dir = Path('.').resolve()

exams_dir          = top_dir / 'exams'
lectures_dir       = top_dir / 'lectures'
presentations_dir  = top_dir / 'presentations'
tutorials_dir      = top_dir / 'tutorials'
labs_maple_dir     = top_dir / 'labs_maple'
labs_maxima_dir    = top_dir / 'labs_maxima'
labs_python_dir    = top_dir / 'labs_python'
web_dir            = top_dir / 'web'

web_exams_dir         = web_dir / 'exams'
web_lectures_dir      = web_dir / 'lectures'
web_presentations_dir = web_dir / 'presentations'
web_tutorials_dir     = web_dir / 'tutorials'
web_labs_maple_dir    = web_dir / 'labs_maple'
web_labs_maxima_dir   = web_dir / 'labs_maxima'
web_labs_python_dir   = web_dir / 'labs_python'

lab_numbers = [f'{i:02d}' for i in range(1,12)]

def convert_ipynb(name, source_dir, target_dir):
    subprocess.run(['jupyter', 'nbconvert',
                    '--to', 'html',
                    '--output-dir', target_dir,
                    '--output', name,
                    name + '.ipynb'],
                   cwd = source_dir, shell=True).check_returncode()

def convert_wxmx(name, source_dir, target_dir):
    raise NotImplementedError("Conversion from wxMaxima to HTML is not implemented yet.")

def convert_mw(name, source_dir, target_dir):
    raise NotImplementedError("Conversion from Maple to HTML is not implemented yet.")

def make_exams():
    """Make the combined exam file"""
    subprocess.run(['pdflatex',
                    'all_exams.tex'],
                   cwd = exams_dir).check_returncode()
    shutil.copy2(exams_dir / 'all_exams.pdf', web_dir)

def make_tutorials():
    """Make the tutorial problem sheets"""
    subprocess.run(['pdflatex',
                    'all_probs.tex'],
                   cwd = tutorials_dir).check_returncode()
    shutil.copy2(tutorials_dir / 'all_probs.pdf', web_dir)

def make_lectures():
    """Make the lecture slides"""
    subprocess.run(['pdflatex',
                    'all_lectures.tex'],
                   cwd = lectures_dir).check_returncode()
    shutil.copy2(lectures_dir / 'all_lectures.pdf', web_dir)
    
def make_handouts():
    """Make the lecture slides"""
    subprocess.run(['pdflatex',
                    '-job-name=all_handouts',
                    r'\def\LECTURES{1}',
                    r'\input{all_lectures}'],
                   cwd=lectures_dir).check_returncode()
    shutil.copy2(lectures_dir / 'all_handouts.pdf', web_dir)
    
def make_all_labs_maple():
    """Make the Maple lab sheets"""
    subprocess.run(['pdflatex',
                    'all_labs_maple.tex'],
                   cwd = labs_maple_dir).check_returncode()
    shutil.copy2(labs_maple_dir / 'all_labs_maple.pdf', web_labs_maple_dir)

def make_primer_maple():
    """Make the Maple primer"""
    subprocess.run(['pdflatex',
                    'primer_maple.tex'],
                   cwd = labs_maple_dir).check_returncode()
    shutil.copy2(labs_maple_dir / 'primer_maple.pdf', web_labs_maple_dir)

def make_all_labs_python():
    """Make the Python lab sheets"""
    subprocess.run(['pdflatex',
                    'all_labs_python.tex'],
                   cwd = labs_python_dir).check_returncode()
    shutil.copy2(labs_python_dir / 'all_labs_python.pdf', web_labs_python_dir)

def make_primer_python_pdf():
    """Make the Python primer"""
    subprocess.run(['pdflatex',
                    'primer_python.tex'],
                   cwd = labs_python_dir).check_returncode()
    shutil.copy2(labs_python_dir / 'primer_python.pdf', web_labs_python_dir)

def make_primer_python_html():
    """Make the HTML version of the Python primer"""
    convert_ipynb('primer_python', labs_python_dir, labs_python_dir)
    shutil.copy2(labs_python_dir / 'primer_python.html', web_labs_python_dir)
    shutil.copy2(labs_python_dir / 'primer_python.ipynb', web_labs_python_dir)

def make_python_sols_web(nn):
    """Make the HTML solutions for a Python lab, and copy to the web directory"""
    name = 'lab_sols' + nn
    convert_ipynb(name, labs_python_dir / 'sols', labs_python_dir / 'sols_html')
    shutil.copy2(labs_python_dir / 'sols' / (name + '.ipynb'), web_labs_python_dir / 'sols')
    shutil.copy2(labs_python_dir / 'sols_html' / (name + '.html'), web_labs_python_dir / 'sols_html')

def make_maxima_sols_web(nn):
    """Make the HTML solutions for a Maxima lab, and copy to the web directory"""
    name = 'lab_sols' + nn
#    convert_wxmx(name, labs_maxima_dir / 'sols', labs_maxima_dir / 'sols_html')
    shutil.copy2(labs_maxima_dir / 'sols' / (name + '.wxmx'), web_labs_maxima_dir / 'sols')
#    shutil.copy2(labs_maxima_dir / 'sols_html' / (name + '.html'), web_labs_maxima_dir / 'sols_html')

def make_maple_sols_web(nn):
    """Make the HTML solutions for a Maple lab, and copy to the web directory"""
    name = 'lab_sols' + nn
#    convert_mw(name, labs_maple_dir / 'sols', labs_maple_dir / 'sols_html')
    shutil.copy2(labs_maple_dir / 'sols' / (name + '.mw'), web_labs_maple_dir / 'sols')
#    shutil.copy2(labs_maple_dir / 'sols_html' / (name + '.html'), web_labs_maple_dir / 'sols_html')

def task_exams():
    """Combined exams file"""
    return {
        'actions'  : [make_exams],
        'targets'  : [exams_dir / 'all_exams.pdf'],
        'file_dep' : [exams_dir / 'all_exams.tex']
    }
    
def task_tutorials():
    """Combined problem sheets file"""
    return {
        'actions'  : [make_tutorials],
        'targets'  : [tutorials_dir / 'all_probs.pdf'],
        'file_dep' : [tutorials_dir / 'all_probs.tex']
    }
    
def task_lectures():
    """Lecture slides file"""
    return {
        'actions'  : [make_lectures],
        'targets'  : [lectures_dir / 'all_lectures.pdf'],
        'file_dep' : [lectures_dir / 'all_lectures.tex']
    }

def task_handouts():
    """Lecture handouts file"""
    return {
        'actions'  : [make_handouts],
        'targets'  : [lectures_dir / 'all_handouts.pdf'],
        'file_dep' : [lectures_dir / 'all_lectures.tex']
    }

def task_primer_maple():
    """Maple primer file"""
    return {
        'actions'  : [make_primer_maple],
        'targets'  : [labs_maple_dir / 'primer_maple.pdf'],
        'file_dep' : [labs_maple_dir / 'primer_maple.tex']
    }

def task_all_labs_maple():
    """Combined Maple lab sheets file"""
    return {
        'actions'  : [make_all_labs_maple],
        'targets'  : [labs_maple_dir / 'all_labs_maple.pdf'],
        'file_dep' : [labs_maple_dir / 'all_labs_maple.tex']
    }

def task_primer_python_pdf():
    """Python primer file"""
    return {
        'actions'  : [make_primer_python_pdf],
        'targets'  : [labs_python_dir / 'primer_python.pdf'],
        'file_dep' : [labs_python_dir / 'primer_python.tex']
    }

def task_primer_python_html():
    """Python primer file"""
    return {
        'actions'  : [make_primer_python_html],
        'targets'  : [labs_python_dir / 'primer_python.html'],
        'file_dep' : [labs_python_dir / 'primer_python.ipynb']
    }

def task_all_labs_python():
    """Combined Python lab sheets file"""
    return {
        'actions'  : [make_all_labs_python],
        'targets'  : [labs_python_dir / 'all_labs_python.pdf'],
        'file_dep' : [labs_python_dir / 'all_labs_python.tex']
    }

def task_python_sols_web():
    """Python HTML solutions""",
    for nn in lab_numbers:
        yield {
            'name' : 'python_sols_web' + nn,
            'actions'  : [(make_python_sols_web, [nn])],
            'targets'  : [labs_python_dir / 'sols_html' / ('lab_sols' + nn + '.html'),
                          web_labs_python_dir / 'sols' / ('lab_sols' + nn + '.ipynb'),
                          web_labs_python_dir / 'sols_html' / ('lab_sols' + nn + '.html')],
            'file_dep' : [labs_python_dir / 'sols' / ('lab_sols' + nn + '.ipynb') ]
        }


def task_web_maxima_sols():
    """Copy Maxima solutions to the web directory"""
    source_dir = labs_maxima_dir / 'sols'
    target_dir = web_labs_maxima_dir / 'sols'
    for nn in lab_numbers:
        name = 'lab_sols' + nn + '.wxmx'
        source_name = source_dir / name
        target_name = target_dir / name
        yield {
            'name' : name,
            'actions' : [(shutil.copy2,[source_name, target_dir])],
            'targets' : [target_name],
            'file_dep': [source_name]
        }

def task_web_maple_sols():
    """Copy Maple solutions to the web directory"""
    source_dir = labs_maple_dir / 'sols'
    target_dir = web_labs_maple_dir / 'sols'
    for nn in lab_numbers:
        name = 'lab_sols' + nn + '.mw'
        source_name = source_dir / name
        target_name = target_dir / name
        yield {
            'name' : name,
            'actions' : [(shutil.copy2,[source_name, target_dir])],
            'targets' : [target_name],
            'file_dep': [source_name]
        }

    

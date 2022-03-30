from flask import render_template, url_for
from jeraldthomas_dot_com import app

import bibtexparser

@app.route('/')
def index():
    return render_template('index.html', current_page='index')

@app.route('/publications')
def publications():
    with open('jeraldthomas_dot_com/static/publications/references.bib') as bibtex_file:
        bibs = bibtexparser.load(bibtex_file)

    for bib in bibs.entries:
        bib["author"] = " and ".join(["<b>"+x+"</b>" if "Jerald" in x else x for x in bib["author"].split(" and ")])

    sorted_bibs = {
        "Peer Reviewed Conference and Journal Papers": [],
        "Peer Reviewed Conference Workshop Papers": [],
        "Peer Reviewed Conference Posters": [],
        "Other Publications": [],
    }

    for bib in bibs.entries:
        if not "type" in bib or not bib["type"] in sorted_bibs:
            sorted_bibs["Other Publications"].append(bib)
        else:
            sorted_bibs[bib["type"]].append(bib)
            
    return render_template('publications.html', current_page='publications', bibs=sorted_bibs)

@app.route('/publications/bib/<key>')
def show_bibtex(key):
    with open('jeraldthomas_dot_com/static/publications/references.bib') as bibtex_file:
        bibs = bibtexparser.load(bibtex_file)

    for bib in bibs.entries:
        if key == bib["ID"]:
            db = bibtexparser.bibdatabase.BibDatabase()
            tmp = bib
            del tmp["type"]
            del tmp["notes"]            
            db.entries = [tmp]
            return f"<pre>{bibtexparser.dumps(db)}</pre>"

@app.route('/projects')
def projects():
    return render_template('projects.html', current_page='projects')

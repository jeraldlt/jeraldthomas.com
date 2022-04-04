from flask import render_template, url_for, redirect

from jeraldthomas_dot_com import app, analytics

import bibtexparser

@app.route('/')
@analytics.log_views('views.json')
def index():
    return render_template('index.html', current_page='index')

@app.route('/publications')
@analytics.log_views('views.json')
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
@analytics.log_views('views.json')
def projects():
    return render_template('projects.html', current_page='projects')

@app.route('/cv')
@analytics.log_views('views.json')
def cv():
    return redirect(url_for('static', filename='JeraldThomas_CV.pdf'))

@app.route('/admin/update_cv', methods=['POST'])
@analytics.log_views('admin_views.json')
def update_cv():
    import subprocess
    process = subprocess.Popen('eval "$(ssh-agent -s)"', shell=True, stdout=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen('ssh-add ~/.ssh/jeraldlt_github', shell=True, stdout=subprocess.PIPE)
    process.wait()

    import git
    repo = git.Repo('jeraldthomas_dot_com/static/ApplicationMaterials/')
    repo.git.pull('origin', 'main')
    return '', 204

from git import Repo
import pypandoc
from os import path, getcwd, remove, environ
from glob import glob
from datetime import datetime

CWD = getcwd()
FILEPATH = path.dirname(path.abspath(__file__))
GIT_YAML = 'git.yaml'

def fetch_zotero(c_id):
    from pyzotero import zotero
    import bibtexparser
    zot_id = environ.get('ZOTERO_ID')
    zot_api = environ.get('ZOTERO_KEY')
    zot = zotero.Zotero(zot_id, 'user', zot_api)
    zot.add_parameters(format='bibtex')
    bibtex = zot.collection_items(c_id)
    with open(path.join(CWD, 'references.bib'), 'w') as w:
        w.write(bibtexparser.dumps(bibtex))
        w.close()
    return None

def write_git(outfile=GIT_YAML):
    repo = Repo(CWD)
    active_branch = repo.active_branch
    commit = active_branch.commit

    props = {
        'git_branch': active_branch.name,
        'git_message': commit.message,
        'git_name': commit.author.name,
        'git_email': commit.author.email,
        'git_time': commit.committed_datetime.strftime("%H:%M"),
        'git_date': commit.committed_datetime.strftime("%B %d, %Y" ),
        'git_sha': commit.hexsha[0:8]
    }
    git_args = '---\n'
    for p in props.items():
        git_args += p[0] + ': "'
        if p[1][-1] == '\n':
            git_args += p[1][0:-1] + '"\n'
        else:
            git_args += p[1] + '"\n'
    git_args += '---\n'
    with open(outfile, 'w') as w:
        w.write(git_args)
        w.close()
    
    return None

def conc_files(extensions, exclude=['README.md']):
    string = ''
    for e in extensions:
        for file in glob(path.join(CWD, '.'.join(('*', e)))):
            if path.split(file)[1] not in exclude:
                with open(file, 'r') as r:
                    string = ''.join((string, r.read(), '\n'))
    return string

def find_file(extension, dir=CWD):
    return glob(path.join(dir, '.'.join(('**/*', extension))), recursive=True)[0]

def build_doc(out_file, out_format, zotero_id=None, keepbib=False): 

    addl = []
    if zotero_id:
        print("Fetching Zotero collection...")
        fetch_zotero(COLLECTION)
    if len(glob(path.join(CWD, '*.bib'))) > 0:
        addl = ['--citeproc', '--bibliography=' + find_file('bib')]

    args = [
        '--pdf-engine=xelatex',
        '--template='+ find_file('tex', dir=FILEPATH),
        '--csl=' + find_file('csl', dir=FILEPATH),
        '--highlight-style=kate',
    ]

    args.extend(addl)
    write_git()

    print("Converting document...")

    text = conc_files(['yaml', 'md'])

    if zotero_id or len(glob(path.join(CWD, '*.bib'))) > 0:
        text += "\n\n#  References"
    
    pypandoc.convert_text(
        text,
        out_format,
        format='md',
        outputfile=path.join(CWD, out_file),
        extra_args = args,
        # filters = filters
    )
    remove(GIT_YAML)
    
    if zotero_id and not KEEPBIB:
        remove(path.join(CWD, 'references.bib'))

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help="Type of document to build.", choices=['pdf'], default='pdf')
    parser.add_argument("-o", "--outputfile", help="Name of output document with extension.", default='output.pdf')
    parser.add_argument("-c", "--collection", help="ID of Zotero collection.", default=None)
    parser.add_argument("-k", "--keepbib", help="Whether to keep bibliography. Keep on final build for replicability reasons.", action='store_true')
    args = parser.parse_args()

    build_doc(out_file=args.outputfile, out_format=args.type, zotero_id=args.collection, keepbib=args.keepbib)


if __name__ == '__main__':
    main()
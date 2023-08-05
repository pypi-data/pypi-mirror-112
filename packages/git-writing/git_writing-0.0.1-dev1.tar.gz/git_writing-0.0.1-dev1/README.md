# Git Writing

This package accomplishes a number of the tedious, tedious tasks associated with reproducible and version-controlled academic writing---in other words, it Gits (🤓) you writing. [A sample of the document produced by the template is here](https://ericrobskyhuntley.org/media/other/git_writing_output.pdf) (it expands on and modifies the Pandoc pdf LaTeX template). If you've been looking for a package to...

+ initiate Git repos that include all documents necessary for particular types of writing
+ build beautiful documents using a Pandoc-LaTeX workflow that are also capable of folding in Git version control metadata
+ remove the additional step of managing your Bibtex bibliography---you already have a Zotero collection! Why spend your time worrying after a local copy?

...this might be for you. It includes templates for multiple types of writing.

## Requires Pandoc

This package requires that Pandoc be installed. I recommend you consult [the Pandoc documentation for installation](https://pandoc.org/installing.html) instructions.

## Initiating a new repository

From the CLI, `git_writing` will initiate a new repository, copy template files, and commit with an "initial commit" message. For example...

```bash
git_writing --genre article --name reponame
```

Currently, there is only an 'article' template, but this will be expanding. 'Repo name' here refers only to the name of the directory into which a repository will be initiated, and the first line of the `README.md` file which is auto-populated. Initiating a new repo will create a directory that looks like this:

```markdown
.
|── README.md
|── authors.yaml
|── style.yaml
|── text.md
```

These files are (hopefully) somewhat self-explanatory. For what it's worth---the _names_ of individual files are arbitrary. So long as your folder contains a collection of `yaml` and `md` files, you should be in business. Keep in mind that they are ordered by file type---YAML first---then filename.

The 'authors' key might require some explication. A single author looks like this:

```yaml
---
authors:
- name: Eric Robsky Huntley, PhD
  affiliation: Massachusetts Institute of Technology
  place: false
  email: ehuntley@mit.edu
  surname: Robsky Huntley
...
```

The `place` appears after the `affiliation` in the authors list. The `surname` is useful here because 1) the template uses last name in the document header, which is slightly complicated because 2) I have two names that I use as a surname.

Two authors look like this:

```yaml
authors:
- name: Eric Robsky Huntley, PhD
  ...
- name: Tipple B. Applesauce, DPhil
  ...
```

## Zotero Integration

If you plan on using the Zotero integration, you'll need to store your Zotero API key and your Zotero ID as `ZOTERO_KEY` and `ZOTERO_ID` environment varibles respectively. On a Mac, this means adding the following lines to your `.bash_profile`:

```bash
export ZOTERO_KEY='...'
export ZOTERO_ID='...'
```

The former grants access to the Zotero API, the latter uniquely identifies your library.

In addition, you'll need to find the collection ID that your particular work is drawing on (these are represented as folders in the GUI).

## Building Your Document

From the CLI, the `git_building` command will build your document. Sensible defaults are provided so you don't need any flags.

```bash
git_building
```

This will build a document using Pandoc running through a custom LaTeX template. The above assumes that you've included your own `.bib` file (provided, again, that citations are needed---otherwise, no `bib` is necessary). If you want to use a Zotero collection, simply run...

```bash
git_building --collection 'ZOTEROCOLLECTIONID'
```

## Credit Where Credit is Due

Much of this is inspired by Kieran Healy's [plaintext social science](https://plain-text.co/)---I make no claim to the superiority of my solution. I can only say that my Make is weaker than my Python, and that I can't stand fighting with the LaTeX memoir class. I also wanted to automate some of the tedious repo-creation tasks.

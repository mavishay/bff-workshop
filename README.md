# Welcome for Tikal Python BFF workshop

## Prerequisites

Before we began please make sure you have `python` and `poetry` installed on your computer. 

Run `python --version` or `python3 --version` and look for something like that 
> Python 3.12.3 

if it's not installed run `brew install python` and try the following step again.

---

In this workshop we will use `poetry` as package management tool please verify it is installed by running `poetry --version` the output should look like something like that 
> Poetry (version 1.8.3)

if it's not installed install it running `curl -sSL https://install.python-poetry.org | python3 -`

## First step - Creating our project

In order to create a new python project got the directory you want to create your project in using the CLI and run `poetry new bff-workshop`
This will create new folder with several files. **Try it now!**. 

If everything worked as planned it should have return you this message 
> Created package bff-workshop in bff-workshop

Let's open the new created folder with a code editor and see it's content: 
The content should be something like that:
```
bff-workshop
├── pyproject.toml
├── README.md
├── bff-workshop
│   └── __init__.py
└── tests
    └── __init__.py
```


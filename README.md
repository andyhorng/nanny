Nanny
=====

Installation
------------

    python setup.py install 

If you want install it in user directory without sudo
  
    python setup.py install --user

Templates default location is in ~/.nanny/templates/ 

Generate
--------

Generate files and folders according a template

    nanny generate <template-name>

List avaliable templates

    nanny list

more help

    nanny --help

Create Template
---------------

    nanny create <template-name>

### An Example ###

    $ tree example/hello-world/
    hello-world
    ├── description.yml
    ├── dynamic.py
    └── {{name}}
        └── hello-{{name}}.txt

    $ cat hello-{{name}}.txt
    Hello, {{name}}. 

    你的名字倒著寫叫 {{reverse_name}}

    $ nanny generate hello-world

    $ tree .
    .
    └── Andy
        └── hello-Andy.txt

    $ cat hello-Andy.txt
    Hello, Andy. 

    你的名字倒著寫叫 ydnA


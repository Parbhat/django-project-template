{{ project_name }}
==================

SET THE PROJECT DESCRIPTION


installation
------------

### setup virtualenv

Note: Its highly recommended to run this app in a virtualenv, however if you're
developing in a sandboxed environment, it should be fine to install all
neccessary packages into the global environment.

    $ pip install virtualenv
    $ virtualenv --no-site-packages {{ project_name }}
    $ cd {{ project_name }}
    $ source bin/activate

### setup git-encrypt

{{ project_name }} does store some secret files in the repo, to unencrypt these files you
will need to install [git-encrypt](https://github.com/shadowhand/git-encrypt)
and configure it with the appropriate secrets.  Ask another developer on the
project to obtain these secrets.

#### mac os x

    $ brew install openssl
    $ brew install git-encrypt
    $ gitcrypt init

### clone the repo

    $ git clone REPO

### configure git-encrypt
    
    $ git config gitcrypt.salt $SALT
    $ git config gitcrypt.pass $PASS
    $ git config gitcrypt.cipher "aes-256-ecb"
    $ git config filter.encrypt.smudge "gitcrypt smudge"
    $ git config filter.encrypt.clean "gitcrypt clean"
    $ git config diff.encrypt.textconv "gitcrypt diff"

### checkout project

    $ git reset --hard HEAD

### set secrets

All projects need secret or private variables, checking these values into VCS
is a known bad practice.  To get around this, {{ project_name }} is designed to load all
secret variables from the ENV (see [12factor.net](http://www.12factor.net/config)).
These variables can be loaded into your environment in any way, the following
is just one way of doing so.

    $ cp .env.sample .env
    $ vim .env
    ... fill in variable values
    $ source .env


development
-----------

### install dependencies

    $ make develop

### run tests

    $ make test

### start development server

    $ make server

### start development shell

    $ make shell

### cleaning temp files

    $ make clean


apps vs libs vs vendor
----------------------

Libs are very much like apps, and technically speaking from a Django perspective
they are exactly the same thing, small isolated components of functionality, that
collectively form the project. The difference lies in how this functionality is
used, as apps are more user oriented features and libs are more or less helper
libraries that are used across multiple apps to get common work done.  If in
doubt think of it like this, will this "app" have a urls.py file, if so then
its probably a user oriented feature and should be an app, if not then it is
probably a lib.

Vendor is of course reserved for all third party javascript/css apps that may
need to be included.

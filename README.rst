|Dependency Status| |Coverage Status| |Landscape|

+------------------+------------------+
| Windows          | Linux            |
+==================+==================+
| |Build status|   | |Build Status|   |
+------------------+------------------+

VoSeq is being rewritten
========================

We are rebuilding VoSeq from scratch. We decided to migrate from PHP to
Python by using the framework Django. We also moved from MySQL to
PostgreSQL.

You can still download the old VoSeq v1.7.4 from
`here <https://github.com/carlosp420/VoSeq/releases/tag/v1.7.4>`__. But
be aware that we will not be doing major maintenance of that code.

Here is a test installation of the old VoSeq (v1.7.0)
http://www.nymphalidae.net/VoSeq/

More details about the migration can be found in our `discussion
list <https://groups.google.com/forum/#!topic/voseq-discussion-list/wQ-E0Xcimgw>`__.

VoSeq 2.0.0 is the future!

Configuration
=============

Clone/download Voseq to your prefer directory.

You need to install some Python packages as dependencies:

.. code:: shell

    cd /path/to/VoSeq
    pip install -r requirements/dev.txt

Download and install PostgreSQL. For macOSX users we recommend to do it
by downloading the Postgres.app from http://postgresapp.com

Download and install ``elasticsearch`` from here:
http://www.elasticsearch.org/overview/elkdownloads/ (In Linux, you can
install the ``.deb`` file directly by running:
``~$ apt-get install elasticsearch``). The bin directory of
elasticsearch should be added automatically to your PATH. If not, add
the following line to your ``.profile`` (Linux) or ``.bash_profile``
(macOSX) file:

.. code:: shell

    export PATH="$PATH:/path/to/elasticsearch/bin/"

Create a PostgreSQL database (replace x.x for 9.3 or 9.4):

.. code:: shell

    sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-x.x
    sudo su postgres

Create new role by typing:

.. code:: shell

    createuser --interactive

Create a password for this user:

.. code:: shell

    psql
    postgres=# ALTER ROLE postgres WITH PASSWORD 'hu8jmn3';

Create a database for Voseq:

.. code:: shell

    postgres=# create database voseq;

In macOSX if you are using the Postgres.app, it my be enough to run:

.. code:: shell

    psql
    user.name=# CREATE DATABASE voseq;

Create a ``config.json`` file to keep the database variables:

.. code:: shell

    cd /path/to/Voseq
    touch config.json

and write in the following content:

.. code:: javascript

    {
    "SECRET_KEY": "create_a_secret_key",
    "DB_USER": "role_name",
    "DB_PASS": "create_a_database_password",
    "DB_NAME": "voseq",
    "DB_PORT": "5432",
    "DB_HOST": "localhost",
    "GOOGLE_MAPS_API_KEY": "get_a_google_map_api_key"
    }

On Windows
----------
* Download and install PostgreSQL from here http://www.enterprisedb.com/products-services-training/pgdownload.
* Instalar psycopg2 psycopg2-2.5.4.win-amd64-py3.4-pg9.3.5-release.exe
* Download and install Python3.4 (Windows x86-64 MSI installer) from here: https://www.python.org/downloads/windows/ 
* It is recommended to create a virtualenvironment. Open a Command Prompt and
  use the command `pip install virtualenvwrapper`
* Create the environment with the command: `c:\Python34\Scripts\virtualenv.exe
  .`
* Download and install git: http://git-scm.com/download/win
* Get a copy of VoSeq from GitHub. You will need to open a Git Bash console
  which behaves similarly to a Linux console.
  
    * First, go to your home folder: `cd /c/Users/Your Name/`
    * Clone the VoSeq repository: where you will keep and type `git clone https://github.com/carlosp420/VoSeq.git`

* Enter to the VoSeq folder and install the requirements:

.. code:: shell

    cd VoSeq
    pip install -r requirements/testing.txt

Migrate VoSeq database
======================

If you have a previous version of Voseq as server and want to migrate,
you need to dump your MySQL database into a XML file:

.. code:: shell

    cd /path/to/Voseq/
    mysqldump --xml voseq_database > dump.xml

Then use our script to migrate all your VoSeq data into a PostGreSQL
database.

.. code:: shell

    make migrations
    python migrate_db.py dump.xml

It might issue a warning message:

::

    WARNING:: Could not parse dateCreation properly.
    WARNING:: Using empty as date for `time_edited` for code Your_Vocher_Code

It means that the creation time for your voucher was probably empty or
similar to ``0000-00-00``. In that case the date of creation for your
voucher will be empty. This will not cause any trouble when running
VoSeq. You can safely ignore this message.

Create an index for all the data in your database:

.. code:: shell

    make index

Test database for development
=============================

You can use test data to populate your PostgreSQL database, useful for
development.

Create tables for the database:

.. code:: shell

    cd /path/to/Voseq/
    make migrations

Import test data for your database:

.. code:: shell

    make import

Start the server
================

In Linux start elasticsearch as a service and then start the server:

.. code:: shell

    sudo service elasticsearch start
    cd /path/to/Voseq
    make serve

In macOSX if you do not have the ``service`` command, run
``elasticsearch`` in the background and then start the server (\*):

\* *Note that if you did not check to Start Postgres automatically after
login, you first have to go to Applications and start it manually from
there by clicking on the Postgres.app. Do this before running the
server.*

.. code:: shell

    elasticsearch -d
    cd /path/to/Voseq
    make serve

Finally, open this URL in your web browser and you are ready to start
using VoSeq: ``http://127.0.0.1:8000/``

Administrate the server
=======================

Optionally if you want to add items/vouchers to your database
interactively, you need to create an administration account. Run the
following command and provide the requested information:

.. code:: shell

    make admin

.. |Dependency Status| image:: https://gemnasium.com/carlosp420/VoSeq.svg
   :target: https://gemnasium.com/carlosp420/VoSeq
.. |Coverage Status| image:: https://img.shields.io/coveralls/carlosp420/VoSeq.svg
   :target: https://coveralls.io/r/carlosp420/VoSeq?branch=master
.. |Build status| image:: https://ci.appveyor.com/api/projects/status/0ba440vjw8811845/branch/master?svg=true
   :target: https://ci.appveyor.com/project/carlosp420/voseq/branch/master
.. |Build Status| image:: https://travis-ci.org/carlosp420/VoSeq.svg
   :target: https://travis-ci.org/carlosp420/VoSeq
.. |Landscape| image:: https://landscape.io/github/carlosp420/VoSeq/master/landscape.svg
   :target: https://landscape.io/github/carlosp420/VoSeq/master
   :alt: Code Health

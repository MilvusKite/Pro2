# Proteostasis Profiler (PRO2) Web Application

Written in [Python](https://www.python.org) using [Django](https://www.djangoproject.com) framework, 
Proteostasis Profiler or PRO2 for short is "an integrated online resource and toolbox for the analysis 
and visualization of proteostasis disease alterations". Check http://www.proteostasys.org for 
trying out the tool, and [our paper](http://dx.doi.org/10.1371/journal.pcbi.1005890) for more information.


## Installing and running PRO2 locally
Here's a quick guide in case you want to run PRO2 locally. All codes in the guide are written and tested 
on Mac OS X, and are expected to run on other unix-based systems as well, and on windows with small 
modifications.
Although not fully necessary, we wholeheartedly recommend using "Virtual Environment" for running 
the proper version of python (2.7) and other packages dependencies of this app. 
You can install Virtualenv from [here](https://virtualenv.pypa.io/en/stable/). This tutorial is 
written with the assumption of Virtualenv availability.

#### PRO2 Installation
1. Firstly, you need to clone the repository to your local computer. Easiest way for doing this is 
using [git](https://git-scm.com):
```
git clone https://github.com/brehmelab/Pro2.git
```
(You can also manually download the repository from github in case you don't want to use git)

2. Switch to "Python (Visualizations&Webtool)" directory, where PRO2 tool subsists:
```
cd Pro2/Python\ \(Visualizations\&Webtool\)/
```

3. Make a new virtualenv with python 2.7 as interpreter: (here we made it in the parent directory, 
in a folder named PRO2Env)
```
virtualenv --python=python2.7 ../PRO2Env
```

4. You need to activate the newly created virtualenv:
```
source ../PRO2Env/bin/activate
```

5. Now that you are in a virtualenv, you need to install all the dependency packages of PRO2.
These packages are used in making of PRO2. And they are listed in the file "requirements.txt".
You can install all packages in requirements.txt using pip:
```
pip install -r requirements.txt 
```
(pip should already be available inside your virtualenv, but in case it has problems with 
installing the dependencies, you probably need to update it to the last version)

6. You need to edit the "setting.py" of PRO2 app in three places to adapt it for running
locally:

* You need to add a "SECRET_KEY" to the setting.py of PRO2 app. Because of security reasons, 
we removed our specific secret key before pushing PRO2 into the repository. Your app won't
run without this key so you need to manually open the setting.py file (sitting in PRO2 folder)
and add a secret key (line 23). It could be any string you want, but we recommend a proper key,
e.g. you can make one using the random library in python:
```python
import random
''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
```

* You also need to comment out or remove line 172 and 173 of setting.py; these two lines set up the database 
of the app for deployment on [Heroku](https://www.heroku.com), but since we want to run PRO2 locally, 
we have to remove them:
```python
#Heroku setting:
#import dj_database_url
#DATABASES['default'] = dj_database_url.config()
```

* You need to turn on the "Debug" mode. You can do this easily by changing the line 26 of setting.py
from 
```python
DEBUG = False
```
to
```python
DEBUG = True
```


7. At the end, you need to make a database for PRO2. For doing this:

* First you need to 'migrate':
```
python manage.py migrate
```
(migration makes a new database named db.sqlite3 in your main directory)

* and then you need to import some results for PRO2 to show:
```
python PNsActivitiesImporter.py
```
(This script imports values in 'RawDataToImport' directory into the db.sqlite3 
database. The values in RawDataToImport are made by the R codes in "R (Calculations&Visualizations)"
folder of the repository)

#### Running PRO2
Before lunching PRO2, we recommend for you to make a new admin user for yourself 
(So you can log into PRO2 as an admin and/or user "Django admin site" of PRO2). 
You can make an admin account by:
```
python manage.py createsuperuser
```

Now you can lunch PRO2 by:
```
python manage.py runserver 9999
```
Now PRO2 is running locally on port 9999 (you can access it via your browser at http://127.0.0.1:9999)

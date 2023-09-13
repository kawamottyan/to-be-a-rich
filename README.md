article:https://qiita.com/kawa_mottyan/private/56497e3341c96c565386

# For running locally
clone repo
```python
git clone https://github.com/kawamottyan/to-get-rich.git  
```
change dir 
```python
cd to-get-rich
```
you need to have conda env(Im using miniforge)
and create new python env
```python
conda create -n to-get-rich python=3.8
```
activate python env

```python
conda activate to-get-rich
```
install packages
```python
pip install -r requirements.txt
```
finally run server
```python
python manage.py runserver
```
hope you run it with no issue

# Dir info
dataset/ : for making models  
keiba/ : for front and backend  
keiba_project/ : for djnago project  
.gitignore : for hiding secret keys  
Procfile : for heroku server  
db.sqlite3 : for database  
manage.py : for djnago project  
requirements.txt : for installing packages  
runtime.txt : for heroku server  

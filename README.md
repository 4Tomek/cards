**This is learning app using flashcards. Users can simply learn one-time, or they can use long-term learning, which is significantly more effective.**

## Quick Start - in your console:

- Clone the repository:
```
git clone https://github.com/4Tomek/cards.git
```
- Go into the repository and create virtual environment:
```
cd cards
python -m venv venv
```
- Activate scripts:
```
venv\Scripts\activate 
```
- Install dependencies:
```
pip install -r requirements.txt
```
- To migrate and fill tables into db.sqlite3 enter sequentially:
```
python manage.py makemigrations users
python manage.py migrate
python manage.py makemigrations textbooks
python manage.py migrate
```
- Run server:
```
python manage.py runserver
```
- Now the app runs in browser on: 
```
http://127.0.0.1:8000/
```
- If you want to use Django admin, you must create superuser:
```
python manage.py createsuperuser
```
- You can find detailed information about how this app works in the 'About' section of this app
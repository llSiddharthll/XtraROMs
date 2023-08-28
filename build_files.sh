echo "BUILD START"
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic
python3.9 manage.py makemigrations app
python3.9 manage.py makemigrations account
python3.9 manage.py makemigrations socialaccount
python3.9 manage.py migrate app
python3.9 manage.py migrate 
python3.9 manage.py migrate account
python3.9 manage.py migrate socialaccount
echo "BUILD DONE"
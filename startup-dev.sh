npm install
npm run build
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations core
python3 manage.py migrate core
python3 manage.py migrate
python3 manage.py createcachetable
npm run serve -- --port 3000 &
python3 manage.py runserver 0.0.0.0:80
# gunicorn ranker. wsgi -b 0.0.0.0:8000
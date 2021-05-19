release: python manage.py migrate
web: daphne ds2.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=ds2.settings -v2

release: flask --app patient.py db upgrade
release: flask --app medicine.py db upgrade
web: gunicorn patient:app
web: gunicorn medicine:app
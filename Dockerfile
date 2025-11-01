FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev

RUN pip install --no-cache-dir -r requirements.txt -v

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY . /app/

ENV PYTHONUNBUFFERED 1

CMD ["/wait-for-it.sh", "db:5432", "--timeout=30", "--", "bash", "-c", "python manage.py migrate && python loaddata.py && python manage.py runserver 0.0.0.0:8000"]



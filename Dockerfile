FROM python:3.11.5

WORKDIR /usr/src/apps

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["pushups.json"]

CMD ["python", "main.py"]

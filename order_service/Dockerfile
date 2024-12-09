FROM python:3.9-slim

# imposto la directory di lavoro
WORKDIR /app

# copio i file necessari
COPY . /app/

# installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "wsgi.py"]

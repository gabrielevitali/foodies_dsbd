FROM python:3.9-slim

RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
# aggiorna lista pacchetti
# installa comando ping
# elimina la cache di apt per ridurre le dimensioni dell'image

# imposto la directory di lavoro
WORKDIR /app

# copio i file necessari
COPY . /app/

# installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "flask", "run"]
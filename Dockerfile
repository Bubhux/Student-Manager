# Dockerfile
# Étape 1 : Utilisation de l'image Python 3.12 basée sur Debian Bullseye
FROM python:3.12-slim-bullseye

# Étape 2 : Installation des dépendances système pour MongoDB et Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev \
    gcc \
    wget \
    && wget -qO /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Configuration des variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Étape 3 : Configuration du répertoire de travail
WORKDIR /app

# Étape 4 : Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copie des fichiers de l'application
COPY . .

# Étape 6 : Commande par défaut
CMD ["sh", "-c", "pwd && ls -l /app && wait-for-it mongo:27017 -- python /app/main.py"]

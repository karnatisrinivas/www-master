# FROM ubuntu

# EXPOSE 80

# COPY app.py .
# COPY requirements.txt .
# COPY images/* images/
# COPY README.md .

# RUN apt-get update
# RUN apt-get install python3 python3-pip
# RUN pip install -r requirements.txt

# ENTRYPOINT ["python", "app.py"]


FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
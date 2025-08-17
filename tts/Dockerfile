FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg espeak-ng

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5002
CMD ["python", "app.py"]
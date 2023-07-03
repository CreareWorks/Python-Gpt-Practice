FROM python:3.11.1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
COPY . .

CMD [ "python", "src/main.py" ]

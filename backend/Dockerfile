FROM python:3.10

RUN mkdir -p /app
WORKDIR /app

COPY . .

ENV TOKEN="5488409861:AAHzpFNAAyDPehYJFcQN0oWisKdA3dHrkwQ"

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
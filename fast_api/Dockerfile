FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["fastapi" , "dev" , "main.py" , "--host" , "0.0.0.0", "--port" , "8000"]
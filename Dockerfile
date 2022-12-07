FROM python:3.10

WORKDIR /code
COPY . .
RUN pip3 install --no-cache-dir -r ./requirements.txt
CMD ["python3", "main.py"]
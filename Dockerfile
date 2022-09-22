FROM python:3
ENTRYPOINT ["python3", "/main.py"]

COPY . /
WORKDIR /

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x main.py
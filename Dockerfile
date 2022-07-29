FROM python:3.8
ENV PYTHONUNBUFFERED 1
COPY . /app
WORKDIR /app

RUN pip install  --use-deprecated=legacy-resolver --no-cache-dir -r ./requirements.txt \
    && chmod +x ./*.py
EXPOSE 9000
CMD ["./main.py"]

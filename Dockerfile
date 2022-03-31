# FROM python:3.7

# # Allows docker to cache installed dependencies between builds
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Mounts the application code to the image
# COPY . code
# WORKDIR /code

# EXPOSE 8000

# # runs the production server
# ENTRYPOINT ["python3", "manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]

FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip3 install --upgrade pip wheel
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt

COPY . code
EXPOSE 8000
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
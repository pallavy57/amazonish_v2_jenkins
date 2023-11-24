FROM python:3.6-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p amazonish
WORKDIR /amazonish
RUN pip install --upgrade pip
COPY . /amazonish
COPY ./amazonish/requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./amazonish/entrypoint.sh"]                     
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
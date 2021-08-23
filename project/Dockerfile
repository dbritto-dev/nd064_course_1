FROM python:2.7
WORKDIR /app
COPY ./techtrends/requirements.txt /app
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY ./techtrends /app
EXPOSE 3111
CMD [ "python", "init_db.py" ]
ENTRYPOINT [ "python", "app.py" ]
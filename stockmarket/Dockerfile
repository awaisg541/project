FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /stock_data
COPY req.txt /stock_data/
RUN pip install --upgrade pip
RUN pip install -r req.txt
COPY . /stock_data/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
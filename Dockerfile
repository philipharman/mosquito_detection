# Base image
FROM python:3.7

# Run Dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt


# Copy files
COPY data/output.npy /data/
COPY flask_app.py /

EXPOSE 80

CMD ["python", "flask_app.py"]

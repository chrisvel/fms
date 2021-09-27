FROM python:3.9.7-alpine
WORKDIR /msa
ADD . /msa
RUN pip install -r requirements.txt
CMD ["python","main.py"]
EXPOSE 5000
FROM  debian:latest
RUN pip3 install -U -r requirements.txt
CMD python3 register.py


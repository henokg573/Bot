FROM  debian:latest

RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-pip ffmpeg -y
RUN apt install -y git
RUN git clone https://github.com/henokg573/Bot.git
RUN cd Bot
WORKDIR /Bot
RUN pip3 install -U -r requirements.txt
CMD python3 register.py


FROM python:3.6

RUN pip3 install flask
RUN pip3 install opencv-python 
RUN pip3 install numpy 
RUN pip3 install color_transfer 
RUN pip3 install pillow

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev

COPY . .

EXPOSE 80

ENTRYPOINT ["python"] 
CMD ["server.py"]
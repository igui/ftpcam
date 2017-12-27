FROM python:3.6
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p files
VOLUME "files"
EXPOSE 2121
EXPOSE 30000-30512
COPY main.py ./
CMD ./main.py
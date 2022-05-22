FROM ubuntu:20.04

ENV TZ=US
ARG DEBIAN_FRONTEND=noninteractive

# installs npm, python3, and pip3
RUN apt update && apt install -y npm python3 python3-pip

# makes sure npm is up to date
RUN npm i npm@latest

# Sets the working directory to /code in the docker ubuntu image
WORKDIR /code
RUN ls /code

# Copys in the package.json, package-lock.json and requirements.txt files
# Uses these files to build the dependencies for the project
COPY package.json /code
COPY package-lock.json /code

# install npm project dependencies
RUN npm install

COPY requirements.txt /code

# install python project dependencies
RUN pip3 install -r requirements.txt

# Copies all the files now
COPY . /code

EXPOSE 8000

CMD ["bash", "./startup-dev.sh"]

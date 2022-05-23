FROM ubuntu:20.04

ENV TZ=US
ARG DEBIAN_FRONTEND=noninteractive

# installs python3, and pip3
RUN apt update -yq && apt-get upgrade -yq && apt install -y python3 python3-pip curl

# Install npm version 12
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -yq nodejs build-essential

# Sets the working directory to /code in the docker ubuntu image
WORKDIR /code
RUN ls /code

# Copys in the package.json, package-lock.json and requirements.txt files
# Uses these files to build the dependencies for the project
COPY package.json /code
COPY package-lock.json /code

# install npm project dependencies
RUN npm install .

COPY requirements.txt /code

# install python project dependencies
RUN pip3 install -r requirements.txt

# Copies all the files now
COPY . /code

EXPOSE 8000

CMD ["bash", "./startup-dev.sh"]

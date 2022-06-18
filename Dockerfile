# FROM node:latest

# # Sets the working directory to /code in the docker ubuntu image
# WORKDIR /code

# # Copys in the package.json, package-lock.json and requirements.txt files
# # Uses these files to build the dependencies for the project
# COPY package.json /code
# COPY package-lock.json /code

# # install npm project dependencies
# RUN npm install .
# RUN npm run build

FROM python:3.10.4

# Sets the working directory to /code in the docker ubuntu image
WORKDIR /code

COPY requirements.txt /code

RUN pip install --upgrade pip

# install python project dependencies
RUN pip3 install -r requirements.txt

# Copies all the files now
COPY . /code

CMD ["bash", "./startup-dev.sh"]

# Use the predefined node base image for this module.
FROM python:2.7

# Creating base "src" directory where the source repo will reside in our container.
# Code is copied from the host machine to this "src" folder in the container as a last step.
RUN mkdir /src
WORKDIR /src
# Lets first copy and install anything that changed with requirements.txt. If nothing changed in this file, the
# docker image cache will prevent re-installs if not necessary.
COPY requirements.txt /src

# Install python dependencies
RUN pip install -r /src/requirements.txt

# Now copy everything you need.
COPY . /src

# Our default command will start up the python web apps (GUI and producers).
CMD ["bash", "bin/start_services.sh"]

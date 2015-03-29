FROM ubuntu:14.04

# Install the packages we need for getting things done
RUN apt-get update && \
    apt-get install -y \
      build-essential \
      dos2unix \
      git \
    && \
    apt-get clean

# Install the packages we need for Pyramid
RUN apt-get update && \
    apt-get install -y \
      python3-pip \
    && \
    apt-get clean

# Install the Python packages we need
COPY requirements3.txt /tmp/requirements3.txt
RUN pip3 install -r /tmp/requirements3.txt && \
    rm /tmp/requirements3.txt

# Install our source
COPY tractdb_pyramid.py /tmp/tractdb_pyramid.py

# Port where Pyramid will listen
EXPOSE 8080

# Volume for secrets
VOLUME ["/secrets"]

# Our wrapper script
COPY run.sh /tmp/run.sh
RUN dos2unix /tmp/run.sh
RUN chmod a+x /tmp/run.sh

# Run the wrapper script
CMD ["/tmp/run.sh"]

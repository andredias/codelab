FROM pronusbox-base

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D && \
    echo 'deb https://apt.dockerproject.org/repo ubuntu-trusty main' > /etc/apt/sources.list.d/docker.list && \
    add-apt-repository -y ppa:chris-lea/uwsgi && \
    apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    uwsgi uwsgi-plugin-python3 python3 python3-pip \
    docker-engine

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y vim

WORKDIR /opt/codelab
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD codelab.wsgi .
ADD app app
ADD etc /etc

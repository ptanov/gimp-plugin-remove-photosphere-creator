FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y gimp gimp-plugin-registry

# Changes based on https://github.com/shangmu/docker.wine
# Without them (on Ubuntu 18.04) we will need to allow root@localhost to access X (xhost +SI:localuser:root) - this generally is not a good idea!
# btw vlc does not like running as root too (and will not run under root)

# Replace 1000 with your user / group id on your host system
RUN useradd -u 1000 -d /home/developer -m -s /bin/bash developer
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    mkdir -p /etc/sudoers.d && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

RUN mkdir /data
RUN chown developer:developer /data
ADD remove_photosphere_creator.py /home/developer/.gimp-2.8/plug-ins/
RUN chown developer:developer -R /home/developer/.gimp-2.8/

USER developer
ENV HOME /home/developer

WORKDIR /data

CMD ["gimp"]

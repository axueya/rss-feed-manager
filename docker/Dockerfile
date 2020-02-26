FROM tensorflow/tensorflow:1.12.3-gpu-py3
RUN echo Asia/Shanghai > /etc/timezone  &&  \
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN apt -y update && apt install -y vim
RUN pip install pqi&&pqi use aliyun && \
    pip install --upgrade pip && \
    pip install --default-timeout=1000 numpy\
                sklearn \
                keras \
                h5py \
                tqdm \
                jieba \
                gensim \
                spacy \
                jupyterlab \
                matplotlib \
                Flask \
                pandas==0.24.2 \
                flask_marshmallow==0.10.1 \
                SQLAlchemy==1.3.5 \
                Flask_RESTful==0.3.7 \
                Markdown==3.1.1 \
                marshmallow==3.3.0 \
                requests==2.22.0 \
                tomd==0.1.3 \
                schedule==0.6.0 \
                feedparser==5.2.1 \
                listparser==0.18 \
                Flask_SQLAlchemy==2.4.1 \
                Flask_And_Redis==1.0.0 \
                flask-jwt-extended
COPY jupyter_notebook_config.py /root/.jupyter/
ENV SHELL=/bin/bash
ENV LANG=C.UTF-8

WORKDIR /tmp
ADD start.sh /
RUN ["chmod", "+x", "/start.sh"]
ENTRYPOINT ["/start.sh"]

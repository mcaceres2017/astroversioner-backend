FROM python:3.11


#ARG REMOTE_REPO_LINK

# Add dvc repo.
#RUN wget \https://dvc.org/deb/dvc.list \-O /etc/apt/sources.list.d/dvc.list \
#    && wget -qO - https://dvc.org/deb/iterative.asc | gpg --dearmor > packages.iterative.gpg \
#    && install -o root -g root -m 644 packages.iterative.gpg /etc/apt/trusted.gpg.d/ \
#    && rm -f packages.iterative.gpg


# install dvc
#RUN apt-get update -y \ 
#    && apt install dvc -y

RUN apt-get update -y

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8003


CMD ["python", "main.py"]

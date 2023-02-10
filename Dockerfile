FROM python:3.10

# set a directory for the app
WORKDIR /usr/src

# copy dependencies
COPY ./README.md ./requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN echo "All python packages have been installed successfully"

# copy app files to the container
COPY ./app ./app

# run the command
EXPOSE 5005
CMD ["uvicorn", "app.main_v2:app", "--host", "0.0.0.0", "--port", "5005"]

# Select the base image
FROM  python:3.11

# Set the working directory
WORKDIR /code

# Copy the requirements file
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the source code
COPY ./app /code/app

ARG MONGO_CLIENT=mongodb+srv://user:contrasena_segura_2.0@realidad-aumentada.evjmu.mongodb.net/?retryWrites=true&w=majority&appName=realidad-aumentada
ARG SECRET_KEY=_D325b5q2wW7CJXDKoLIYA8VEi9E_LqMGH7zVevaaEc%
ARG CLIENT_DATABASE=clients
ARG RESEND_API_KEY=re_ZK39viaA_Fg24wxsmyeBgqkT2P8WccWFz

# Copy the dotenv file
COPY ./.env /code/.env

COPY ./main.py /code/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
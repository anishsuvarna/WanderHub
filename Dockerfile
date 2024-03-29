FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# Removes output stream buffering, allowing for more efficient logging
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY tiara_23_backend $APP_HOME/tiara_23_backend/

# Copy local code to the container image.
COPY . .

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 Tourist_destination_recommendation_System.wsgi:application
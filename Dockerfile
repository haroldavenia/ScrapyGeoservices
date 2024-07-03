# Use an official Python runtime as a parent image
FROM python:3.10.6
# Set the working directory in the container
WORKDIR /usr/src/geotwitter
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
# Download the spaCy model
RUN python -m spacy download en_core_web_lg
# Copy the current directory contents into the container at /usr/src/app
COPY src src
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/geotwitter"
# Copy the current directory contents into the container at
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 \
            CMD curl -f http://localhost:5000/health || exit 1
ENTRYPOINT ["python", "./src/app.py"]


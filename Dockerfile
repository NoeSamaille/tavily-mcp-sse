# Use the official Red Hat UBI 9 image with Python 3.12
FROM registry.access.redhat.com/ubi9/python-312:1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the command to start the development server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

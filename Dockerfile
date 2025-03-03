# Use an appropriate base image
FROM engineervix/python-latex:3.12-slim-bookworm

# Install any dependencies (e.g., if it's a Python app)
RUN apt-get update && apt-get install -y make && pip install pyyaml

# Set the working directory inside the container
WORKDIR /app

# Copy your application code (if applicable)
COPY . /app

# Specify the entrypoint for the container (adjust as per your application)
CMD ["python3", "generator.py", "/app/config.yaml", "/app/students_list.csv", "/app/database","/app/output"]

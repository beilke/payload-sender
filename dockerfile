# Use official Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5001 for Flask
EXPOSE 5001

# Run the application
CMD ["python", "send_payload.py"]

FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Initialize database with mock data
RUN python reset_database.py

# Expose port
EXPOSE 5002

# Run the application
CMD ["python", "app.py"]

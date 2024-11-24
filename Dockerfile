FROM python:3.11-alpine

# Set up environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY . .
COPY requirements.txt .
#COPY lib/ .

# Install dependencies
RUN pip install --no-cache-dir lib/osdbaccess-1.0-py2.py3-none-any.whl
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Expose the port your application will run on
EXPOSE 8080

# Specify the command to run on container start
CMD ["python", "src/app.py"]


FROM python:3.11

# Update apt and install build tools for C++ and Java
RUN apt-get update && \
    apt-get install -y gcc g++

WORKDIR /app

# Upgrade pip for smoother installs
RUN pip install --upgrade pip

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole Django project code
COPY . .

# Expose port (for Django dev server)
EXPOSE 8000

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=oj_project.settings
ENV PYTHONUNBUFFERED=1

# Command to run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy dependencies first (better for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 80 (inside container)
EXPOSE 8000

# Run the app with uvicorn (exec form)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
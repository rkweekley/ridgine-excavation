FROM python:3.11-slim

WORKDIR /app

# Install Flask + gunicorn
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app + static site
COPY app.py .
COPY static/ ./static/

# Run as non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
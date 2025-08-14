FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

COPY . /app

EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

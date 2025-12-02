# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /backend

COPY requirements.txt .

# Install system packages that provide mariadb_config and build tools,
# then install Python requirements and clean up apt lists.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential gcc g++ \
      libmariadb-dev libmariadb-dev-compat default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


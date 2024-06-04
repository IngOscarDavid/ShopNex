FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# RUN python -m venv venv

# RUN /bin/bash -c "source .\venv\Scripts\activate"

RUN pip install fastapi
RUN pip install uvicorn
RUN pip install mysql
RUN pip install mysqlclient

COPY . .

EXPOSE 8000

# Comando de inicio para ejecutar la aplicación FastAPI
CMD ["uvicorn", "main:App", "--host", "0.0.0.0", "--port", "8000"]

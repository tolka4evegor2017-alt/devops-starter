FROM python:3.12-slim
WORKDIR /app
RUN echo 'print("Hello DevOps")' > app.py
CMD ["python", "app.py"]

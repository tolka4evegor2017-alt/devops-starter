import pytest
import sys
import os

# Добавляем корневую папку проекта в путь поиска
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    # Отключаем реальное подключение к БД для тестов
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello DevOps!"}

def test_app_starts():
    """Тест что приложение вообще запускается"""
    assert app is not None
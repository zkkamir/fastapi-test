from fastapi import status
from fastapi.testclient import TestClient

from todo import main


client = TestClient(main.app)


def test_return_health_check():
    response = client.get('/health_check')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}

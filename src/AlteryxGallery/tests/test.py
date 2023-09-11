import pytest
from unittest.mock import patch
from AlteryxGallery import Gallery
import json

@pytest.fixture
def gallery():
    return Gallery(api_location='https://example.com', api_key='key', api_secret='secret')

@patch('gallery.requests.get')
def test_subscription(mock_get, gallery):
    mock_response = {'workflows': [{'id': 1, 'name': 'workflow1'}, {'id': 2, 'name': 'workflow2'}]}
    mock_get.return_value.status_code = 200
    mock_get.return_value.content.decode.return_value = json.dumps(mock_response)

    response, content = gallery.subscription()

    assert response.status_code == 200
    assert content == mock_response
import pytest
from unittest.mock import patch

import httpx
from AlteryxGallery import AlteryxGalleryAPI
import json

@pytest.fixture
def gallery():
    return AlteryxGalleryAPI.Gallery(api_location='https://example.com', api_key='key', api_secret='secret')

@patch('gallery.httpx.get')
def test_subscription(mock_get, gallery: AlteryxGalleryAPI.Gallery):
    mock_response = {'workflows': [{'id': 1, 'name': 'workflow1'}, {'id': 2, 'name': 'workflow2'}]}
    mock_get.return_value.status_code = 200
    mock_get.return_value.content.decode.return_value = json.dumps(mock_response)

    response, content = gallery.subscription()

    assert response.status_code == 200
    assert content == mock_response

# FILEPATH: /home/fatpunk/AlteryxGalleryAPI/src/tests/test_gallery_connection.py

@pytest.fixture
def gallery():
    return AlteryxGalleryAPI.Gallery(api_location='https://example.com', api_key='key', api_secret='secret')

@patch('AlteryxGalleryAPI.Gallery.httpx.get')
@patch('builtins.open', new_callable=mock_open)
def test_get_app(mock_file, mock_get, gallery: AlteryxGalleryAPI.Gallery):
    app_id = '123'
    app_name = 'test_app'
    mock_response = httpx.Response()
    mock_response.status_code = 200
    mock_response._content = b'test content'
    mock_get.return_value = mock_response

    file_path = gallery.get_app(app_id, app_name)

    assert file_path == f"{app_name}.yxzp"
    mock_file.assert_called_once_with(f"{app_name}.yxzp", 'wb')
    handle = mock_file()
    handle.write.assert_called_once_with(b'test content')
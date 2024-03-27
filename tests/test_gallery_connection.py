import pytest
import os
from dotenv import load_dotenv

from AlteryxGallery import AlteryxGalleryAPI

load_dotenv()

# Fixture to initialize the HTTPX client
@pytest.fixture(scope="module")
def http_client():
    base_url = os.getenv("BASE_URL")
    with AlteryxGalleryAPI.GalleryClient(base_url) as client:
        client.client_id = os.getenv("CLIENT_ID")
        client.client_secret = os.getenv("CLIENT_SECRET")
        yield client

# Test case for the authenticate method
def test_authenticate(http_client: AlteryxGalleryAPI.GalleryClient):
    # Test successful authentication
    assert http_client.authenticate(http_client.client_id, http_client.client_secret) == True

    # Test unsuccessful authentication
    assert http_client.authenticate("incorrect_username", "incorrect_password") == False

# Test case for the get_all_workflows method
def test_get_all_workflows(http_client: AlteryxGalleryAPI.GalleryClient):
    response, content = http_client.get_all_workflows(name="00-Octopus Download Pipeline")
    assert response.status_code == 200
    assert content[0]["name"] == "00-Octopus Download Pipeline"
    assert len(content[0]["name"]) > 0
    
    response, content = http_client.get_all_workflows(name="Non-existent Workflow")
    assert response.status_code == 200
    assert len(content) == 0

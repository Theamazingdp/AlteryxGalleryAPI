from http import client
import pytest
from AlteryxGallery import AlteryxGalleryAPI
import os
from dotenv import load_dotenv

load_dotenv()

# Fixture to initialize the HTTPX client
@pytest.fixture(scope="module")
def http_client():
    base_url = os.getenv("BASE_URL")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    with AlteryxGalleryAPI.GalleryClient(base_url) as client:
        client.client_id = client_id
        client.client_secret = client_secret
        yield client

# Test case for the authenticate method
def test_authenticate(http_client):
    # Test successful authentication
    assert http_client.authenticate(http_client.client_id, http_client.client_secret) == True

    # Test unsuccessful authentication
    assert http_client.authenticate("incorrect_username", "incorrect_password") == False

# Test case for the get_all_workflows method
def test_get_all_workflows(http_client):
    response, content = http_client.get_all_workflows(name="00-Octopus Download Pipeline")
    assert response.status_code == 200
    assert content[0]["name"] == "00-Octopus Download Pipeline"
    assert len(content[0]["name"]) > 0
    
    response, content = http_client.get_all_workflows(name="Non-existent Workflow")
    assert response.status_code == 200
    # assert content["name"] == "Non-existent Workflow"
    assert len(content["name"]) == 0

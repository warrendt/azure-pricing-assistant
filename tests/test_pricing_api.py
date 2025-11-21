import pytest
from unittest.mock import patch, MagicMock
from src.utils.pricing_api import get_azure_price
import requests

@patch("src.utils.pricing_api.requests.get")
def test_get_azure_price_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"Items": [{"retailPrice": 0.176}]}
    mock_get.return_value = mock_resp
    price = get_azure_price("Virtual Machines", "Standard_D2s_v3", "eastus")
    assert price == 0.176

@patch("src.utils.pricing_api.requests.get")
def test_get_azure_price_empty_results(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"Items": []}
    mock_get.return_value = mock_resp
    price = get_azure_price("Virtual Machines", "Standard_D2s_v3", "eastus")
    assert price == 0.0

@patch("src.utils.pricing_api.requests.get")
def test_get_azure_price_retry_then_success(mock_get):
    timeout_exc = requests.Timeout("Timeout")
    mock_success = MagicMock()
    mock_success.status_code = 200
    mock_success.json.return_value = {"Items": [{"retailPrice": 0.2}]}
    mock_get.side_effect = [timeout_exc, mock_success]
    price = get_azure_price("Azure App Service", "P1v2", "eastus")
    assert price == 0.2
    assert mock_get.call_count == 2

@patch("src.utils.pricing_api.requests.get")
def test_get_azure_price_invalid_price(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"Items": [{"retailPrice": None}]}
    mock_get.return_value = mock_resp
    price = get_azure_price("SQL Database", "S1", "eastus")
    assert price == 0.0

@patch("src.utils.pricing_api.requests.get")
def test_get_azure_price_transient_status(mock_get):
    # First transient 500 then success
    mock_fail = MagicMock(); mock_fail.status_code = 500; mock_fail.json.return_value = {}
    mock_success = MagicMock(); mock_success.status_code = 200; mock_success.json.return_value = {"Items": [{"retailPrice": 0.3}]}
    mock_get.side_effect = [mock_fail, mock_success]
    price = get_azure_price("Blob Storage", "Standard_LRS", "eastus")
    assert price == 0.3

@patch("src.utils.pricing_api.requests.get")
def test_get_azure_price_retry_exhausted(mock_get):
    mock_get.side_effect = requests.Timeout("Timeout")
    price = get_azure_price("Virtual Machines", "Standard_D2s_v3", "eastus")
    assert price == 0.0

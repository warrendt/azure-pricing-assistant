import os
import pytest
from src.utils.pricing_api import get_azure_price

LIVE_SKUS = [
    ("Virtual Machines", "Standard_M16-4ms", "eastus"),
    ("Azure App Service", "P0v3", "eastus"),
    ("SQL Database", "14 vCore", "eastus"),
]

@pytest.mark.skipif(os.getenv("LIVE_TESTS") != "1", reason="Set LIVE_TESTS=1 to run live pricing API tests")
def test_live_prices_positive():
    failures = []
    for service, sku, region in LIVE_SKUS:
        price = get_azure_price(service, sku, region)
        if price <= 0.0:
            failures.append(f"{service} {sku} {region} returned {price}")
    assert not failures, f"Live pricing failures: {failures}" 

"""Azure Retail Prices API utility.

Implements get_azure_price(service_name, sku_name, region) -> float
following Phase 2 specifications.
"""
from __future__ import annotations
import requests
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

AZURE_PRICES_ENDPOINT = "https://prices.azure.com/api/retail/prices"

def get_azure_price(service_name: str, sku_name: str, region: str) -> float:
    """Get Azure retail hourly price for a service SKU in a region.

    Args:
        service_name: Exact Azure serviceName (e.g. "Virtual Machines")
        sku_name: skuName (e.g. "Standard_D2s_v3", "P1v2", "S1")
        region: armRegionName (e.g. "eastus")

    Returns:
        Hourly retail price as float, or 0.0 if not found / error.
    """
    filter_expr = (
        f"serviceName eq '{service_name}' and (skuName eq '{sku_name}' or armSkuName eq '{sku_name}') and armRegionName eq '{region}'"
    )
    params = {"$filter": filter_expr}

    attempt = 0
    delay = 0.5  # initial backoff seconds
    max_attempts = 2  # one retry per spec

    while attempt < max_attempts:
        try:
            logger.info("Pricing API request: %s", filter_expr)
            resp = requests.get(AZURE_PRICES_ENDPOINT, params=params, timeout=10)
            if resp.status_code in (429, 500, 503):
                raise requests.RequestException(f"Transient status code {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            items = data.get("Items") or data.get("items") or []
            if not items:
                logger.warning("No pricing Items found for filter: %s", filter_expr)
                return 0.0
            first = items[0]
            price = first.get("retailPrice") or first.get("unitPrice")
            if price is None:
                logger.warning("Pricing item missing retailPrice: %s", first)
                return 0.0
            try:
                return float(price)
            except (TypeError, ValueError):
                logger.error("Invalid price value: %r", price)
                return 0.0
        except (requests.Timeout, requests.RequestException) as e:
            attempt += 1
            logger.warning("Pricing API error (attempt %d/%d): %s", attempt, max_attempts, e)
            if attempt >= max_attempts:
                return 0.0
            time.sleep(delay)
            delay *= 2  # exponential backoff
        except Exception as e:  # unexpected parsing/network error
            logger.error("Unexpected error querying pricing API: %s", e)
            return 0.0
    return 0.0

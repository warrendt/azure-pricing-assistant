# API Specifications

## Azure Retail Prices API

### Endpoint
```
https://prices.azure.com/api/retail/prices
```

### Authentication
None required (public API)

### Method
GET

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `api-version` | string | No | API version (e.g., `2023-01-01-preview`) |
| `currencyCode` | string | No | Currency code (default: USD) |
| `$filter` | string | No | OData filter expression |

### OData Filter Examples

**Filter by service and region:**
```
$filter=serviceName eq 'Virtual Machines' and armRegionName eq 'eastus'
```

**Filter by service, SKU, and region:**
```
$filter=serviceName eq 'Virtual Machines' and skuName eq 'Standard_D2s_v3' and armRegionName eq 'eastus'
```

**Filter by service family:**
```
$filter=serviceFamily eq 'Compute'
```

**Multiple conditions:**
```
$filter=serviceName eq 'Virtual Machines' and priceType eq 'Consumption' and armRegionName eq 'eastus'
```

### Response Schema

```json
{
  "BillingCurrency": "USD",
  "CustomerEntityId": "Default",
  "CustomerEntityType": "Retail",
  "Items": [
    {
      "currencyCode": "USD",
      "tierMinimumUnits": 0,
      "retailPrice": 0.176,
      "unitPrice": 0.176,
      "armRegionName": "eastus",
      "location": "US East",
      "effectiveStartDate": "2020-08-01T00:00:00Z",
      "meterId": "00000000-0000-0000-0000-000000000000",
      "meterName": "D2s v3",
      "productId": "DZH318Z0BQPS",
      "skuId": "DZH318Z0BQPS/00TG",
      "productName": "Virtual Machines Dsv3 Series",
      "skuName": "D2s v3",
      "serviceName": "Virtual Machines",
      "serviceId": "DZH313Z7MMC8",
      "serviceFamily": "Compute",
      "unitOfMeasure": "1 Hour",
      "type": "Consumption",
      "isPrimaryMeterRegion": true,
      "armSkuName": "Standard_D2s_v3"
    }
  ],
  "NextPageLink": "https://prices.azure.com/api/retail/prices?$skip=100",
  "Count": 1
}
```

### Key Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `retailPrice` | number | Pay-as-you-go retail price per unit |
| `unitPrice` | number | Same as retailPrice |
| `unitOfMeasure` | string | Pricing unit (e.g., "1 Hour", "1 GB/Month") |
| `serviceName` | string | Azure service name |
| `skuName` | string | SKU display name |
| `armSkuName` | string | ARM SKU identifier |
| `armRegionName` | string | ARM region code (e.g., "eastus") |
| `location` | string | Human-readable location (e.g., "US East") |
| `type` | string | Price type: "Consumption", "Reservation", etc. |

### Pagination

API returns maximum 100 items per page. Use `NextPageLink` for additional results.

```python
# Example: Handle pagination
url = "https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Virtual Machines'"
while url:
    response = requests.get(url)
    data = response.json()
    items = data.get("Items", [])
    # Process items...
    url = data.get("NextPageLink")
```

### Common Service Names

| Service Name | Description |
|--------------|-------------|
| `Virtual Machines` | Azure Virtual Machines |
| `Azure App Service` | Web app hosting |
| `Storage` | Blob, File, Queue, Table storage |
| `SQL Database` | Azure SQL Database |
| `Azure Cosmos DB` | Cosmos DB NoSQL database |
| `Azure Database for MySQL` | MySQL PaaS |
| `Azure Database for PostgreSQL` | PostgreSQL PaaS |
| `Functions` | Azure Functions serverless |
| `Azure Kubernetes Service` | AKS managed Kubernetes |
| `Load Balancer` | Azure Load Balancer |
| `VPN Gateway` | VPN Gateway |
| `Application Gateway` | Application Gateway |

### Common ARM Region Names

| ARM Region | Location |
|------------|----------|
| `eastus` | East US |
| `eastus2` | East US 2 |
| `westus` | West US |
| `westus2` | West US 2 |
| `centralus` | Central US |
| `northcentralus` | North Central US |
| `southcentralus` | South Central US |
| `westcentralus` | West Central US |
| `canadacentral` | Canada Central |
| `canadaeast` | Canada East |
| `brazilsouth` | Brazil South |
| `northeurope` | North Europe |
| `westeurope` | West Europe |
| `uksouth` | UK South |
| `ukwest` | UK West |
| `francecentral` | France Central |
| `germanywestcentral` | Germany West Central |
| `norwayeast` | Norway East |
| `switzerlandnorth` | Switzerland North |
| `swedencentral` | Sweden Central |
| `southeastasia` | Southeast Asia |
| `eastasia` | East Asia |
| `australiaeast` | Australia East |
| `australiasoutheast` | Australia Southeast |
| `japaneast` | Japan East |
| `japanwest` | Japan West |
| `koreacentral` | Korea Central |
| `southindia` | South India |
| `centralindia` | Central India |
| `westindia` | West India |

### Error Handling

**No Results Found:**
```json
{
  "Items": [],
  "Count": 0
}
```

**HTTP Error Codes:**
- `400 Bad Request`: Invalid filter syntax
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: API error

### Rate Limits

No official documented rate limits, but recommended to:
- Implement exponential backoff for retries
- Cache results when possible
- Batch requests when feasible

### Example Python Implementation

```python
import requests
from typing import Optional

def get_azure_price(
    service_name: str,
    sku_name: str,
    region: str
) -> Optional[float]:
    """
    Get Azure retail price for a specific service SKU in a region.
    
    Args:
        service_name: Azure service name (e.g., "Virtual Machines")
        sku_name: SKU name (e.g., "Standard_D2s_v3")
        region: ARM region code (e.g., "eastus")
    
    Returns:
        Retail price per hour (or None if not found)
    """
    url = "https://prices.azure.com/api/retail/prices"
    
    # Construct OData filter
    filter_expr = (
        f"serviceName eq '{service_name}' and "
        f"skuName eq '{sku_name}' and "
        f"armRegionName eq '{region}'"
    )
    
    params = {
        "$filter": filter_expr
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("Items", [])
        
        if items:
            # Return first result's retail price
            return items[0].get("retailPrice")
        else:
            print(f"No pricing found for {service_name} / {sku_name} / {region}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return None
```

---

## Microsoft Agent Framework APIs

### Create Agent (Azure AI Foundry)

```python
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async with AzureCliCredential() as credential:
    client = AzureAIAgentClient(async_credential=credential)
    
    agent = await client.create_agent(
        name="MyAgent",
        instructions="You are a helpful assistant.",
        model_deployment_name="gpt-4o-mini"  # Optional
    )
```

### HandoffBuilder Workflow

```python
from agent_framework import HandoffBuilder

workflow = (
    HandoffBuilder(
        name="my_handoff",
        participants=[coordinator_agent, specialist_agent]
    )
    .set_coordinator("coordinator_agent")
    .with_termination_condition(lambda conv: len(conv) > 10)
    .build()
)

# Run workflow
async for event in workflow.run_stream("Initial message"):
    if isinstance(event, RequestInfoEvent):
        # Handle user input request
        user_input = input("You: ")
        async for response_event in workflow.send_responses_streaming({event.request_id: user_input}):
            # Process response events
            pass
```

### SequentialBuilder Workflow

```python
from agent_framework import SequentialBuilder

workflow = SequentialBuilder().participants([
    agent1,
    agent2,
    agent3
]).build()

# Run workflow
async for event in workflow.run_stream("Input message"):
    if isinstance(event, WorkflowCompletedEvent):
        result = event.data  # List of ChatMessage objects
```

### Event Types

```python
from agent_framework import (
    RequestInfoEvent,        # User input needed
    WorkflowCompletedEvent,  # Workflow finished
    AgentRunUpdateEvent,     # Agent streaming response
    WorkflowStatusEvent      # Workflow state change
)
```

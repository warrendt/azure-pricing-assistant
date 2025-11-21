import unittest
from unittest.mock import patch, MagicMock
from src.agents.pricing_agent import create_pricing_agent

class TestPricingAgent(unittest.TestCase):

    @patch('src.agents.pricing_agent.requests.get')
    def test_fetch_pricing_data_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'items': [
                {'serviceName': 'Virtual Machines', 'sku': 'Standard_D2s_v3', 'unitPrice': 100.00},
                {'serviceName': 'SQL Database', 'sku': 'Standard_S0', 'unitPrice': 50.00}
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Create the pricing agent
        agent = create_pricing_agent(MagicMock())
        result = agent

        # Check the result
        self.assertEqual(len(result['items']), 2)
        self.assertEqual(result['total_monthly'], 150.00)

    @patch('src.agents.pricing_agent.requests.get')
    def test_fetch_pricing_data_failure(self, mock_get):
        # Mock a failed API response
        mock_get.side_effect = Exception('API request failed')

        # Create the pricing agent
        agent = create_pricing_agent(MagicMock())
        result = agent

        # Check the error message
        self.assertIn('error', result)
        self.assertEqual(result['message'], 'Failed to fetch pricing data.')

if __name__ == '__main__':
    unittest.main()
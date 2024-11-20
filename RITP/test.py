import unittest
import requests

class TestAssets(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"  # Replace with your actual base URL

    def test_get_asset_by_valid_id(self):
        """Test case for retrieving an asset with a valid ID"""
        test_asset_id = 3  # Replace with a valid asset ID from your database
        response = requests.get(f"{self.BASE_URL}/GetAssetById/{test_asset_id}")
        
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Validate the response structure
        data = response.json()
        self.assertIn("asset_id", data)
        self.assertIn("name", data)
        self.assertIn("type", data)
        self.assertIn("value", data)
        self.assertIn("criticality", data)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_get_asset_by_invalid_id(self):
        """Test case for retrieving an asset with an invalid ID"""
        test_asset_id = 9999  # Use an ID that doesn't exist
        response = requests.get(f"{self.BASE_URL}/GetAssetById/{test_asset_id}")
        
        # Check if the response status code is 404
        self.assertEqual(response.status_code, 404)
        
        # Validate the error message
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Asset not found")
    def test_get_asset_risk_by_valid_id(self):
        """Test case for retrieving an asset risk with a valid ID"""
        test_asset_risk_id = 1  # Replace with a valid asset risk ID from your database
        response = requests.get(f"{self.BASE_URL}/GetAssetRiskById/{test_asset_risk_id}")
        
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Validate the response structure
        data = response.json()
        self.assertIn("risk_id", data)
        self.assertIn("asset_id", data)
        self.assertIn("risk_score", data)
        self.assertIn("risk_description", data)
        self.assertIn("threat_level", data)
        self.assertIn("last_evaluation", data)

    def test_get_asset_risk_by_invalid_id(self):
        """Test case for retrieving an asset risk with an invalid ID"""
        test_asset_risk_id = 9999  # Use an ID that doesn't exist
        response = requests.get(f"{self.BASE_URL}/GetAssetRiskById/{test_asset_risk_id}")
        
        # Check if the response status code is 404
        self.assertEqual(response.status_code, 404)
        
        # Validate the error message
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Asset risk not found")
    def test_add_asset(self):
        """Test case for adding a new asset"""
        payload = {
            "name": "Asset1",
            "type": "Hardware",
            "value": 1000.0,
            "criticality": "high"
        }
        response = requests.post(f"{self.BASE_URL}/addAssets", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("success", data)
        self.assertIn("asset_id", data)
    def test_get_all_assets(self):
        """Test case for retrieving all assets"""
        response = requests.get(f"{self.BASE_URL}/GetAssets")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    def test_update_asset(self):
        """Test case for updating an asset"""
        test_asset_id = 3  # Replace with a valid asset ID
        payload = {"value": 2000.0}
        response = requests.put(f"{self.BASE_URL}/updateAsset/{test_asset_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("success", data)
    def test_add_asset_risk(self):
        """Test case for adding a risk to an asset"""
        payload = {
            "asset_id": 3,  # Replace with a valid asset ID
            "risk_score": 5,
            "risk_description": "Risk description example",
            "threat_level": "high"
        }
        response = requests.post(f"{self.BASE_URL}/addAssetsRisks", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("success", data)
        self.assertIn("new_assetRisk", data)
    def test_get_all_asset_risks(self):
        """Test case for retrieving all asset risks"""
        response = requests.get(f"{self.BASE_URL}/GetAssetRisks")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_delete_asset_not_found(self):
        """Test case for deleting an asset with an invalid ID"""
        test_asset_id = 9999  # Use an ID that doesn't exist
        response = requests.delete(f"{self.BASE_URL}/deleteAsset/{test_asset_id}")
        
        # Check if the response status code is 404
        self.assertEqual(response.status_code, 404)
        
        # Validate the error message
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Asset not found")

if __name__ == "__main__":
    unittest.main()

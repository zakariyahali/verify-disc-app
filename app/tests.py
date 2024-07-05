import unittest
from fastapi.testclient import TestClient

import logging

from app.main import app
from app.services.pdf_service_dummy import PdfService
from app.services.discrepancy_service import compare_dictionaries
from app.database import database_v1_dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestCompareDictionaries(unittest.TestCase):
    def test_compare_identical_dicts(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'a': 1, 'b': 2}
        result = compare_dictionaries(dict1, dict2)
        logger.info(f"Result of comparing identical dicts: {result}")
        self.assertEqual(result["Number of different values: "], 0)
        self.assertEqual(result["only_in_dict1"], {})
        self.assertEqual(result["only_in_dict2"], {})
        self.assertEqual(result["different_values"], {})

    def test_compare_different_dicts(self):
        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {'a': 1, 'b': 3}
        result = compare_dictionaries(dict1, dict2)
        logger.info(f"Result of comparing different dicts: {result}")
        self.assertEqual(result["Number of different values: "], 1)
        self.assertEqual(result["only_in_dict1"], {'c': 3})
        self.assertEqual(result["only_in_dict2"], {})
        self.assertEqual(result["different_values"], {'b': (2, 3)})

    def test_compare_with_type_conversion(self):
        dict1 = {'a': '1.0', 'b': '2.0'}
        dict2 = {'a': 1.0, 'b': 2}
        result = compare_dictionaries(dict1, dict2)
        logger.info(f"Result of comparing dicts with type conversion: {result}")
        self.assertEqual(result["Number of different values: "], 0)

class TestPdfService(unittest.TestCase):
    def setUp(self):
        self.pdf_service = PdfService(key="TEST_KEY")

    def test_extract_healthinc(self):
        result = self.pdf_service.extract("assets/healthinc.pdf")
        logger.info(f"Extracted data from healthinc.pdf: {result}")
        self.assertEqual(result['Company Name'], 'HealthInc')
        self.assertEqual(result['Industry'], 'Healthcare')

    def test_extract_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            self.pdf_service.extract("assets/invalid.pdf")
        logger.info("FileNotFoundError raised as expected for invalid file")

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_status(self):
        response = self.client.get("/status")
        logger.info(f"Response from GET /status: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Service status": "Running", "Database status": "DB content is available"})

    def test_read_status_empty_db(self):
        # Simulate an empty database scenario
        original_db = database_v1_dict.copy()
        database_v1_dict.clear()
        response = self.client.get("/status")
        logger.info(f"Response from GET /status with empty database: {response.json()}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Database is empty"})
        database_v1_dict.update(original_db)

    def test_convert_valid_pdf(self):
        response = self.client.post("/convert", json={"file_path": "assets/healthinc.pdf"})
        logger.info(f"Response from POST /convert with valid PDF: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("discrepancies", response.json())

    def test_convert_valid_pdf_alternative(self):
        response = self.client.post("/convert", json={"file_path": "assets/financellc.pdf"})
        logger.info(f"Response from POST /convert with valid PDF: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("discrepancies", response.json())

    def test_convert_invalid_pdf(self):
        response = self.client.post("/convert", json={"file_path": "assets/invalid.pdf"})
        logger.info(f"Response from POST /convert with invalid PDF: {response.status_code}, {response.text}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Cannot extract data. Invalid file provided."})

    def test_convert_unknown_company(self):
        response = self.client.post("/convert", json={"file_path": "assets/healthinc.pdf"})
        # Simulate an unknown company scenario
        original_db = database_v1_dict.copy()
        database_v1_dict.pop('HealthInc')
        response = self.client.post("/convert", json={"file_path": "assets/healthinc.pdf"})
        logger.info(f"Response from POST /convert with unknown company: {response.json()}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Company not found in database"})
        database_v1_dict.update(original_db)

if __name__ == '__main__':
    unittest.main()
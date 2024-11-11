#!/usr/bin/python3
"""
Contains the TestCityDocs classes
"""

from datetime import datetime
import inspect
from api.v1.app import app
from models.state import State
import models
from models.city import City
from models.base_model import BaseModel
import pycodestyle as pep8
from models import storage
import unittest


class TestCityDocs(unittest.TestCase):
    """Tests to check the documentation and style of City class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.city_f = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance_city(self):
        """Test that models/city.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_city(self):
        """Test that tests/test_models/test_city.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_city_module_docstring(self):
        """Test for the city.py module docstring"""
        self.assertIsNot(city.__doc__, None,
                         "city.py needs a docstring")
        self.assertTrue(len(city.__doc__) >= 1,
                        "city.py needs a docstring")

    def test_city_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(City.__doc__, None,
                         "City class needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1,
                        "City class needs a docstring")

    def test_city_func_docstrings(self):
        """Test for the presence of docstrings in City methods"""
        for func in self.city_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestCity(unittest.TestCase):
    """Test the City class"""
    def test_is_subclass(self):
        """Test that City is a subclass of BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_name_attr(self):
        """Test that City has attribute name, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        if models.storage_t == 'db':
            self.assertEqual(city.name, None)
        else:
            self.assertEqual(city.name, "")

    def test_state_id_attr(self):
        """Test that City has attribute state_id, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        if models.storage_t == 'db':
            self.assertEqual(city.state_id, None)
        else:
            self.assertEqual(city.state_id, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        c = City()
        new_d = c.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in c.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        c = City()
        new_d = c.to_dict()
        self.assertEqual(new_d["__class__"], "City")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], c.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], c.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))


class TestCityAPI(unittest.TestCase):
    """Test API endpoints related to City"""

    @classmethod
    def setUpClass(cls):
        """Set up Flask test client and other test resources"""
        app.testing = True
        cls.client = app.test_client()

    def setUp(self):
        """Set up test context and initialize data for each test"""
        self.ctx = app.app_context()
        self.ctx.push()
        storage.reload()

        # Create a state to use in tests
        self.state = State(name="TestState")
        storage.new(self.state)
        storage.save()

    def tearDown(self):
        """Tear down test context and remove created data"""
        storage.delete(self.state)
        storage.save()
        self.ctx.pop()

    def test_get_cities_by_state(self):
        """Test GET /api/v1/states/<state_id>/cities"""
        response = self.client.get(f"/api/v1/states/{self.state.id}/cities")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 0)

    def test_get_city(self):
        """Test GET /api/v1/cities/<city_id>"""
        city = City(name="TestCity", state_id=self.state.id)
        storage.new(city)
        storage.save()

        response = self.client.get(f"/api/v1/cities/{city.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "TestCity")

        # Clean up
        storage.delete(city)
        storage.save()

    def test_delete_city(self):
        """Test DELETE /api/v1/cities/<city_id>"""
        city = City(name="TestCityToDelete", state_id=self.state.id)
        storage.new(city)
        storage.save()

        response = self.client.delete(f"/api/v1/cities/{city.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

        # Ensure city was deleted
        response = self.client.get(f"/api/v1/cities/{city.id}")
        self.assertEqual(response.status_code, 404)

    def test_create_city(self):
        """Test POST /api/v1/states/<state_id>/cities"""
        headers = {"Content-Type": "application/json"}
        data = {"name": "NewCity"}

        response = self.client.post(
            f"/api/v1/states/{self.state.id}/cities",
            json=data,
            headers=headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "NewCity")
        self.assertEqual(response.json["state_id"], self.state.id)

    def test_create_city_missing_name(self):
        """Test POST /api/v1/states/<state_id>/cities with missing 'name'"""
        headers = {"Content-Type": "application/json"}
        response = self.client.post('/api/v1/states', json={}, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing name", response.get_json().get("error"))

    def test_update_city(self):
        """Test PUT /api/v1/cities/<city_id>"""
        city = City(name="OldCity", state_id=self.state.id)
        storage.new(city)
        storage.save()

        headers = {"Content-Type": "application/json"}
        data = {"name": "UpdatedCity"}

        response = self.client.put(
            f"/api/v1/cities/{city.id}",
            json=data,
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "UpdatedCity")

        # Clean up
        storage.delete(city)
        storage.save()

    def test_update_city_invalid_json(self):
        """Test PUT /api/v1/cities/<city_id> with invalid JSON"""
        city = City(name="CityWithBadData", state_id=self.state.id)
        storage.new(city)
        storage.save()

        headers = {"Content-Type": "application/json"}
        data = "Invalid JSON"

        response = self.client.put(
            f"/api/v1/cities/{city.id}",
            data=data,
            headers=headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not a JSON", response.get_json().get("error"))

        # Clean up
        storage.delete(city)
        storage.save()


if __name__ == '__main__':
    unittest.main()

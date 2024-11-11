#!/usr/bin/python3
"""
Contains the TestStateDocs, TestState classes, and API tests.
"""

import unittest
import inspect
from datetime import datetime
import json
import pycodestyle as pep8
from api.v1.app import app
import models
from models import storage
from models import state
from models.state import State
from models.base_model import BaseModel


class TestStateDocs(unittest.TestCase):
    """Tests to check the documentation and style of State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_f = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_state(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_state_module_docstring(self):
        """Test for the state.py module docstring"""
        self.assertIsNot(state.__doc__, None,
                         "state.py needs a docstring")
        self.assertTrue(len(state.__doc__) >= 1,
                        "state.py needs a docstring")

    def test_state_class_docstring(self):
        """Test for the State class docstring"""
        self.assertIsNot(State.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_func_docstrings(self):
        """Test for the presence of docstrings in State methods"""
        for func in self.state_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestState(unittest.TestCase):
    """Test the State class and API endpoints related to State"""

    @classmethod
    def setUpClass(cls):
        """Set up Flask test client and other test resources"""
        app.testing = True
        cls.client = app.test_client()

    def setUp(self):
        """Set up context and reload storage before each test"""
        self.ctx = app.app_context()
        self.ctx.push()
        storage.reload()

        for state in storage.all(State).values():
            storage.delete(state)
        storage.save()

    def tearDown(self):
        """Remove the test context after each test"""
        storage.close()
        self.ctx.pop()

    def test_create_state_unsupported_media_type(self):
        """Test POST /api/v1/states with unsupported media type"""
        response = self.client.post(
            '/api/v1/states', data="Invalid JSON format"
            )
        self.assertEqual(response.status_code, 415, "Expected status code 415")

    def test_create_state_invalid_json(self):
        """Test POST /api/v1/states with invalid JSON data"""
        # Set Content-Type header but provide invalid JSON format
        headers = {"Content-Type": "application/json"}
        response = self.client.post(
            '/api/v1/states', data="Invalid JSON format", headers=headers
            )
        self.assertEqual(response.status_code, 400, (
            "Expected status code 400 for invalid JSON"))

    def test_create_state_missing_name(self):
        """Test POST /api/v1/states with missing 'name' field in JSON"""
        headers = {"Content-Type": "application/json"}
        response = self.client.post('/api/v1/states', json={}, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing name", response.get_json().get("description"))

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_name_attr(self):
        """Test that State has attribute name, empty string or None"""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        if models.storage_t == 'db':
            self.assertEqual(state.name, None)
        else:
            self.assertEqual(state.name, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attributes"""
        s = State()
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in s.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        s = State()
        new_d = s.to_dict()
        self.assertEqual(new_d["__class__"], "State")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], s.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], s.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output"""
        state = State()
        string = "[State] ({}) {}".format(state.id, state.__dict__)
        self.assertEqual(string, str(state))

    def test_get_state_by_id(self):
        """Test GET /state/<state_id> for a valid State"""
        state = State(name="TestState")
        storage.new(state)
        storage.save()

        response = self.client.get(f"/api/v1/states/{state.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "TestState")

        # Clean up
        storage.delete(state)
        storage.save()


if __name__ == '__main__':
    unittest.main()

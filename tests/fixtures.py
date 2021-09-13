import base64

import pytest

from app import app
from nest.data_struct import NestedDefaultDict


@pytest.fixture
def auth_headers():
  auth = base64.b64encode("admin:admin".encode()).decode()
  return {'Authorization': f'Basic {auth}'}


@pytest.fixture
def client():
    client = app.test_client()

    yield client


@pytest.fixture
def nested_dict():
  return NestedDefaultDict()


@pytest.fixture
def flat_data():
    return [
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "FBP",
    "amount": 10.9
  }
]


@pytest.fixture
def folded_data():
    return {
  "EUR": {
    "ES": {
      "Madrid": [
        {
          "amount": 8.9
        }
      ]
    },
    "FR": {
      "Lyon": [
        {
          "amount": 11.4
        }
      ],
      "Paris": [
        {
          "amount": 20
        }
      ]
    }
  },
  "FBP": {
    "UK": {
      "London": [
        {
          "amount": 10.9
        }
      ]
    }
  },
  "GBP": {
    "UK": {
      "London": [
        {
          "amount": 12.2
        }
      ]
    }
  },
  "USD": {
    "US": {
      "Boston": [
        {
          "amount": 100
        }
      ]
    }
  }
}


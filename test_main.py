import sys
import pytest
from unittest.mock import MagicMock, patch

# --- Patch google.cloud.bigquery globally before import ---
mock_bq_module = MagicMock()
sys.modules["google.cloud.bigquery"] = mock_bq_module

# Now safe to import your app
from main import app, client as app_client


@pytest.fixture
def client():
    """Provide Flask test client."""
    app.testing = True
    with app.test_client() as test_client:
        yield test_client


def test_main_endpoint(client):
    """Test / endpoint without real GCP dependencies."""
    mock_load_job = MagicMock()
    mock_load_job.result.return_value = None
    app_client.load_table_from_uri.return_value = mock_load_job

    mock_table = MagicMock()
    mock_table.num_rows = 50
    app_client.get_table.return_value = mock_table

    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"data": 50}

    app_client.load_table_from_uri.assert_called_once()
    mock_load_job.result.assert_called_once()
    app_client.get_table.assert_called_once()

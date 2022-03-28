import pytest
from prefect.utilities.storage import extract_flow_from_file


@pytest.mark.vcr()
def test_flow():
    """Test scrape tasks."""
    flow = extract_flow_from_file("flow.py")
    flow.validate()

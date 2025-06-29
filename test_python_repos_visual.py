import pytest

from python_repos_visual import get_github_data


@pytest.fixture
def api_response():
    """The API response data that will be used in other tests."""
    return get_github_data("python")


def test_response_200(api_response: tuple[int, dict]):
    """Check if the API call returns a status code of 200."""
    response_code, _ = api_response
    assert response_code == 200


def test_complete_results(api_response: tuple[int, dict]):
    """Check if the API call returns complete results."""
    _, response_dict = api_response
    assert not response_dict["incomplete_results"]


def test_more_than_10_repos_found(api_response: tuple[int, dict]):
    """Check that the API call has returned more than 10 items."""
    _, response_dict = api_response
    assert len(response_dict["items"]) > 10

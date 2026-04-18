import pytest
from hypothesis import settings, HealthCheck

# Global hypothesis settings for property-based testing (enterprise reliability)
settings.register_profile(
    "ci",
    max_examples=50,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow]
)
settings.load_profile("ci")


@pytest.fixture(scope="session")
def sample_llm_response():
    """Realistic LLM response fixture for testing"""
    return {
        "content": "This is a test response from the AI model.",
        "model": "gpt-4o",
        "usage": {"prompt_tokens": 120, "completion_tokens": 45, "total_tokens": 165},
        "finish_reason": "stop"
    }


@pytest.fixture
def mock_openai_response():
    """Mock for OpenAI-style API responses"""
    class MockResponse:
        def __init__(self):
            self.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Mocked AI output'})})()]
            self.usage = type('obj', (object,), {'prompt_tokens': 100, 'completion_tokens': 30})()
    return MockResponse()

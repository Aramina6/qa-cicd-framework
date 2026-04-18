import pytest
import asyncio
from src.ai_orchestration.retry import RetryConfig, async_retry

@pytest.mark.asyncio
async def test_retry_decorator_success_on_first_try():
    call_count = 0

    @async_retry(RetryConfig(max_retries=2))
    async def flaky_func():
        nonlocal call_count
        call_count += 1
        return "success"

    result = await flaky_func()
    assert result == "success"
    assert call_count == 1   # no retry needed

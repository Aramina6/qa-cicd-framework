"""
tests/unit/ai_orchestration/test_retry_logic.py

Comprehensive tests for the async_retry decorator.
LLM calls are flaky (rate limits, network timeouts, model errors).
This decorator implements exponential backoff + max retries — the most important
resilience mechanism in any production AI orchestration layer.
"""

import pytest
import asyncio
from src.ai_orchestration.retry import RetryConfig, async_retry


@pytest.mark.asyncio
async def test_retry_decorator_success_on_first_attempt():
    """Most common case: call succeeds immediately → no retry should happen."""
    call_count = 0

    @async_retry(RetryConfig(max_retries=3, base_delay=0.01))
    async def successful_func():
        nonlocal call_count
        call_count += 1
        return "success"

    result = await successful_func()
    assert result == "success"
    assert call_count == 1  # no retries


@pytest.mark.asyncio
async def test_retry_decorator_retries_on_failure_and_succeeds():
    """Fails twice, succeeds on third attempt."""
    call_count = 0

    @async_retry(RetryConfig(max_retries=3, base_delay=0.01))
    async def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise RuntimeError("Simulated LLM failure")
        return "success after retries"

    result = await flaky_func()
    assert result == "success after retries"
    assert call_count == 3


@pytest.mark.asyncio
async def test_retry_decorator_fails_after_max_retries():
    """Fails every time → should raise the last exception after max retries."""
    call_count = 0

    @async_retry(RetryConfig(max_retries=2, base_delay=0.01))
    async def always_failing():
        nonlocal call_count
        call_count += 1
        raise RuntimeError(f"Failure #{call_count}")

    with pytest.raises(RuntimeError, match="Failure #3"):
        await always_failing()

    assert call_count == 3  # max_retries + 1


@pytest.mark.asyncio
async def test_retry_config_default_values():
    """Verify sensible defaults when no config is passed."""
    config = RetryConfig()
    assert config.max_retries == 3
    assert config.base_delay == 1.0
    assert config.max_delay == 30.0

from backend.main import run_agent


def test_run_agent_returns_tuple():
    ans, conf = run_agent("测试")
    assert isinstance(ans, str)
    assert isinstance(conf, float)
    assert 0.0 <= conf <= 1.0

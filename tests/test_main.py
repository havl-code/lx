from lx.main import get_user_task


def test_get_user_task_returns_valid_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "list files")
    result = get_user_task()
    assert result == "list files"


def test_get_user_task_rejects_empty_then_accepts(monkeypatch):
    responses = iter(["", "   ", "show disk usage"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    result = get_user_task()
    assert result == "show disk usage"
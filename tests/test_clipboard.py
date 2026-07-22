from lx.clipboard import prompt_copy_to_clipboard


def test_copies_when_user_confirms(monkeypatch, capsys):
    copied = {}

    def fake_copy(text):
        copied["value"] = text

    monkeypatch.setattr("lx.clipboard.pyperclip.copy", fake_copy)
    monkeypatch.setattr("builtins.input", lambda _: "y")

    prompt_copy_to_clipboard("ls -la")

    assert copied["value"] == "ls -la"
    output = capsys.readouterr().out
    assert "Copied." in output


def test_does_not_copy_when_user_declines(monkeypatch):
    called = {"copy_was_called": False}

    def fake_copy(text):
        called["copy_was_called"] = True

    monkeypatch.setattr("lx.clipboard.pyperclip.copy", fake_copy)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    prompt_copy_to_clipboard("ls -la")

    assert called["copy_was_called"] is False
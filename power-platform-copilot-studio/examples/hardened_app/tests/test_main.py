import importlib
import os
import sys
import types

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

ENV_KEYS = ["FOUNDRY_PROJECT_ENDPOINT", "FOUNDRY_AGENT_NAME", "REQUIRE_LOGIN", "ALLOWED_USERS",
            "CRED_MODE", "TENANT_ID", "CLIENT_ID", "CLIENT_SECRET", "FRAME_ANCESTORS"]


def load(**env):
    for k in ENV_KEYS:
        os.environ.pop(k, None)
    base = {"FOUNDRY_PROJECT_ENDPOINT": "https://x.services.ai.azure.com/api/projects/p",
            "FOUNDRY_AGENT_NAME": "agent", "REQUIRE_LOGIN": "true"}
    base.update(env)
    for k, v in base.items():
        os.environ[k] = v
    sys.modules.pop("app.main", None)
    return importlib.import_module("app.main")


class FakeClient:
    def __init__(self, text="Hello **world**", fail=None):
        self.text, self.fail, self.created = text, fail, 0
        outer = self

        class Conversations:
            def create(self):
                outer.created += 1
                return types.SimpleNamespace(id="conv_%d" % outer.created)

        class Responses:
            def create(self, conversation, input):
                if outer.fail:
                    raise outer.fail
                items = [types.SimpleNamespace(type="fabric_dataagent_preview_call"),
                         types.SimpleNamespace(type="message")]
                return types.SimpleNamespace(output_text=outer.text, output=items)

        self.conversations, self.responses = Conversations(), Responses()


H = {"x-ms-client-principal-id": "u1", "x-ms-client-principal-name": "a@x.com", "x-requested-with": "fetch"}


@pytest.fixture
def mod():
    m = load()
    m._client = FakeClient()
    return m


def post(c, msg="hi", headers=None):
    return c.post("/api/chat", json={"message": msg}, headers=H if headers is None else headers)


def test_requires_login(mod):
    assert post(TestClient(mod.app), headers={"x-requested-with": "fetch"}).status_code == 401


def test_csrf_header_required(mod):
    assert post(TestClient(mod.app), headers={"x-ms-client-principal-id": "u1"}).status_code == 403


def test_ok_and_markdown_rendered(mod):
    r = post(TestClient(mod.app))
    assert r.status_code == 200
    j = r.json()
    assert "<strong>world</strong>" in j["html"]
    assert "tools" not in j  # SHOW_TOOLS is off by default


def test_citation_markers_stripped(mod):
    mod._client = FakeClient(text="Answer 【4:0†source】 done")
    j = post(TestClient(mod.app)).json()
    assert "【" not in j["answer"] and "source" not in j["answer"]


def test_script_images_and_js_links_removed(mod):
    mod._client = FakeClient(
        text="<script>alert(1)</script> ![x](https://evil.example/p.png?d=secret) [l](javascript:alert(1))")
    j = post(TestClient(mod.app)).json()
    assert "<script" not in j["html"] and "<img" not in j["html"] and "javascript:" not in j["html"]


def test_message_too_long_and_empty(mod):
    c = TestClient(mod.app)
    assert post(c, "x" * (mod.MAX_CHARS + 1)).status_code == 400
    assert post(c, "   ").status_code == 400


def test_rate_limit(mod):
    c = TestClient(mod.app)
    codes = [post(c).status_code for _ in range(mod.RATE_PER_MINUTE + 1)]
    assert codes[:-1] == [200] * mod.RATE_PER_MINUTE and codes[-1] == 429


def test_conversation_per_user_and_reuse(mod):
    c = TestClient(mod.app)
    post(c)
    post(c)
    post(c, headers=dict(H, **{"x-ms-client-principal-id": "u2"}))
    assert mod._client.created == 2  # u1 reused its conversation, u2 got its own
    c.post("/api/reset", headers=H)
    post(c)
    assert mod._client.created == 3


def test_allow_list():
    m = load(ALLOWED_USERS="boss@x.com")
    m._client = FakeClient()
    c = TestClient(m.app)
    assert post(c).status_code == 403
    assert post(c, headers=dict(H, **{"x-ms-client-principal-name": "boss@x.com"})).status_code == 200


def test_errors_are_generic(mod):
    err = RuntimeError("secret internal detail")
    err.status_code = 403
    mod._client = FakeClient(fail=err)
    r = post(TestClient(mod.app))
    assert r.status_code == 502
    assert "secret" not in r.text and "permission" in r.json()["error"]


def test_security_headers_and_no_docs(mod):
    c = TestClient(mod.app)
    r = c.get("/")
    assert "frame-ancestors 'none'" in r.headers["content-security-policy"]
    assert r.headers["x-content-type-options"] == "nosniff"
    assert c.get("/docs").status_code == 404 and c.get("/openapi.json").status_code == 404


def test_frame_ancestors_configurable():
    m = load(FRAME_ANCESTORS="https://*.sharepoint.com")
    r = TestClient(m.app).get("/")
    assert "frame-ancestors https://*.sharepoint.com" in r.headers["content-security-policy"]
    assert "x-frame-options" not in r.headers


def test_health_and_ready(mod):
    c = TestClient(mod.app)
    assert c.get("/healthz").status_code == 200
    assert c.get("/readyz").status_code == 200
    m = load(FOUNDRY_PROJECT_ENDPOINT="")
    assert TestClient(m.app).get("/readyz").status_code == 503


def test_obo_requires_token():
    m = load(CRED_MODE="obo", TENANT_ID="t", CLIENT_ID="c", CLIENT_SECRET="s")
    assert post(TestClient(m.app)).status_code == 401

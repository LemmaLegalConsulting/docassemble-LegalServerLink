"""The preloaded endpoint must import on both supported Flask layouts."""

import importlib.util
import sys
import types
from pathlib import Path

import pytest
from flask import Flask


@pytest.mark.parametrize("modern", [False, True])
@pytest.mark.parametrize("authorized", [False, True])
def test_ls_interviews_uses_existing_app_and_authorization(
    monkeypatch, modern, authorized
):
    app = Flask("legalserver-import-compatibility")
    csrf = types.SimpleNamespace(exempt=lambda function: function)
    config = {"interviews": [{"name": "Synthetic interview"}]}
    modules = {}
    for name in ["docassemble", "docassemble.base", "docassemble.webapp"]:
        module = types.ModuleType(name)
        module.__path__ = []
        modules[name] = module
    util = types.ModuleType("docassemble.base.util")
    util.get_config = lambda name: config
    modules[util.__name__] = util
    objects = types.ModuleType("docassemble.webapp.app_object")
    modules[objects.__name__] = objects
    api_verify = lambda **kwargs: authorized
    jsonify_with_status = lambda data, status: (data, status)
    if modern:
        objects.flaskapp = app
        extension = types.ModuleType("docassemble.webapp.extensions")
        extension.csrf = csrf
        modules[extension.__name__] = extension
        for package in ["docassemble.webapp.api", "docassemble.webapp.utils"]:
            module = types.ModuleType(package)
            module.__path__ = []
            modules[package] = module
        api = types.ModuleType("docassemble.webapp.api.helpers")
        api.api_verify = api_verify
        response = types.ModuleType("docassemble.webapp.utils.helpers")
        response.jsonify_with_status = jsonify_with_status
        modules[api.__name__] = api
        modules[response.__name__] = response
    else:
        objects.app, objects.csrf = app, csrf
        server = types.ModuleType("docassemble.webapp.server")
        server.api_verify = api_verify
        server.jsonify_with_status = jsonify_with_status
        modules[server.__name__] = server
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)
    source = (
        Path(__file__).resolve().parents[1]
        / "docassemble/LegalServerLink/LSinterviews.py"
    )
    spec = importlib.util.spec_from_file_location("lsinterviews_under_test", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.app is app
    assert module.csrf is csrf
    response = app.test_client().get("/lsinterviews")
    if authorized:
        assert response.status_code == 200
        assert response.get_json() == {
            "interviews": [
                {"name": "Synthetic interview", "external": False, "sites": []}
            ]
        }
    else:
        assert response.status_code == 403
        assert response.get_json() == {"url": "Access denied."}

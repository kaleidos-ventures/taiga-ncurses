import os
import tempfile

### TODO
#
#from taiga_ncurses.config import DEFAULTS, Configuration
#
#
#SAMPLE_HOST = {
#    "scheme": "http",
#    "domain": "localhost",
#    "port": 8000
#}
#
#SAMPLE_CONFIG = """
#[host]
#scheme = {scheme}
#domain = {domain}
#port = {port}
#
#[site]
#domain = {domain}
#""".format(**SAMPLE_HOST)
#
#
#SAMPLE_AUTH = {
#    "token": "42",
#}
#
#SAMPLE_AUTH_CONFIG = """
#[auth]
#token = {token}
#""".format(**SAMPLE_AUTH)
#
#def test_configuration_builds_a_url_for_the_host():
#    _ = tempfile.NamedTemporaryFile()
#    config = Configuration(config_file=_)
#    _.close()
#    assert config.host == "{scheme}://{domain}:{port}".format(scheme=DEFAULTS["main"]["host"]["scheme"],
#                                                              domain=DEFAULTS["main"]["host"]["domain"],
#                                                              port=DEFAULTS["main"]["host"]["port"])
#
#def test_configuration_load_host_from_file():
#    _ = tempfile.NamedTemporaryFile()
#    config_file = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False)
#    config_file.file.write(SAMPLE_CONFIG)
#    config_file.close()
#    config = Configuration(config_file=config_file.name)
#    config.load()
#    os.remove(config_file.name)
#    _.close()
#    assert config.host == "{scheme}://{domain}:{port}".format(scheme=SAMPLE_HOST["scheme"],
#                                                              domain=SAMPLE_HOST["domain"],
#                                                              port=SAMPLE_HOST["port"])
#
#def test_configuration_load_site_from_file():
#    _ = tempfile.NamedTemporaryFile()
#    config_file = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False)
#    config_file.file.write(SAMPLE_CONFIG)
#    config_file.close()
#    config = Configuration(config_file=config_file.name)
#    config.load()
#    os.remove(config_file.name)
#    _.close()
#    assert config.site == str(SAMPLE_HOST["domain"])
#
#def test_configuration_auth_property_is_none_when_no_token_is_loaded():
#    _ = tempfile.NamedTemporaryFile()
#    config = Configuration(config_file=_)
#    _.close()
#    assert config.auth_token is None
#
#def test_configuration_save_to_file():
#    config_file = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False)
#    config_file.file.write(SAMPLE_CONFIG)
#    config_file.close()
#    config = Configuration(config_file=config_file.name)
#    config.load()
#    config.save()
#    parser = ConfigParser()
#    parser.read(config_file.name, encoding="utf-8")
#    os.remove(config_file.name)
#    assert "host" in parser._sections
#    assert "site" in parser._sections
#    assert "auth" not in parser._sections
#    for k, v in SAMPLE_HOST.items():
#        assert str(v) == parser._sections["host"][k]
#    assert str(SAMPLE_HOST["domain"]) == parser._sections["site"]["domain"]
#
#def test_auth_configuration_save_to_file():
#    auth_config_file = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False)
#    auth_config_file.file.write(SAMPLE_AUTH_CONFIG)
#    auth_config_file.close()
#    config = Configuration(config_file=auth_config_file.name)
#    config.load()
#    config.save()
#    parser = ConfigParser()
#    parser.read(auth_config_file.name, encoding="utf-8")
#    os.remove(auth_config_file.name)
#    assert "auth" in parser._sections
#    assert "host" not in parser._sections
#    assert "site" not in parser._sections
#    assert "keys" not in parser._sections
#    assert "colors" not in parser._sections
#    assert SAMPLE_AUTH["token"] == parser._sections["auth"]["token"]

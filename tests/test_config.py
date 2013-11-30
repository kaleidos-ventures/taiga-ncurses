from gmncurses.config import DEFAULTS, Configuration

def test_configuration_builds_a_url_for_the_host():
    config = Configuration(DEFAULTS)
    assert config.host == "{scheme}://{domain}:{port}".format(scheme=DEFAULTS["host"]["scheme"],
                                                              domain=DEFAULTS["host"]["domain"],
                                                              port=DEFAULTS["host"]["port"])

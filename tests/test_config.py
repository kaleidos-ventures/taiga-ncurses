from gmncurses.config import DEFAULTS, Configuration

def test_configuration_builds_a_url_for_the_host():
    config = Configuration(DEFAULTS)
    assert config.host == "{protocol}://{url}".format(protocol=DEFAULTS['host']['protocol'],
                                                      url=DEFAULTS['host']['url'])

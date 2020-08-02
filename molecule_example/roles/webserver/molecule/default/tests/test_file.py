import os

import testinfra.utils.ansible_runner

testinfra = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_apache_pkg(host):
    assert  host.package("apache2").is_installed

def test_apache_running_and_enabled(host):
    apache = host.service("apache2")
    assert apache.is_running
    assert apache.is_enabled

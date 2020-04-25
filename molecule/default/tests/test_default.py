import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_default_packages(host):
    p = host.package('rsyslog')
    assert p.is_installed


def test_default_config(host):
    f = host.file('/etc/rsyslog.conf')
    modules = """module(
  load="imuxsock"
)
module(
  load="imklog"
)
module(
  load="builtin:omfile"
  Template="RSYSLOG_TraditionalFileFormat"
  DirCreateMOde="0755"
  FileCreateMode="0640"
  fileOwner="root"
  fileGroup="adm"
)
"""

    global_configs = """global(
  workDirectory="/var/spool/rsyslog"
  umask="0022"
)"""

    include_configs = """include(
  file="/etc/rsyslog.d/*"
  mode="optional"
)"""

    filters = """auth,authpriv.* /var/log/auth.log
*.*;auth,authpriv.none -/var/log/syslog
daemon.* -/var/log/daemon.log
kern.* -/var/log/kern.log
lpr.* -/var/log/lpr.log
mail.* -/var/log/mail.log
user.* -/var/log/user.log
mail.info -/var/log/mail.info
mail.warn -/var/log/mail.warn
mail.err /var/log/mail.err
*.=debug,auth,authpriv.none,news.none;mail.none -/var/log/debug
*.=info;*.=notice;*.=warn,auth,authpriv.none,cron,daemon.none,mail,news.none -/var/log/messages
"""

    assert f.contains(modules)
    assert f.contains(global_configs)
    assert f.contains(include_configs)
    assert f.contains(filters)

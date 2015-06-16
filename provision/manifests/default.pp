
# ----------------------------------------------------------------------------
# Install packages:
# ----------------------------------------------------------------------------

package { 
    [
      "libpq-dev",
      "python-pip", 
      "python-dev", 
      "python-psycopg2",
      "build-essential", 
      "postgresql",
      "postgresql-contrib",
      "nginx",
      "uwsgi",
      "uwsgi-plugin-python",
    ]:
    ensure => present,
}

# ----------------------------------------------------------------------------
# Execute commands:
# ----------------------------------------------------------------------------

# install the required python packages from the requirements file
exec { "dev-requirements":
    command => "/usr/bin/env pip install -r /vagrant/requirements/local_dev.txt",
    require => Package["python-pip"],
}

# XXX other stuff...


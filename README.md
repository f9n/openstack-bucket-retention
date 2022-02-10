# openstack-bucket-retention [![PyPi version](https://img.shields.io/pypi/v/openstack-bucket-retention.svg)](https://pypi.python.org/pypi/openstack-bucket-retention/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/openstack-bucket-retention.svg)](https://pypi.python.org/pypi/openstack-bucket-retention/) [![](https://img.shields.io/github/license/f9n/openstack-bucket-retention.svg)](https://github.com/f9n/openstack-bucket-retention/blob/main/LICENSE)

Openstack bucket retention cli


## Installation

```
$ # Install
$ python3 -m pip install openstack-bucket-retention --user

$ # Install with upgrade
$ python3 -m pip install openstack-bucket-retention --user --upgrade
```

## Usage

First you need to download 'OpenStack RC File' on openstack provider. And Source the sh file.

```bash
$ openstack-bucket-retention --help

$ # Show version
$ openstack-bucket-retention version
openstack-bucket-retention: 0.1.0

$ # Set Openstack environment variables
$ #  or
$ # Use 'OpenStack RC File' on openstack provider. Download and Source the file.
$ source Openstack-openrc.sh
$ openstack-bucket-retention run --bucket-name "test-bucket" --retention-time "1w"

```

# rio-cli
[![PyPI version](https://badge.fury.io/py/rio-chopt.svg)](https://badge.fury.io/py/rio-chopt)
[![pypi supported versions](https://img.shields.io/pypi/pyversions/rio-chopt.svg)](https://pypi.python.org/pypi/rio-chopt)

This utility helps you deploy your code as an API locally on your machine using [Docker](#https://www.docker.com/products/docker-desktop). It is a python based package that can be installed via pip.


## Quickstart

1. Install rio: `pip install rio-chopt`

2. Deploy your package : `rio deploy -l path/to/package/folder`

    eg: `rio deploy -l /Users/abcdef@ghi.com/Documents/git/myProject`

    Note: you will be prompted to enter your **docker hub username, password, and email**
    
You can find a sample project [here.](https://github.com/chainopt/rio-cli/tree/main/samples/myProject)

----

#### - Deploy Package Arguments and Options

`rio deploy -l path/to/package/folder`


* `-l` is for local deployment(only local is available for now) 
* `-n` is for specifying a package name. If left out, the folder name is chosen as package name. 
* `-p` is a port you specify for it to be spun up on(The valid range is 1024-65535). If left out, a port will be assigned. 

#### - Re-deploying a package.
`rio deploy -l path/to/package/folder`

#### If you used a custom name for your package, you will have to specify it with the package name (-n) flag just like you did initially.



e.g. `rio deploy -l /Users/abcdef@ghi.com/Documents/git/myUpdatedProject`
or

`rio deploy -l -n myCustomName /Users/abcdef@ghi.com/Documents/git/myUpdatedProject`

>Note: It will re-use the port from the first deployment.
---
### Other commands:

| Description           | Command                    |
| --------------------- |----------------------------|
| List packages deployed| `rio list -l`              |
| Stop a package ¹      | `rio stop -l myProject`    |
| Stop all packages     | `rio stop -l --all`        |
| Start a package       | `rio start -l myProject`   |
| Start all packages    | `rio start -l --all`       |
| Undeploy a package    | `rio undeploy -l myProject`|
| Undeploy all packages | `rio undeploy -l --all`    |
| Begin RIO session ² ³ | `rio begin -l`             |
| End RIO session       | `rio end -l`               |



¹ If a model API associated with this package is running, you will be asked to enter 'Y' to stop it and proceed with deleting the package.



² A RIO Session begins automatically upon running `rio deploy` or `rio list`.

³ You can also point to a yaml file like this:
`rio begin -l -f /Users/myUser/Documents/docker-creds.yaml`. Download a sample credential file [here.](https://github.com/chainopt/rio-cli/tree/main/samples/credentials.yaml)

##### You can use the `--help` command in front of any command from within the CLI for help with options and arguments. 
##### Eg: `rio deploy --help`
----
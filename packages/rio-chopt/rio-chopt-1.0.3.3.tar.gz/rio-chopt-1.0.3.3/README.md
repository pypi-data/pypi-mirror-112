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

### Other commands:


#### - Deploy Package Arguments and Options

`rio deploy -l path/to/package/folder`

Here,
* -l (**required**) is for local deployment(only local is available for now) 
* -n (**not required**) is for specifying a package name. If left out, the folder name is chosen as package name. 
* -p (**not required**) is a port you specify for it to be spun up on(The valid range is 1024-65535). If left out, a port will be assigned. 

#### - Re-deploying a package.
`rio deploy -l path/to/package/folder`

>Note: If you used a custom name for your package, you will have to specify it with the package name (-n) flag just like you did in rio deploy.

---example---

e.g. `rio deploy -l /Users/abcdef@ghi.com/Documents/git/myUpdatedProject`
or

`rio deploy -l -n myCustomName /Users/abcdef@ghi.com/Documents/git/myUpdatedProject`

>Note: It will re-use the same port from the first deployment.

#### - List Packages Uploaded and APIs Running

`rio list -l`


#### - Stop a running package.
`rio stop -l myProject`
or 
`rio stop -l --all`(to stop all running packages.)


#### - Start a stopped package.
`rio start -l myProject` or `rio start -l --all`(to start all stopped packages.)

#### - Undeploy a package.
`rio undeploy -l myProject` or `rio undeploy -l --all`(to undeploy all packages.)

>Note: If a model API associated with this package is running, you will be asked to enter 'Y' to stop it and proceed with deleting the package.


#### - Begin RIO 
`rio begin -l`

This is also triggered automatically upon running `rio deploy` or `rio list` to ensure RIO is up.

You can also point to a yaml file like this:

`rio begin -l -f /Users/myUser/Documents/docker-creds.yaml`

Download a sample credential file [here.](https://github.com/chainopt/rio-cli/tree/main/samples/credentials.yaml)

>Note: Running `rio begin -l` at any time will restart the API, but packages/model APIs will not be affected. 

#### - End RIO
`rio end -l`
to close out the RIO Session. `rio begin -l`,`rio deploy -l` or `rio list -l` will be required to restart.
# rio-cli
[![PyPI version](https://badge.fury.io/py/rio-chopt.svg)](https://badge.fury.io/py/rio-chopt)
[![pypi supported versions](https://img.shields.io/pypi/pyversions/rio-chopt.svg)](https://pypi.python.org/pypi/rio-chopt)

This utility helps you deploy your code as an API locally on your machine.  It is a python based package that can be installed via pip.

## Pre-requisites
1. Install Docker for desktop on your machine and make sure it is running. - [Download here!](https://www.docker.com/products/docker-desktop)
2. Install git - [Download here!](https://git-scm.com/downloads)
3. Install python - [Download here!](https://www.python.org/downloads/)
4. Request **github** and **docker hub** credentials by sending an email titled "Requesting access to RIO github and dockerhub" to contact@chainopt.com with your Full Name and relevant context(client/student/DS Masterclass Practitioner etc.) 

## Installation From [PyPI](https://pypi.python.org/pypi/rio-chopt/) directly:

1. Start Docker

2. Install rio
```
pip install rio-chopt
```
You may now go directly to [Begin](#Begin)

## Alternatively you may choose to install from source:

1. Start Docker
2. Download the repository using the command below. You will be prompted to enter the **github username and email**.
```bash
git clone https://github.com/chainopt/rio-cli.git
```
3. Navigate to the repository folder from the command line
```bash
cd rio-cli
```

4. Install the rio-cli

```bash
pip install .
```


## <a name="Begin"></a>Begin RIO
1. Initialize RIO. Now you will be prompted to enter the **docker hub username, password, and email** provided to you by ChainOpt.
```bash
rio begin -l
Enter your Docker Username: ***********  
Enter your Docker Password: ***********
Enter your Docker email: ***********
```
You can also point to a yaml file like this:
```bash
rio begin -l -f /Users/myUser/Documents/docker-creds.yaml
```
Download a sample credential file [here.](https://github.com/chainopt/rio-cli/tree/main/samples/credentials.yaml)

>Note: Running `rio begin -l` at any time will restart the API, but packages/model APIs will not be affected. 


**You're now ready to deploy your first package!**


## Deploy a package
You can find a sample project [here.](https://github.com/chainopt/rio-cli/tree/main/samples/myProject)

```
rio deploy -l path/to/package/folder

---example---
rio deploy -l /Users/abcdef@ghi.com/Documents/git/myProject
```
Here,
* -l (**required**) is for local deployment(only local is available for now) 
* -n (**not required**) is for specifying a package name. If left out, the folder name is chosen as package name. 
* -p (**not required**) is a port you specify for it to be spun up on(The valid range is 1024-65535). If left out, a port will be assigned. 

### To list Packages Uploaded and APIs Running
```
rio list -l
```

### To re-deploy a package.
```
rio deploy -l path/to/package/folder

>Note: If you used a custom name for your package, you will have to specify it with the package name (-n) flag just like you did in rio deploy.

---example---
e.g. rio deploy -l /Users/abcdef@ghi.com/Documents/git/myUpdatedProject
or
rio deploy -l -n myCustomName /Users/abcdef@ghi.com/Documents/git/myUpdatedProject
```
>Note: It will re-use the same port from the first deployment.

### To stop a running package.
```
rio stop -l myProject
```
### To stop all running packages.
```
rio stop -l --all
```

### To start a stopped package.
```
rio start -l myProject
```
### To start all stopped packages.
```
rio start -l --all
```

### To undeploy a package.
```
rio undeploy -l myProject
```
>Note: If a model API associated with this package is running, you will be asked to enter 'Y' to stop it and proceed with deleting the package.

### To undeploy all packages.
```
rio undeploy -l --all
```


### To end RIO
```
rio end -l
```
>All background processes will be closed. `rio begin -l` will be required to restart.

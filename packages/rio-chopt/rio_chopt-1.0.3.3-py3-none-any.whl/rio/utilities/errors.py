class BadCredError(SystemExit):
    """
    Handles passing through bad credentials to Docker
    """

    def __init__(self, message="All credentials given failed to authenticate."):
        super().__init__(message)


class DockerNotRunningError(SystemExit):
    """
    Handles trying to run RIO locally without Docker running
    """

    def __init__(self, message="Docker cannot be found running anywhere on this machine."):
        super().__init__(message)


class DockerHubAccountError(SystemExit):
    """
    Handles when the user is not logged in with the correct Docker Hub account.
    """

    def __init__(self, message="The Docker Hub account used does not have permission to the rio-api image. "
                               "Please try another accouunt or try again."):
        super().__init__(message)


class NoLocalFlagError(SystemExit):
    """
    Handles when local flag is not set

    ***SET TO BE DEPRECATED UPON RELEASING CLOUD SUPPORT THROUGH CLI***
    """

    def __init__(self, message="Please email contact@chainopt.com for remote deployment services."):
        super().__init__(message)


class LoggingError(SystemExit):
    """
    Handles when creation of logs has failed.
    """

    def __init__(self, message="Logs could not be generated. Please check your code and retry or contact support."):
        super().__init__(message)


class PackageDeletionError(SystemExit):
    """
    Handles when deleting a package has failed.
    """

    def __init__(self, message="Unable to delete package."):
        super().__init__(message)


class DuplicatePackageError(SystemExit):
    """
    Handles when a user attempts to deploy a package with a duplicate name
    and chooses not to overwrite the package with the new deployment.
    """

    def __init__(self, message="A deployed package already exists with that name. "
                               "Please attempt again with a new package name."):
        super().__init__(message)


class BadPortError(SystemExit):
    """
    Handles when a user inputs a port that cannot be used.
    """

    def __init__(self, message="Please try again and enter a port number between 1024 and 65535. You also may not "
                               "specify a port and it will be assigned automatically."):
        super().__init__(message)


class UploadAPIError(SystemExit):
    """
    Handles when the RIO upload API is non-responsive.
    """

    def __init__(self, message="Upload API unavailable!"):
        super().__init__(message)


class DeployAPIError(SystemExit):
    """
    Handles when the RIO deploy API is non-responsive.
    """

    def __init__(self, message="Deploy API unavailable!"):
        super().__init__(message)


class APIError(SystemExit):
    # TODO: Combine Upload and Deploy API errors into this singular error
    """
    Handles issues with the RIO-API backend.
    """

    def __init__(self, module="", message="API unavailable!"):
        if module:
            super().__init__(module + " " + message)
        else:
            super().__init__(message)


class PackagePathError(SystemExit):
    """
    Handles bad OS paths being input for deployments.
    """

    def __init__(self, message="Unable to find package in location given. Please check the path and try again."):
        super().__init__(message)


class PackageExistenceError(SystemExit):
    """
    Handles when a package name is given that does not exist in Docker/RIO-API
    """

    def __init__(self, package_name, message=" not found. Please check the package name and retry."):
        super().__init__(package_name + message)


class NoRunningPackagesError(SystemExit):
    """
    Handles when a request has been made but no packages are running.
    """

    def __init__(self, message="No running packages."):
        super().__init__(message)


class MissingPackageInputError(SystemExit):
    """
    Handles when a function that requires a package or --all gets neither input
    """

    def __init__(self, message="Please specify a package name or --all."):
        super().__init__(message)


class PackagingError(SystemExit):
    """
    Handles when creating a zipped version of the package fails
    """

    def __init__(self, message="Failed to create .zip version of package. Please check package name."):
        super().__init__(message)


class PackageStopError(SystemExit):
    """
    Handles when the API fails to stop a package
    """

    def __init__(self, package_name):
        message = f"Unable to stop {package_name} package. Please retry or report this as a bug."
        super().__init__()

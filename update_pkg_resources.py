"""A script that reads a list of requirements files, extracts the package names
and their versions, and generates new requirements files with pinned package
versions."""

import pkg_resources


def get_pkg_version(pkg: str) -> str:
    """Return a string with the package name and its pinned version.

    Args:
        pkg: The name of the package to get the version for.

    Returns:
        A string with the package name and pinned version in the format "pkg==version".

    Raises:
        DistributionNotFound: If the package is not installed.
    """
    return f"{pkg}=={pkg_resources.get_distribution(pkg).version}\n"


def get_requirement_list(filename: str):
    """Read a requirements file and return a list of requirements with pinned versions.

    Args:
        filename: The name of the requirements file to read.

    Returns:
        A list of requirements with pinned versions.
    """
    req_list = []
    with open(filename) as req_file:
        for line in req_file:
            try:
                pkg = line.split("==")[0].strip()
                req_list.append(get_pkg_version(pkg))
            except Exception:
                req_list.append(line)
    return req_list


def update_requirement_file(filename: str, req_list: list):
    """Write a list of requirements to a file.

    Args:
        filename: The name of the file to write the requirements to.
        req_list: A list of requirements with pinned versions.
    """
    with open(filename, "w") as req_file:
        req_file.writelines(req_list)


def main():
    """Read each requirements file in the list, get a list of requirements with
    pinned versions, and write them to a new file."""
    requirement_files = [
        "requirements/base.txt",
        "requirements/local.txt",
        "requirements/production.txt",
    ]
    for requirement_file in requirement_files:
        req_list = get_requirement_list(requirement_file)
        update_requirement_file(requirement_file, req_list)


if __name__ == "__main__":
    main()

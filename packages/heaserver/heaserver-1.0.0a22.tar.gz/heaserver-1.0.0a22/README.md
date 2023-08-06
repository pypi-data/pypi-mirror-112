# HEA Server Framework
[Research Informatics Shared Resource](https://risr.hci.utah.edu), [Huntsman Cancer Institute](https://healthcare.utah.edu/huntsmancancerinstitute/), Salt Lake City, UT

The HEA Server Framework contains shared code for creating HEA microservices.

## Version 1
Initial release.

## Runtime requirements
* Python 3.8

## Development environment

### Build requirements
* Any development environment is fine.
* On Windows, you also will need:
    * Build Tools for Visual Studio 2019, found at https://visualstudio.microsoft.com/downloads/. Select the C++ tools.
    * git, found at https://git-scm.com/download/win.
* On Mac, Xcode or the command line developer tools is required, found in the Apple Store app.
* Python 3.8: Download and install Python 3.8 from https://www.python.org, and select the options to install for all users and add
Python to your environment variables. The install for all users option will help keep you from accidentally installing
packages into your Python installation's site-packages directory instead of to your virtualenv environment, described
below.
* Create a virtualenv environment using the `python -m venv <venv_directory>` command, substituting `<venv_directory>`
with the directory name of your virtual environment. Run `source <venv_directory>/bin/activate` (or `<venv_directory>/Scripts/activate` on Windows) to activate the virtual
environment. You will need to activate the virtualenv every time before starting work, or your IDE may be able to do 
this for you automatically. **Note that PyCharm will do this for you, but you have to create a new Terminal panel
after you newly configure a project with your virtualenv.**
* From the project's root directory, and using the activated virtualenv, run `pip install -r requirements_dev.txt`.
**Do NOT run `python setup.py develop`. It will break your environment.**

### Running tests
Run tests with the `pytest` command from the project root directory.

### Running integration tests
* Install Docker
* On Windows, install pywin32 version >= 223 from https://github.com/mhammond/pywin32/releases. In your venv, make sure that
`include-system-site-packages` is set to `true`.

### Versioning
Use semantic versioning as described in 
https://packaging.python.org/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme. In addition,
while development is underway, the version should be the next version number suffixed by -SNAPSHOT.

### Version tags in git
Version tags should follow the format `heaserver-<version>`, for example, `heaserver-1.0.0`.

### Uploading to an index server
You will need a custom index server such as devpi to upload HEA component releases so that HEA
components can depend on each other. You will need to configure pip to use the custom index server
instead of the usual Pypi.

The following instructions assume separate stable and staging indexes. Numbered releases, including alphas and betas, go 
into the stable index. Snapshots of works in progress go into the staging index. Artifacts uploaded to the
staging index can be overwritten. Artifacts uploaded to stable cannot. Thus, also use staging to upload numbered
releases, verify the uploaded packages, and then upload to stable.

From the project's root directory:
1. For numbered releases, remove `.dev` from the version number in setup.py, tag it in git to indicate a release, 
and commit to version control. Skip this step for developer snapshot releases.
2. Run `python setup.py clean --all sdist bdist_wheel` to create the artifacts.
3. Run `twine upload -r <repository> dist/heaserver-<version>.whl dist/heaserver-<version>.tar.gz` to upload to the
 repository. The repository name has to be defined in a twine configuration file such as `$HOME/.pypirc`.
4. For numbered releases, increment the version number in setup.py, append `.dev` to it, and commit to version 
control with a commit message like, "Prepare for next development iteration."

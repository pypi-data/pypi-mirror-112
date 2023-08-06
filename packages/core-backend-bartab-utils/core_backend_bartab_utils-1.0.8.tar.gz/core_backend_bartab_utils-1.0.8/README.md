# Core Backend Bartab Utils

_Updated Saturday May 8th 2021 by [cassio](https://github.com/cassio)_

Common python code for BarTab python repositories. Hosted in pip production [here](https://pypi.org/project/core-backend-bartab-utils/), test pip hosted [here](https://test.pypi.org/project/core-backend-bartab-utils/)


## First Time Developer Setup

_Must be done for each dev that works on the project. Please **do not** remove these instructions._

1. Set git remote head to development:

```bash
git remote set-head origin development
```

2. Create your bartab cosmopolitan database:

```bash
psql -U postgres -f settings.sql
```
## Automated Version Release

When a commit is pushed to the `main` branch [publish-pip-package.yml](https://github.com/BarTabPayments/core_backend_bartab_utils/blob/main/.github/workflows/publish-pip-package.yml) will deploy to the [pypi core backend bartab utils project](https://pypi.org/project/core-backend-bartab-utils/).

The project version is determined using the commit message.

* If the commit message contains the word `breaking` (case insensitive) a new version will be released. ie. `1.3.4` -> `2.0.0`

* If the commit message contains the word `major` (case insensitive) or `cut-major` (case insensitive) a new major version will be released ie. `1.3.4` -> `1.4.0`

* All other commit messages will result in a minor release. ie. `1.3.4` -> `1.3.5`

## Manual Version Release

Update the `version` parameter in `./setup.py`. The run:

```bash
python setup.py sdist
```

This will create a new version in `./dist`. To release run the following:

```bash
python twine upload dist/core_backend_bartab_utils-<YOUR_NEW_VERSION>.tar.gz
```

To upload to test pip run:

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/core_backend_bartab_utils-<YOUR_NEW_VERSION>.tar.gz
```

## External References

How to create a pip package is walked through [here](https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/).

## Features

1. **Issue Templates**
   1. _Bug Report_ - Create a bug report issue
   2. _Feature Request_ - Create feature request/enhancement
   3. _Dev Ops Request_ - Create a new development operations request, this can be sever management, user access item, workflow automation enhancement, or a report of issues going on with cloud infrastructure
   4. _Test Request_ - Create test automation or manual testing request
2. **Workflows**
   1. _[org-project-automation.yml](https://github.com/BarTabPayments/core_backend_bartab_utils/blob/main/.github/workflows/org-project-automation.yml)_ - Will link new issues and pull requests to: [Master Bartab Project](https://github.com/orgs/BarTabPayments/projects/3)
   2. _[main-project-automation.yml](https://github.com/BarTabPayments/core_backend_bartab_utils/blob/main/.github/workflows/main-project-automation.yml)_ - Will link new issues and pull requests to project within this repo
   3. _[publish-pip-package.yml](https://github.com/BarTabPayments/core_backend_bartab_utils/blob/main/.github/workflows/publish-pip-package.yml)_ - Will deploy to the [pypi core backend bartab utils project](https://pypi.org/project/core-backend-bartab-utils/). See above.
   4. _Auto Assign_ - Using [Auto Assign](https://github.com/apps/auto-assign) will assign the creator of a pull request to the author of the pull request

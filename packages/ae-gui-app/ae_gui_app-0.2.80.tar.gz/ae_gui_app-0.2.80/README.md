<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
-->
# gui_app portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_gui_app/master?logo=python)](
    https://gitlab.com/ae-group/ae_gui_app)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_gui_app)](
    https://pypi.org/project/ae-gui-app/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_gui_app/coverage.svg)](
    https://ae-group.gitlab.io/ae_gui_app/coverage/ae_gui_app_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_gui_app/mypy.svg)](
    https://ae-group.gitlab.io/ae_gui_app/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_gui_app/pylint.svg)](
    https://ae-group.gitlab.io/ae_gui_app/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_gui_app)](
    https://pypi.org/project/ae-gui-app/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_gui_app)](
    https://pypi.org/project/ae-gui-app/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_gui_app)](
    https://pypi.org/project/ae-gui-app/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_gui_app)](
    https://pypi.org/project/ae-gui-app/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_gui_app)](
    https://libraries.io/pypi/ae-gui-app)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_gui_app)](
    https://pypi.org/project/ae-gui-app/#files)


## installation


execute the following command to use the ae.gui_app sub-package in your
application. it will install ae.gui_app into your python (virtual) environment:
 
```shell script
pip install ae-gui-app
```

if you instead want to contribute to this portion then first fork
[the ae_gui_app repository at GitLab](https://gitlab.com/ae-group/ae_gui_app "ae.gui_app code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_gui_app):

```shell script
pip install -e .[dev]
```

the last command will install this sub-package portion into your virtual environment, along with
the tools you need to develop and run tests or to extend the portion documentation.
to contribute only to the unit tests or to the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

more info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.gui_app.html#module-ae.gui_app
"ae_gui_app documentation").

<!-- common files version 0.2.77 deployed version 0.2.75 (with 0.2.77)
     to https://gitlab.com/ae-group as ae_gui_app sub-package as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-gui-app as namespace portion ae-gui-app.
-->

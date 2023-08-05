# Speedup-Work-Lib

This repo is a library for speed up work

## Get Started
> There are **3 COMPONENTS** in Speedup Work Lib:<br/>
> - `file_tool.py` contain functions for dealing with file.<br/>
> - `simple_log.py` contain functions for a simple log.<br/>
> - `ssh_client.py` contain functions for creating SSH client to perform function on the remote computer.<br/>

## How to Deploy Package to Pypi Manually
```bash
pip freeze > requirements.txt
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
```

&copy; 2021

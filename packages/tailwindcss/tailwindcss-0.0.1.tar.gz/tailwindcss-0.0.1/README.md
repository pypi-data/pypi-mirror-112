# DJANGO TAILWINDCSS APPLICATION
![pypi](https://img.shields.io/pypi/v/tailwindcss) ![status](https://img.shields.io/pypi/status/tailwindcss)

This django application is used to apply [tailwindcss](https://tailwindcss.com) into project.


## Installation
You can install from this repository or from the pypi.

### From Repository

1. clone
```
git clone https://github.com/malinkaphann/tailwindcss.git
```
2. build the installer file
```
cd tailwindcss
make package
```

3. install tailwindcss from the project directory
```
cd ../my_project_dir
pip install ../tailwindcss/dist/tailwindcss-0.0.1.tar.gz
```

### From Pypi
[tailwindcss](https://pypi.org/project/tailwindcss/)

## Project Configuration
After the installation, it is time to configure the project.

update settings.py as the following.
```
INSTALLED_APPS = [
    'tailwindcss', # add this line
]
```

## How to use
At the top of the base.html, put this line.
```
{% include 'tailwindcss/base.html' %}
```

# UPLOAD
Commands in terminal

```
py -m twine upload --repository pypi dist/*
```

Install Lib

````
py -m pip install nascorp.library==version
````

Upgrade Lib

````
py -m pip install --upgrade nascorp.library==version
````

Install on requirements.txt

````
py -m pip install -r requirements.txt
````

Install on local

````
py -m pip install {DIRECTORY}/nascorp.library-*.*.*.tar.gz
````
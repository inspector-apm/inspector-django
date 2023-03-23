# Inspector | Code Execution Monitoring Tool

Inspector is a Code Execution Monitoring tool to help developers find out technical problems in their application automatically, before customers do.

## Requirements

- Python >= 3.x
- Django >= 4.x

## Install
Install the latest version of the package from PyPI:

```shell
pip install inspector-django
```

## Configure the Ingestion Key
In settings.py add the ingestion key of your project:

```python
INSPECTOR_INGESTION_KEY = "xxxxxxxxx"
```

### Get a new Ingestion Key
You can get a new key creating a new project in your [Inspector dashboard](https://app.inspector.dev).

## Activate the module
Add `inspector_django` to installed apps:
```python
INSTALLED_APPS = [
    ....,
 	
    'inspector_django',
]
```

## Attach the middleware
To monitor the incoming HTTP traffic you need to register the middleware. 
We suggest to add the middleware at the top of the list:

```python
MIDDLEWARE = [
	'inspector_django.InspectorMiddleware',
	
	....
]
```

## Official documentation
Checkout our [official documentation](https://docs.inspector.dev/guides/python) for more detailed tutorial.

## License
This library is licensed under the [MIT](LICENSE) license.
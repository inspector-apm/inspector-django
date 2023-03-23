# Inspector | Code Execution Monitoring Tool

Inspector is a Code Execution Monitoring tool to help developers find out technical problems in their application automatically, before customers do.

## Requirements

- Python >= 3.x
- Django >= 3.x

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

## Ignore URLs
It could be needed to exclude some parts of your application from your monitoring data. 
It could be something that doesn't impact your user experience, or if you prefer to focus your attention 
on a small part of your system.

The `INSPECTOR_IGNORE_URL` also support wildcards:

```python
INSPECTOR_IGNORE_URL = [
     'static*',
     'media*'
     'assets*',
     'js*',
     'css*',
]
```

This is the default array. You have to copy this property in your `settings.py` file 
and then add your custom entries. 

## Official documentation
Checkout our [official documentation](https://docs.inspector.dev/guides/django) for more detailed tutorial.

## License
This library is licensed under the [MIT](LICENSE) license.
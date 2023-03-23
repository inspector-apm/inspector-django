from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='inspector-django',
    version='0.1.1',
    description='Real-time Code Execution Monitoring of your Django applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Inspector',
    author_email='support@inspector.dev',
    url='https://inspector.dev/',
    install_requires=[
        'Django>=3',
        'inspector-python'
    ],
    project_urls={
        'Documentation': 'https://docs.inspector.dev/guides/django/',
        'Source Code': 'https://github.com/inspector-apm/inspector-django',
        'Issue Tracker': 'https://github.com/inspector-apm/inspector-django/issues',
    },
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    zip_safe=False,
    license='MIT'
)

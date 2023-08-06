# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['warehouse14']

package_data = \
{'': ['*'],
 'warehouse14': ['static/css/*',
                 'static/js/*',
                 'templates/*',
                 'templates/account/*',
                 'templates/project/*',
                 'templates/simple/*']}

install_requires = \
['Authlib>=0.15.4,<0.16.0',
 'Flask-HTTPAuth>=4.4.0,<5.0.0',
 'Flask-Login>=0.5.0,<0.6.0',
 'Flask-Markdown>=0.3,<0.4',
 'Flask-WTF>=0.15.1,<0.16.0',
 'Flask>=2.0.1,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pypitoken>=3.0.2,<4.0.0',
 'readme-renderer[md]>=29.0,<30.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'warehouse14',
    'version': '0.1.9',
    'description': 'A PyPI implementation for closed groups with authentication only',
    'long_description': '# Warehouse14\n\nWhile the PyPI (Warehouse) provides a global package index for all Python users, companies and closed groups do have the\nneed for a non-global Python package index.\n\nWhile [existing projects](#related-projects) provide different options for a private package index, Warehouse14 provides\nan implementation that requires authentication by default, but provides the option for a decentralized access management\non individual project level.\n\n## Features\n\n* Authentication via OIDC provider by default\n* User manageable API keys for download/upload\n* Project\n    * Project page\n    * Package metadata\n    * User access management\n        * **Admin** is able to modify package content and upload new versions. They also manage users.\n        * **Member** read access to private repositories.\n    * Project Types: Public (still require authentication) / Private (Access only for defined users)\n\n## Deployment\n\n> TODO 🙈\n\n### Deploy on AWS Lambda\n```python\nimport boto3\nfrom warehouse14 import OIDCAuthenticator, create_app\nfrom warehouse14.repos_dynamo import DynamoDBBackend, create_table\nfrom warehouse14.storage import S3Storage\n\n# requires apig_wsgi\nfrom apig_wsgi import make_lambda_handler\n\nconfig = {}\nconfig["SECRET_KEY"] = "{{ LONG_RANDOM_STRING }}"\nconfig["OIDC_USER_ID_FIELD"] = "email"\nconfig["OIDC_CLIENT_ID"] = "<your oidc client id>"\nconfig["OIDC_CLIENT_SECRET"] = "<your oidc client secret>"\nconfig["OIDC_SERVER_METADATA_URL"] = "https://<idp>/.well-known/openid-configuration"\nauth = OIDCAuthenticator()\n\ndynamodb = boto3.resource("dynamodb")\ntable = create_table(dynamodb, "table")\ndb = DynamoDBBackend(table)\n\nbucket = boto3.resource("s3").Bucket("<bucket name>")\nstorage = S3Storage(bucket)\n\napp = create_app(db, storage, auth, config=config)\nlambda_handler = make_lambda_handler(app, binary_support=True)\n```\n\n## Glossary\n\nTo use common Python terms we take over the glossary\nof [Warehouse](https://warehouse.readthedocs.io/ui-principles.html#write-clearly-with-consistent-style-and-terminology)\n\n| Term         | Definition                                                                                                                                                                                                        |\n| :----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |\n| Project      | A collection of releases and files, and information about them. Projects on Warehouse are made and shared by members of the Python community so others can use them.                                              |\n| Release      | A specific version of a project. For example, the requests project has many releases, like requests 2.10 and requests 1.2.1. A release consists of one or more files.                                             |\n| File         | Something that you can download and install. Because of different hardware, operating systems, and file formats, a release may have several files, like an archive containing source code or a binary wheel.      |\n| Package      | A synonym for a file.                                                                                                                                                                                             |\n| User         | A person who has registered an account on Warehouse.                                                                                                                                                              |\n| Account      | An object representing a logged in user.                                                                                                                                                                          |\n| Maintainer   | An user who has permissions to manage a project on Warehouse.                                                                                                                                                     |\n| Owner        | An user who has permissions to manage a project on Warehouse, and has additional permission to add and remove other maintainers and owners to a project.                                                          |\n| Author       | A free-form piece of information associated with a project. This information could be a name of a person, an organization, or something else altogether. This information is not linked to a user on Warehouse.   |\n\n## Related Projects\n\n* [warehouse](https://github.com/pypa/warehouse)\n* [pypiserver](https://pypi.org/project/pypiserver/)\n    * Backends:\n        * Filesystem\n    * upload supported\n    * different auth options\n* [pywharf](https://github.com/pywharf/pywharf)\n    * Backends:\n        * Filesystem\n        * Github\n    * server or github pages\n    * NO UPLOAD\n* [PyPICloud](https://pypicloud.readthedocs.io/en/latest/)\n    * Backends:\n        * Filesystem\n        * S3\n    * Cache via Redis, Dynamo, ...\n    * Upload supported\n    * Extendable\n* [lapypi](https://github.com/amureki/lapypi)\n    * almost fully PEP 503\n    * Backends:\n        * S3\n    * Uses Chalice\n* [plambdapi](https://github.com/berislavlopac/plambdapi)\n    * Uses Terraform\n    * Backends:\n        * S3\n    * Uses Chalice\n* [pypiprivate](https://github.com/helpshift/pypiprivate)\n    * static generator\n    * Backends:\n        * S3\n* [elasticpypi](https://github.com/khornberg/elasticpypi)\n    * Backends:\n        * S3/ Dynamodb\n    * serverless framework\n    * 10MB limit\n    * supports upload (strange /simple/post method)\n    * uses s3 trigger to update dynamodb entries\n* [devpypi](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html)\n',
    'author': 'Maic Siemering',
    'author_email': 'maic@siemering.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eruvanos/warehouse14',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

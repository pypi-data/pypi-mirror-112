# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iot_inspector_client',
 'iot_inspector_client.keys',
 'iot_inspector_client.queries']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=0.15.3,<0.16.0',
 'httpx>=0.17.0,<0.18.0',
 'importlib-resources>=5.1.2,<6.0.0',
 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'iot-inspector-client',
    'version': '0.1.1',
    'description': 'IoT Inspector API client',
    'long_description': '# IoT Inspector API Client\n\nThis is the official Python client for the\n[IoT Inspector](https://www.iot-inspector.com/) public API.\n\n# Usage\n\nFirst, you have to log in and select a tenant:\n\n```python\nfrom iot_inspector_client import Client\n\nYOUR_API_URL = "https://demo.iot-inspector.com/api"\n\nclient = Client(api_url=YOUR_API_URL)\n\nclient.login(EMAIL, PASSWORD)\ntenant = client.get_tenant("Environment name")\nclient.use_tenant(tenant)\n```\n\nAfter you logged in and selected the tenant, you can query the GraphQL API\n\n```python\nGET_ALL_FIRMWARES = """\nquery {\n  allFirmwares {\n    id\n    name\n  }\n}\n"""\nres = client.query(GET_ALL_FIRMWARES)\nprint(res)\n\nGET_PRODUCT_GROUPS = """\nquery {\n  allProductGroups {\n    id\n    name\n  }\n}\n"""\nres = client.query(GET_PRODUCT_GROUPS)\ndefault_product_group = next(pg for pg in res["allProductGroups"] if pg["name"] == "Default")\n```\n\nYou can upload firmwares:\n\n```python\nmetadata = FirmwareMetadata(\n    name="myFirmware",\n    vendor_name="myVendor",\n    product_name="myProduct",\n    product_group_id=default_product_group["id"],\n)\n\nfirmware_path = Path("/path/to/firmware.bin")\nres = client.upload_firmware(metadata, firmware_path, enable_monitoring=True)\nprint(res)\n```\n\n# Support\n\nYou can create a [new issue in this repo](https://github.com/IoT-Inspector/python-client/issues/new)\nor contact us at support@iot-inspector.com.\n',
    'author': 'IoT Inspector',
    'author_email': 'support@iot-inspector.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.iot-inspector.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)


# django-moova

## Starting
_These instructions will allow you to install the library in your python project._

### Current features

-   Create shipment.
-   Get tracking info.
-   Get shipping label.

### Pre-requisitos

-   Python >= 3.7
-   Django >= 3
-   requests >= 2
***
## Installation

1. To get the latest stable release from PyPi:
```
pip install django-moova
```
or

2. From a build
```
git clone https://gitlab.com/linets/ecommerce/oms/integrations/oms-moova
```

```
cd {{project}}
```

```
python setup.py sdist
```
and, install in your project django
```
pip install {{path}}/django-moova/dist/{{tar.gz file}}
```

3. Settings in django project

```
DJANGO_MOOVA = {
    'MOOVA': {
        'BASE_URL': '<MOOVA_BASE_URL>',
        'SECRET': '<MOOVA_SECRET_TOKEN>',
        'KEY': '<MOOVA_SECRET_KEY>',
        'CURRENCY': 'CLP',
        'TYPE': 'regular',
        'FLOW': 'manual',
        'INTERNALCODE': 'XX5555WWW123',
        'EXTRA': {},
        'ASSURANCE': False,
    },
    'REMITENTE': {
        'STREET': '<STREET>',
        'NUMBER': '<NUMBER>',
        'FLOOR': '<FLOOR>',
        'APARTMENT': '',
        'CITY': '<CITY>',
        'STATE': '<STATE>',
        'POSTALCODE': '<POSTAL_CODE>',
        'COUNTRY': 'CHL',
        'INSTRUCTIONS': 'Call before delivery',
        'FIRST_NAME': '<FIRST_NAME>',
        'LAST_NAME': '<LAST_NAME>',
        'EMAIL': '<EMAIL>',
        'PHONE': '<PHONE>',
    },
}
```

## Usage

1. Create shipment:
```
from moova.handler import MoovaHandler

handler = MoovaHandler()

default_data = handler.get_default_payload(instance)
default_data["currency"] = "CLP" # eg. (Optional)
response = handler.create_shipping(default_data)
```


2. Get tracking info:
```
from moova.handler import MoovaHandler

handler = MoovaHandler()

tracking_info = handler.get_tracking(<identifier>)
```


3. Get shipping label:
```
from moova.handler import MoovaHandler

handler = MoovaHandler()

label_info = handler.get_shipping_label(<shipping_id>)

Output:
'https://moova-user-data-test.s3.amazonaws.com/etiqueta-10x15.pdf'
```

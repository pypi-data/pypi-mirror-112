# Linets Bluexpress


## Starting 🚀
_These instructions will allow you to install the library in your django project._

### Current features 📋

-   Generate order in Bluexpress.
-   Generate default data for create order in Bluexpress.

### Pre-requisitos 📋

-   Python >= 3.7
-   Django >= 3
-   zeep >= 4
***
## Installation 🔧

1. To get the latest stable release from PyPi:
```
pip install django-bluexpress
```
or

2. From a build
```
git clone https://gitlab.com/linets/ecommerce/oms/integrations/oms-bluexpress
```

```
cd {{project}} && git checkout develop
```

```
python setup.py sdist
```
and, install in your project django
```
pip install {{path}}/oms-bluexpress/dist/{{tar.gz file}}
```

3. Settings in django project

```
DJANGO_BLUEXPRESS = {
    'BLUEXPRESS': {
        'ISSUE_WSDL': '<BLUEXPRESS_ISSUE_WSDL>',
        'TOKEN_ID': '<BLUEXPRESS_TOKEN_ID>',
        'USER_COD': '<BLUEXPRESS_USER_COD>',
        'COMPANY_CODE': '<BLUEXPRESS_COMPANY_CODE>',
        'SHIPPING_TYPE': '<BLUEXPRESS_SHIPPING_TYPE>',
        'PAYMENT_TYPE': '<BLUEXPRESS_PAYMENT_TYPE>',
        'PRODUCT_CODE': '<BLUEXPRESS_PRODUCT_CODE>',
        'CURRENCY_CODE': '<BLUEXPRESS_CURRENCY_CODE>',
        'SERVICE_TYPE_CODE': '<BLUEXPRESS_SERVICE_TYPE_CODE>',
        'PRODUCT_FAMILY_CODE': '<BLUEXPRESS_PRODUCT_FAMILY_CODE>',
    },
    'SENDER': {
        'PERSON_CODE': '<BLUEXPRESS_PERSON_CODE>',
        'ACCOUNT_CLIENT': '<BLUEXPRESS_ACCOUNT_CLIENT>',
        'RUT': '<BLUEXPRESS_RUT>',
        'DV': '<BLUEXPRESS_DV>',
        'NAME': '<BLUEXPRESS_NAME>',
        'STREET': '<BLUEXPRESS_STREET>',
        'NUMBER': '<BLUEXPRESS_NUMBER>',
        'FLOOR': '<BLUEXPRESS_FLOOR>',
        'DPTO': '<BLUEXPRESS_DPTO>',
        'PHONE_PREFIX': '<BLUEXPRESS_PHONE_PREFIX>',
        'PHONE_NUMBER': '<BLUEXPRESS_PHONE_NUMBER>',
        'PHONE_ANNEXED': '<BLUEXPRESS_PHONE_ANNEXED>',
        'COUNTRY_CODE': '<BLUEXPRESS_COUNTRY_CODE>',
        'REGION_CODE': '<BLUEXPRESS_REGION_CODE>',
        'COMMUNE_CODE': '<BLUEXPRESS_COMMUNE_CODE>',
        'LOCATION_CODE': '<BLUEXPRESS_LOCATION_CODE>'
    },
    'DESTINATARY': {
        'PHONE_PREFIX': '<BLUEXPRESS_PHONE_PREFIX>',
        'COUNTRY_CODE': '<BLUEXPRESS_COUNTRY_CODE>',
    },
}
```

## Usage 🔧

1. Generate default data for create a order in Bluexpress:
```
from bluexpress.handler import BluexpressHandler

handler = BluexpressHandler()
default_data = handler.get_default_payload(instance)

Output:

```

2. Create a order in Bluexpress:
```
from bluexpress.handler import BluexpressHandler

handler = BluexpressHandler()
response = handler.create_shipping(default_data)

Output:

```

3. Get events:
```
from bluexpress.handler import BluexpressHandler

handler = BluexpressHandler()

raw_data = {
    'carrier_tracking_number': int.
    'tracking_data': xml string.
}
response = handler.get_events(raw_data)

Output:
[{
    'city': string
    'state': string
    'description': string
    'date': string
}, ...]
```

4. Get status and if "is_delivered":
```
from bluexpress.handler import BluexpressHandler

handler = BluexpressHandler()

raw_data = {
    'carrier_tracking_number': int.
    'tracking_data': xml string.
}
response = handler.get_status(raw_data)

Output:
('Entregado', True)
```

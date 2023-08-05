# Linets Correos Chile


## Starting 🚀
_These instructions will allow you to install the library in your django project._

### Current features 📋

-   Generate order in Correos Chile.
-   Generate default data for create order in Correos Chile.

### Pre-requisitos 📋

-   Python >= 3.7
-   Django >= 3
-   zeep >= 4
***
## Installation 🔧

1. To get the latest stable release from PyPi:
```
pip install django-correos-chile
```
or

2. From a build
```
git clone https://gitlab.com/linets/ecommerce/oms/integrations/oms-correos-chile
```

```
cd {{project}} && git checkout develop
```

```
python setup.py sdist
```
and, install in your project django
```
pip install {{path}}/oms-correos-chile/dist/{{tar.gz file}}
```

3. Settings in django project

```
DJANGO_CORREOS_CHILE = {
    'CORREOS_CHILE': {
        'EXECUTE_WSDL': '<CORREOS_CHILE_EXECUTE_WSDL>',
        'USER': '<CORREOS_CHILE_USER>',
        'PASSWORD': '<CORREOS_CHILE_PASSWORD>',
        'COD_SERVICIO': '<CORREOS_CHILE_COD_SERVICIO>',
        'COD_REF': '<CORREOS_CHILE_COD_REF>',
        'TYPE_POR': '<CORREOS_CHILE_TYPE_POR>',
        'DEV_CON': '<CORREOS_CHILE_DEV_CON>',
        'PAG_SEG': '<CORREOS_CHILE_PAG_SEG>',
    },
    'SENDER': {
        'ADMISSION': '<CORREOS_CHILE_ADMISSION>',
        'CLIENT': '<CORREOS_CHILE_CLIENT>',
        'CENTRO': '<CORREOS_CHILE_CENTRO>',
        'NAME': '<CORREOS_CHILE_NAME>',
        'ADDRESS': '<CORREOS_CHILE_ADDRESS>',
        'COUNTRY': '<CORREOS_CHILE_COUNTRY>',
        'POSTALCODE': '<CORREOS_CHILE_POSTALCODE>',
        'CITY': '<CORREOS_CHILE_CITY>',
        'RUT': '<CORREOS_CHILE_RUT>',
        'CONTACT_NAME': '<CORREOS_CHILE_CONTACT_NAME>',
        'CONTACT_PHONE': '<CORREOS_CHILE_CONTACT_PHONE>',
    },
}
```

## Usage 🔧

1. Generate default data for create a order in Correos Chile:
```
from correos_chile.handler import CorreosHandler

handler = CorreosHandler()
default_data = handler.get_default_payload(instance)

Output:
{
    'recipient_name': 'Ascensión Paniagua',
    'recipient_address': 'Jessica Villaverde 8752',
    'recipient_postal_code': 'PROV',
    'recipient_commune': 'Providencia',
    'recipient_rut': '41.460.173-4',
    'recipient_contact': 'Ascensión Paniagua',
    'recipient_phone': '9999999999'
}
```

2. Create a order in Correos Chile:
```
from correos_chile.handler import CorreosHandler

handler = CorreosHandler()
response = handler.create_shipping(default_data)

Output:
{
    'ExtensionData': None,
    'CodigoSucursal': None,
    'NombreSucursal': None,
    'Cuartel': None,
    'Sector': None,
    'SDP': None,
    'Movil': None,
    'AbreviaturaCentro': '61001',
    'CodigoDelegacionDestino': '864',
    'NombreDelegacionDestino': 'PLANTA CEP RM',
    'DireccionDestino': 'JESSICA VILLAVERDE 8752',
    'CodigoEncaminamiento': '02475000007',
    'GrabarEnvio': 'S',
    'NumeroEnvio': '990077321938',
    'ComunaDestino': 'PROVIDENCIA',
    'AbreviaturaServicio': 'PED',
    'IdTransaccional': None,
    'CodigoAdmision': 'PRB20201103'
}
```

3. Get events:
```
from correos_chile.handler import CorreosHandler

handler = CorreosHandler()

raw_data = {
    'expedicion': '990077324935',
    'referencia': 'CLV-10000001',
    'estado_2': 'ENVIO ENTREGADO',
    'fechaEvento': '12/12/2021',
    'fechaCarga': '12/12/2021',
    'estadoBase': 'Envio en reparto',
    'ciudad': 'Santiago'
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
from correos_chile.handler import CorreosHandler

handler = CorreosHandler()

raw_data = {
    'expedicion': '990077324935',
    'referencia': 'CLV-10000001',
    'estado_2': 'ENVIO ENTREGADO',
    'fechaEvento': '12/12/2021',
    'fechaCarga': '12/12/2021',
    'estadoBase': 'Envio en reparto',
    'ciudad': 'Santiago'
}
response = handler.get_status(raw_data)

Output:
('Entregado', True)
```

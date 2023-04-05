import requests
import json
import logging


logging.basicConfig(level=logging.INFO)

URL_AUTORIZATION = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/authorization'

s = requests.session()

SERVICE_KEY = s.get('https://carrinho-inusd5bbia-rj.a.run.app/Login/GetServiceKey').json()

AUTORIZATION_PAYLOAD = {
    'username': 'default',
    'key': SERVICE_KEY['serviceKey']
}

REQUEST = s.post(URL_AUTORIZATION, data=json.dumps(AUTORIZATION_PAYLOAD))

REQUEST_JSON = REQUEST.json()

API_TOKEN = REQUEST_JSON['api_token']

LOGIN_PAYLOAD = {
    "email": "leonardo@coopertotal.com.br",
    "password": "1234",
    "storeid": 0
}

URL_LOGIN = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/login&api_token=' + API_TOKEN

logging.info(' Realizando login...')

REQUEST = s.post(URL_LOGIN, data=json.dumps(LOGIN_PAYLOAD))

REQUEST_JSON = REQUEST.json()

URL_ADRESS = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/addresses&api_token=' + API_TOKEN

REQUEST = s.post(URL_ADRESS, data=json.dumps({'customer_id': REQUEST_JSON['customer']['customer_id']}))

REQUEST_JSON = REQUEST.json()

FEDERAL_TAX_ID = '62.973.677/0001-63'

ADDRESS_ID = ''

for farmacia in REQUEST_JSON['addresses']:
    if FEDERAL_TAX_ID == farmacia['federal_tax_id']:
        ADDRESS_ID = farmacia['address_id']
        logging.info(' Farmácia: ' + farmacia['federal_tax_id'] + ' ' + farmacia['company'])

logging.info(' Buscando informações no site...')

URL_FEDERAL_TAX = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/address&api_token=' + API_TOKEN

REQUEST = s.post(URL_FEDERAL_TAX, data=json.dumps({'address_id': ADDRESS_ID}))

URL_COMERCIAL_CONDITIONS = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/commercial_conditions&api_token=' + API_TOKEN

REQUEST = s.post(URL_COMERCIAL_CONDITIONS, data=json.dumps({'address_id': ADDRESS_ID}))

REQUEST_JSON = REQUEST.json()

PAY_TERM = ''
COMERCIAL_CONDITION_ID = REQUEST_JSON['commercial_conditions'][0]['commercial_condition_id']

for pay_terms in REQUEST_JSON['commercial_conditions'][0]['pay_terms']:
    if pay_terms['pay_term_id'] == 1:
        PAY_TERM = pay_terms['pay_term_id']
        logging.info(' Condição selecionada: '+ REQUEST_JSON['commercial_conditions'][0]['name'] + ' | Prazo de pagamento: ' + pay_terms['name'])

logging.info(' Abrindo produtos...')
logging.info(' Montando carrinho...')

URL_CART = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/get_cart_ui&api_token=' + API_TOKEN

REQUEST = s.post(URL_CART, data=json.dumps({'address_id': ADDRESS_ID, 'commercial_condition_id': COMERCIAL_CONDITION_ID}))

URL_PRODUCTS = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/produtos_integracao_target&api_token=' + API_TOKEN

REQUEST = s.post(URL_PRODUCTS, data=json.dumps({'commercial_condition_id': COMERCIAL_CONDITION_ID, 'pay_term_id': PAY_TERM}))

REQUEST_JSON = REQUEST.json()

for product in REQUEST_JSON['products']:
    if product['ean'] == '7897595901927':
        logging.info(' Produto Adicionado. Ean: ' + product['ean'] + ' | Qtd: 2 | Estoque: ' + str(product['quantity']))
    if product['ean'] == '7896241225547':
        logging.info(' Produto Adicionado. Ean: ' + product['ean'] + ' | Qtd: 1 | Estoque: ' + str(product['quantity']))

URL_CONFIRM = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/commercial_condition_associated&api_token=' + API_TOKEN

REQUEST = s.post(URL_CONFIRM, data=json.dumps({'commercial_condition_id': COMERCIAL_CONDITION_ID}))

URL_CONFIRM = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/produtos_integracao_target&api_token=' + API_TOKEN

REQUEST = s.post(URL_CONFIRM, data=json.dumps({'commercial_condition_id': COMERCIAL_CONDITION_ID, 'pay_term_id': PAY_TERM}))

logging.info(' Enviando pedido...')

URL_CONFIRM = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/cart_add&api_token=' + API_TOKEN

DATA_CONFIRM = {
    "products":[{"ean":"7897595901927",
                 "discount":5,
                 "price":62.98,
                 "product_id":34748,
                 "quantity":2,
                 "name":"AAS INFANTIL 100MG 120CPR",
                 "manufacturer":"HYPERA PP",
                 "tax":1.56,
                 "category":"ANALGESICOS E ANTIPIRETICOS","cashback":0},
                 {"ean":"7896241225547",
                  "discount":5,
                  "price":52.68,
                  "product_id":30,
                  "quantity":1,
                  "name":"ABLOK PLUS 100/25MG 30CPR",
                  "manufacturer":"BIOLAB SANUS",
                  "tax":1.09,
                  "category":"ANTI-HIPERTENSIVOS",
                  "cashback":0}]
}

REQUEST = s.post(URL_CONFIRM, data=json.dumps(DATA_CONFIRM))

URL_CONFIRM = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/commercial_condition&api_token=' + API_TOKEN
DATA_CONFIRM = {
    "commercial_condition_id":"103",
    "commercial_condition":"CONDIÇÃO DIAMANTE A PRAZO",
    "pay_term_id":"1",
    "name":"42 DIAS",
    "code":"001",
    "minimum_value":"100",
    "comercial_condition_queue":""
}

REQUEST = s.post(URL_CONFIRM, data=json.dumps(DATA_CONFIRM))

URL_CONFIRM = 'https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/order&api_token=' + API_TOKEN

DATA_CONFIRM = {"customer_id":"3326","order_id":"620774","integrated":"false"}

REQUEST = s.post(URL_CONFIRM, data=json.dumps(DATA_CONFIRM))

logging.info(' Pedido enviado!')

REQUEST_JSON = REQUEST.json()

FINAL_JSON = {
    'order_status_id': REQUEST_JSON['order']['order_status_id'],
    'order_status': REQUEST_JSON['order']['order_status']
}

with open('status.json', 'w') as arquivo:
    json.dump(FINAL_JSON, arquivo)
import requests
import hashlib
import time
import json
import re
import sys
import urllib.parse
import base64


class MyError(Exception):
    def __init__(self, value='Ошибка'):
        self.msg = value

    def __str__(self):
        return self.msg


class muapi_client:
    def __init__(self, private_key, public_key, API_host):
        self.priv_key = private_key
        self.pub_key = public_key
        self.API_host = API_host

    def get_params(self, path, data):
        url = 'http://' + self.API_host + path
        date_utc = int(time.time())
        data['time'] = date_utc
        data = json.dumps(data)
        data = data.encode('utf-8')
        data = str(base64.b64encode(data))
        sign = hashlib.sha256((data + self.priv_key).encode()).hexdigest()
        meta = None
        params = {
            'data': data,
            'format': 'b64',
            'public_key': self.pub_key,
            'sign': sign,
            'meta': meta
        }
        return params, url

    def connect(self):
        params, url = self.get_params(path='/auth', data={})
        r = requests.post(url=url, data=params)
        print(r.json())
        r.json()

    def get_resources(self):
        params, url = self.get_params(path='/resources', data={})
        r = requests.post(url=url, data=params)
        print(r.json())

    def get_all_catalogs(self, resource):
        if isinstance(resource, dict):
            data = {
                'resource': resource['name'].lower(),
                'catalog': {}
            }
        else:
            data = {
                'resource': resource.lower(),
                'catalog': {}
            }
        params, url = self.get_params(path='/resource/catalog', data=data)
        r = requests.post(url=url, data=params)
        data_dict = r.json()['data']
        if data_dict != 'not found':
            return data_dict

    def get_resource(self, resource):
        if isinstance(resource, dict):
            data = {'resource': resource['name'].lower()}
        else:
            data = {'resource': resource.lower()}
        params, url = self.get_params(path='/resource', data=data)
        r = requests.post(url=url, data=params)
        # print(r)
        # print(r.json())
        data_dict = r.json()['data']
        if data_dict != 'not found':
            id_resource = data_dict['id']
        else:
            id_resource = None
        return id_resource

    def encode_url(self, url):
        url_list = url.split('?')
        if len(url_list) > 1:
            url = url.split('?')[0] + '?' + urllib.parse.quote(url.split('?')[1])
        else:
            url = url.split('?')[0]
        return url

    def add_resource(self, resource_name='', resource_url=''):
        if resource_url == '':
            raise MyError(value='Не передано поле "url"')
        resource_url = self.encode_url(resource_url)
        resource = {
            'name': resource_name.lower(),
            'url': resource_url
        }
        data = {'resource': resource}
        if resource['name'] == '':
            raise MyError(value='Не передано поле "name"')
        p = re.compile(r'https?://.+?\..+')
        check_url = p.findall(resource['url'])
        if len(check_url) == 0:
            raise MyError(value='Передана не правильная структура url')
        p = re.compile(r'/$')
        resource['url'] = p.sub('', resource['url'])
        id_resource = self.get_resource(resource)
        if id_resource is None:
            params, url = self.get_params(path='/resource/add', data=data)
            requests.post(url=url, data=params)
            print(f'Ресурс "{resource_name}" был добавлен в базу')
        else:
            print(f'Ресурс "{resource_name}" уже существует в базе')

    def add_catalog(self, resource_name, catalog_name='', catalog_url='', description=None, external_id=None,
                    parents=None, parent_id=None, image=None, additional=None, uniform_name=None, region=None, logger=None):
        if parents is None:
            parents = []
        if catalog_url == '':
            raise MyError(value='Не передано поле "url"')
        catalog_url = self.encode_url(catalog_url)
        catalog = {
            'name': catalog_name.capitalize(),
            'url': catalog_url,
            'description': description,
            'external_id': external_id,
            'parents': parents,
            'parent_id': parent_id,
            'image': image,
            'additional': additional,
            'uniform_name': uniform_name,
            'region': region
        }
        data = {
            'resource': resource_name,
            'catalog': catalog
        }
        if catalog['name'] == '':
            raise MyError(value='Не передано поле "name"')
        p = re.compile(r'https?://.+?\..+')
        check_url = p.findall(catalog['url'])
        if len(check_url) == 0:
            if logger is not None:
                logger.info(
                    f'\n--------------------------------\nurl: {catalog["url"]}\n--------------------------------\n')
            raise MyError(value='Передана не правильная структура url')
        id_resource = self.get_resource(resource_name)
        if id_resource is None:
            raise MyError(value='Указанного ресурса нет в базе.')
        data_dict = self.get_catalog_list(resource=resource_name, catalog_name=catalog['name'], catalog_url=catalog_url, region=region)
        if len(data_dict) > 0:
            id_catalog = data_dict[0]['id']
        else:
            id_catalog = None
        catalog_name = catalog['name']
        if id_catalog is None:
            params, url = self.get_params(path='/resource/catalog/add', data=data)
            r = requests.post(url=url, data=params)
            # print(r.json())
            error = r.json()['error']
            if error is None:
                pass
                # print(f'Каталог "{catalog_name}" добавлен в базу')
            else:
                print(f'Произошла ошибка: "{error}"')
        else:
            params, url = self.get_params(path='/resource/catalog/add', data=data)
            r = requests.post(url=url, data=params)
            print(r.json())
            error = r.json()['error']
            if error is None:
                print(f'Каталог "{catalog_name}" обновлен')
            else:
                print(f'Произошла ошибка: "{error}"')

    def add_item(self, resource_name, item_name='', item_url='', description=None, external_id=None,
                 catalogs: list = None, catalog_id=None, image=None, price: float = None, currency=None,
                 additional=None, uniform_name=None, region=None, brand=None):
        if catalogs is None:
            catalogs = []
        if item_url == '':
            raise MyError(value='Не передано поле "url"')
        item_url = self.encode_url(item_url)
        item = {
            'name': item_name,
            'url': item_url,
            'description': description,
            'external_id': external_id,
            'catalogs': catalogs,
            'catalog_id': catalog_id,
            'currency': currency,
            'additional': additional,
            'uniform_name': uniform_name,
            'region': region,
            'brand': brand
        }
        if price is not None:
            item['price'] = price
        if image is not None:
            item['image'] = image
        data = {
            'resource': resource_name,
            'item': item
        }
        if item['name'] == '':
            raise MyError(value='Не передано поле "name"')
        if item['url'] == '':
            raise MyError(value='Не передано поле "url"')
        p = re.compile(r'https?://.+?\..+')
        check_url = p.findall(item['url'])
        if len(check_url) == 0:
            raise MyError(value='Передана не правильная структура url')
        if item['catalog_id'] is None:
            raise MyError(value='Не передано поле "catalog_id"')
        id_resource = self.get_resource(resource_name)
        if id_resource is None:
            raise MyError(value='Указанного ресурса нет в базе.')
        params, url = self.get_params(path='/resource/catalog/item/add', data=data)
        # print(resource_name, item_name, item_url, region)
        data_item = self.get_item_list(resource=resource_name, item_name=item_name, item_url=item_url, region=region)
        r = requests.post(url=url, data=params)
        error = r.json()['error']
        # print(data_item)
        if error is None and len(data_item['item']) == 0:
            print('Объект успешно добавлен в базу')
        elif error is None and len(data_item['item']) > 0:
            print('Объект успешно обновлен')
        else:
            raise MyError(value=error)

    def get_catalog_list(self, catalog_name, resource, region=None, catalog_url=None, parent_id=None, logger=None):
        data = {
            'resource': resource,
            'catalog': {'name': catalog_name.capitalize()
                        }
        }
        if parent_id is not None:
            data['catalog']['parent_id'] = parent_id
        if catalog_url is not None:
            catalog_url = self.encode_url(catalog_url)
            data['catalog']['url'] = catalog_url
        if region is not None:
            data['catalog']['region'] = region

        params, url = self.get_params(path='/resource/catalog', data=data)
        r = requests.post(url=url, data=params)
        # print(r.json())
        # print(
        #     f'get catalog list params, {catalog_name}, {resource}, {region}, {catalog_url} \n{r.status_code}; {r.text}')
        try:
            data_dict = r.json()['data']
            if data_dict == 'resource is not found':
                raise MyError(value='Неправильно указан ресурс')
            return data_dict
        except Exception as e:
            if logger is not None:
                logger.info(f'get catalog list params, {catalog_name}, {resource}, {region}, {catalog_url} \n{r.status_code}; {r.text}')
                logger.info(f'request data: {data}, {int(time.time())}\n--------------------------------')
                logger.error("Exception occurred", exc_info=True)
                # logger.error(sys.exc_info()[2])
            else:
                print(f'get catalog list params, {catalog_name}, {resource}, {region}, {catalog_url} \n{r.status_code}; {r.text}')
                print(sys.exc_info())
            raise MyError('Error')

    def get_item_list(self, resource, item_name, item_url=None, region=None, catalog_id=None):
        item_url = self.encode_url(item_url)
        data = {
            'resource': resource,
            'item': {'name': item_name}
        }
        if item_url is not None:
            data['item']['url'] = item_url
        if catalog_id is not None:
            data['item']['catalog_id'] = catalog_id
        if region is not None:
            data['item']['region'] = region
        params, url = self.get_params(path='/resource/catalog/item', data=data)
        r = requests.post(url=url, data=params)
        data_dict = r.json()['data']
        if data_dict == 'resource is not found':
            raise MyError(value='Указанного ресурса не существует в базе')
        return data_dict

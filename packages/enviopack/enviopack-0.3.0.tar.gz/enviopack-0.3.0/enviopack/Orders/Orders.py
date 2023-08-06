# -*- coding: utf-8 -*-
import datetime
from typing import List

from enviopack import Auth, Enviopack, Pickings
from enviopack.constants import BASE_API_URL
from requests import get, post, delete

base_path = '/pedidos'

class Orders(Enviopack):
  """
  Es la entidad que representa al pedido u orden en tu aplicación. Tiene los datos básicos para poder identificar un pedido de tu plataforma en EnvioPack
  Parámetro	¿Es Obligatorio?	Tipo de Dato	Observaciones
  id_externo	Sí	String	Máx. 30 caracteres
  nombre	Sí	String	Máx. 30 caracteres
  apellido	Sí	String	Máx. 30 caracteres
  email	Sí	String	Máx. 100 caracteres
  telefono	No	String	Máx. 30 caracteres
  celular	No	String	Máx. 30 caracteres
  monto	Sí	Numero	Hasta 2 dígitos decimales
  fecha_alta	Sí	Fecha	Ej. 2016-04-26 13:52:00
  pagado	Sí	Booleano	Recordá que Booleano no es String
  provincia	No	ID	Deberá informarse el valor ID devuelto por el webservice de provincias. Los IDs de provincias están bajo el estándar ISO_3166-2:AR sin el prefijo AR-.
  localidad	No	String	Máx. 50 caracteres
  productos	Condicional	Array	Si tenes tu maestro de productos cargados en Enviopack podes indicarnos que productos tiene asociado el pedido.

  El uso del parametro "productos" de implementación obligatoria si usas el servicio de Fulfillment

  El valor esperado es un array JSON, donde cada posición del array debe contener un objeto JSON formado por:
  - tipo_identificador: las opciones posibles son ID o SKU
  - identificador: aquí debes ingresar el ID o SKU
  - cantidad: Un numero, sin dígitos decimales
  Mediante el campo tipo_identificador, te permitimos asociar productos a un pedido a partir del ID del producto asignado por Enviopack o simplemente por el SKU propio del producto, la elección es tuya.
  empresa	No	ID	Este parámetro solo esta disponible para cuentas marketplaces. Permite crear un pedido en la cuenta de un seller y asociado a la cuenta marketplace.
  Te recomendamos revisar la sección Marketplaces en esta API Docs.
  """
  id:int
  external_id:str
  name:str
  last_name:str
  email:str
  amount:float
  #TODO GET STRING ON THIS FORMAT 2016-04-26 13:52:00
  create_date:str
  payed:bool

  phone:str
  mobile_phone:str
  state:int
  city:str
  products:List[str]
  response:dict
  company:int

  # pickings:List[Pickings]

  def __init__(self, auth:Auth, base_path=base_path, **kwargs):
    super().__init__(auth, base_path=base_path, **kwargs)
    

  def __repr__(self):
    return '(Order: name {name}, amount {amount})'.format(name=self.name + ' ' + self.last_name, amount=self.amount)

  @classmethod
  def create_order(cls, auth:Auth, external_id:str, name:str, last_name:str, email:str, amount:float, create_date:str, payed:bool, **kwargs):
    order = cls(auth, **kwargs)
    order.external_id:str = external_id
    order.name:str = name
    order.last_name:str = last_name
    order.email:str = email
    order.amount:float = amount
    order.create_date:str = create_date
    order.payed:bool = payed
    order.response = order._post_order()
    return order
  
  @classmethod
  def get_order(cls, auth:Auth, id:int):
    order = cls(auth)
    order_vals = order.get_order_by_id(id, auth.access_token)
    
    order._set_attributes_from_response(order_vals, {
    "empresa":'company',
    "provincia": "state",
    "id": 'id',
    "id_externo": "external_id",
    "nombre": "name",
    "apellido": "last_name",
    "email": "email",
    "telefono": "phone",
    "celular": "mobile_phone",
    "localidad": "city",
    "monto": 'amount',
    "fecha_alta": "create_date",
    "pagado": 'payed',
    "pedido_productos": 'products',
    })
    return order

  @classmethod
  def search_orders(cls,auth, from_create_date=None, to_create_date=None, external_id=None, page=None ):
    """
    GET /pedidos
      Permite buscar por diversos parametros sobre el listado de pedidos"""
    access_token = auth.access_token
    url = "{base_url}{base_path}".format(base_url=BASE_API_URL, base_path=base_path )
    params = {}
    if from_create_date: 
      params.update({'fecha_alta_desde':from_create_date})
    if to_create_date: 
      params.update({'fecha_alta_hasta':to_create_date})
    if external_id: 
      params.update({'id_externo':external_id})
    if page: 
      params.update({'pagina':page})
    orders = []
    while True:
      response = get(url,params)
      json_resp = response.json()
      orders += json_resp.get('pedidos')
      if json_resp.get('total_paginas') > 1 and json_resp.get('pagina') < json_resp.get('total_paginas'):
        if not page:
          page = 1
        page += 1
        params.update({'pagina':page})
      else: break
    [cls(auth)._set_attributes_from_response(order, {
    "empresa":'company',
    "provincia": "state",
    "id": 'id',
    "id_externo": "external_id",
    "nombre": "name",
    "apellido": "last_name",
    "email": "email",
    "telefono": "phone",
    "celular": "mobile_phone",
    "localidad": "city",
    "monto": 'amount',
    "fecha_alta": "create_date",
    "pagado": 'payed',
    "pedido_productos": 'products',
    }) for order in orders]

  @staticmethod
  def get_order_by_id(id, access_token) -> dict:
    """
    GET /pedidos/[ID]
    """
    url = "{base_url}{base_path}/{id}".format(base_url=BASE_API_URL, base_path=base_path, id=id )
    response = get(url, {'access_token':access_token})
    return response.json()
  
  def get_order_pickings(self):
    """
    GET /pedidos/[ID]/envios
    """
    pickings = self.pickings
    if pickings:
      return pickings
    url = "{base_url}{base_path}/{id}/envios".format(base_url=self.base_request_url, base_path=self.base_request_path,id=self.id )
    raise NotImplementedError
    #TODO finish when implemented pickings
    response = get(url, {'access_token':self.auth.access_token})
    pickings_json = response.json()
    pickings = Pickings.from_array(pickings_json)
    self.pickings = pickings
    return pickings
  
  # def __del__(self):
  #   """
  #   DELETE /pedidos/[ID]
  #   """
  #   url = "{base_url}{base_path}/{id}".format(base_url=self.base_request_url, base_path=self.base_request_path,id=self.id )
  #   response = delete(url, {'access_token':self.auth.access_token})
  #   del self
  #   return response.json()

  def _post_order(self) -> dict:
    """
    POST /pedidos
      Crea un nuevo pedido en EnvioPack.  
    """
    url = "{base_url}{base_path}".format(base_url=self.base_request_url, base_path=self.base_request_path )
    access_token = self.auth.access_token
    if not access_token:
      raise Exception('No access token defined')

    mandatory_params = {
      'id_externo':self.external_id,
      'nombre': self.name,
      'apellido':self.last_name,
      'email':self.email,
      'monto':self.amount,
      'fecha_alta':self.create_date,
      'pagado':self.payed,
    }
    params = self._optional_params(mandatory_params, optional_fields={
      "phone":"telefono",
      "mobile_phone":"celular",
      "state":"provincia",
      "city":"localidad",
      "products":"productos",
      "company":"empresa",
      })

    response = post(url,params={'access_token':access_token,} ,json=params)
    rspjson = response.json()
    if response.status_code == 200:
      self.id = rspjson.get('id')
      return rspjson
    else:
      raise Exception(f'El pedido no se pudo crear, revisar los parametros utilizados: \n {rspjson}')

# -*- coding: utf-8 -*-
import requests
from enviopack import Enviopack
from enviopack.constants import BASE_API_URL
from enviopack import Auth
from enviopack.Orders.Orders import Orders
from typing import Dict, List
import json
base_path='/envios'

class Pickings(Enviopack):
  """
  Parámetro	¿Es Obligatorio?	Tipo de Dato	Observaciones
  pedido	Sí	ID	ID del pedido al que corresponde este envío
  direccion_envio	Condicional	ID	ID que identifica la dirección, por donde el correo pasara a retirar la mercadería a enviar.
  Podes obtenerlo ingresando en Configuración / Mis Direcciones
  destinatario	Condicional	String	Máx. 50 caracteres
  observaciones	No	String	
  usa_seguro	No	Booleano	Recordá que Booleano no es String.
  Si completas este campo con null o no lo envias en el request se completara automaticamente según el modo de seguro elegido en tus preferencias
  confirmado	Sí	Booleano	Recordá que Booleano no es String.
  productos
        o
  paquetes	Condicional	Array	Podes enviar uno de estos dos campos posibles: "productos" o "paquetes".

  Si tenes tu maestro de productos cargados en Enviopack podes simplemente indicarnos que productos tiene el envío y nosotros nos ocupamos de separarlo en paquetes segun la configuracion que haya elegido dentro de cada producto.

  El uso del parametro "productos" de implementación obligatoria si usas el servicio de Fulfillment. También es nuestra opción recomendada

  Si por el contrario queres especificamente indicar como se conforma cada paquete en particular tambien podes hacerlo.

  Si vas a usar el campo "productos"
  El valor esperado es un array JSON, donde cada posición del array debe contener un objeto JSON formado por:
  - tipo_identificador: las opciones posibles son ID o SKU
  - identificador: aquí debes ingresar el ID o SKU
  - cantidad: Un numero, sin dígitos decimales
  Mediante el campo tipo_identificador, te permitimos asociar productos a un envío a partir del ID del producto asignado por Enviopack o simplemente por el SKU propio del producto, la elección es tuya.

  Si vas a usar el campo "paquetes"
  El valor esperado es un array JSON, donde cada posición del array debe contener un objeto JSON formado por:
  - alto: en cm. y sin dígitos decimales
  - ancho: en cm. y sin dígitos decimales
  - largo: en cm. y sin dígitos decimales
  - peso: en kg. y con hasta 2 dígitos decimales
  - descripcion_primera_linea: String (Máx. 50 caracteres)
  - descripcion_segunda_linea: String (Máx. 50 caracteres)
  tiene_fulfillment	Condicional	Booleano	Recordá que Booleano no es String.
  Debes indicar si el envio será despachado desde el deposito de fullpack.

  En el caso de que no tengas es el servicio de Fullpack activado el valor por defecto es false. En caso de que si lo tengas activado el valor por defecto es true.
  despacho	Condicional	String	Indica si el operador logistico debe retirar el paquete por el deposito del vendedor o si el vendedor lo va a acercar a una sucursal.
  Los valores posibles son:
  - D: retiro por domicilio
  - S: despacho desde sucursal
  modalidad	Sí	String	Los valores posibles son:
  - D: para envíos a domicilio
  - S: para envíos a sucursal
  servicio	Condicional	String	Los valores posibles son:
  - N: para el servicio estándar
  - P: para el servicio prioritario
  - X: para el servicio express
  - R: para el servicio de devoluciones
  Si el envío es a domicilio
  correo	Condicional	ID	Deberá informarse el valor ID devuelto por el webservice de correos.
  Por ejemplo para FastMail su ID es fastmail.
  calle	Condicional	String	Máx. 50 caracteres
  numero	Condicional	String	Máx. 5 caracteres
  piso	No	String	Máx. 6 caracteres
  depto	No	String	Máx. 4 caracteres
  referencia_domicilio	No	String	Máx. 30 caracteres
  codigo_postal	Condicional	Numero	Entero de 4 dígitos
  provincia	Condicional	ID	Deberá informarse el valor ID devuelto por el webservice de provincias. Los IDs de provincias están bajo el estándar ISO_3166-2:AR sin el prefijo AR-.
  localidad	Condicional	String	Máx. 50 caracteres
  Si el envío es a sucursal
  sucursal	Condicional	ID	Deberá informarse el valor ID devuelto por el webservice de sucursales.

  Utilizando el campo "productos" (Obligatorio para uso de Fulfillment)
  {
			"pedido":353,
			"direccion_envio":1,
			"destinatario":"Juan Perez",
			"observaciones":"Timbre 5 - 3 - Campana",
			"modalidad":"D",
			"servicio":null,
			"correo":null,
			"confirmado":false,
			"productos":[
				{"tipo_identificador":"SKU","identificador":"ABC1234","cantidad":1},
				{"tipo_identificador":"ID","identificador":65811,"cantidad":2},
			],
			"calle":"Ambrosetti",
			"numero":"435",
			"piso":"5",
			"depto":"C",
			"codigo_postal":"1405",
			"provincia":"C",
			"localidad":"Caballito"
		}'

  Utilizando el campo "paquetes"
  {
			"pedido":353,
			"direccion_envio":1,
			"destinatario":"Juan Perez",
			"observaciones":"Timbre 5 - 3 - Campana",
			"modalidad":"D",
			"servicio":null,
			"correo":null,
			"confirmado":false,
			"paquetes": [
				{"alto":52,"ancho":42,"largo":3,"peso":2},
				{"alto":52,"ancho":42,"largo":4,"peso":2.5}
			],
			"calle":"Ambrosetti",
			"numero":"435",
			"piso":"5",
			"depto":"C",
			"codigo_postal":"1405",
			"provincia":"C",
			"localidad":"Caballito"
		}'
  """

  order:Orders
  confirmed:bool
  mode:str

  sender_address:int
  service:str 
  dispatch:str
  has_fullfilment:bool
  receiver:str

  observations:str  = False
  uses_insurance:bool = None

  products:List[dict] = False
  packages:List[dict] = False
  
  carrier:int 
  street:str 
  st_number:str 
  zip_code:int 
  state:str 
  city:str 
  
  floor:str  = None
  apartment:str = None
  address_reference:str = None

  post_office:int  

  response:dict

  def __init__(self, auth, order, confirmed, mode, base_path=base_path, **kwargs):
    super().__init__(auth, base_path=base_path,**kwargs)
    if 'packages' in kwargs and 'products' in kwargs:
       raise Exception('Please use either packages or products')
    self.order, self.confirmed, self.mode = order, confirmed, mode
  
  def __repr__(self):
    return '(Picking: order {order}, confirmed {confirmed})'.format(order=self.order.id, confirmed=self.confirmed)

  @classmethod
  def from_array(cls, pickings_json):
    return [cls(picking) for picking in pickings_json]

  @classmethod
  def create_with_products(cls, auth, order, confirmed, mode, products, **kwargs):
    #todo add request to create picking
    picking = cls(auth, order, confirmed, mode)
    picking.products = products
    if 'packages' in kwargs:
      raise Exception('Use create_with_packages constructor to use packages')
    #TODO add products
    pass
    return picking
  
  @classmethod
  def create_with_packages(cls, auth, order, confirmed:bool, mode:str, packages:List[dict], **kwargs):
    """
    @auth
    @order
    @confirmed
    @mode
    @packages
    
    If confirmed True the following params must be set
    @sender_address 
    @has_fullfilment
    @dispatch
    @service
    @receiver
    """
    #todo add request to create picking
    picking = cls(auth, order, confirmed, mode, **kwargs)
    picking.packages = packages
    if 'products' in kwargs:
      raise Exception('Use create_with_products constructor to use products')
    if confirmed:
      sender_address, has_fullfilment, dispatch, service, receiver = kwargs.get('sender_address'),kwargs.get('has_fullfilment'),kwargs.get('dispatch'),kwargs.get('service'),kwargs.get('receiver')
      if not all([sender_address, dispatch, service, receiver]):
        raise Exception('You need to set all of the following params: sender_address, has_fullfilment, dispatch, service, receiver')
      picking.confirm(sender_address, has_fullfilment, dispatch, service, receiver, post_office=kwargs.get('post_office',False))
    else:
      picking._post_picking(post_office=kwargs.get('post_office',False))
    return picking
  

  def confirm(self, sender_address, has_fullfilment, dispatch, service, receiver, post_office=False):
    self.sender_address, self.has_fullfilment, self.dispatch, self.service, self.receiver = sender_address, has_fullfilment, dispatch, service, receiver
    self._post_picking(post_office)

  def _post_picking(self,post_office=False):
    if self.mode == 'D':
      self.send_to_address()
    elif self.mode == 'S':
        self.send_to_post_office(post_office)
    else: 
      raise Exception(f'Unsupported mode {self.mode}')

    
  
  def _base_params(self):
    #TODO refactor this
    params = {
      'pedido':self.order.id,
      'confirmado':self.confirmed,
      'modalidad':self.mode
    }
    if self.confirmed:
      params.update({
        'destinatario':self.receiver or (f"{self.order.name} {self.order.last_name}"),
        'tiene_fulfillment':self.has_fullfilment,
        'despacho':self.dispatch,
        'servicio': self.service
      })
    if self.has_fullfilment and self.products:
      params.update({
        'productos':json.dumps(self.products)
      })
    else:
      params.update({
        'paquetes':json.dumps(self.packages)
      })
    if self.observations:
      params.update({
        'observaciones':self.observations
      })
    if self.uses_insurance:
      params.update({
        'usa_seguro':self.uses_insurance
      })
      
    return params


  def send_to_post_office(self, post_office):
    if not post_office:
        raise Exception('To use mode S you need to add post_office argument')
    params = self._base_params()
    params.update({
      'post_office':post_office
    })
    url = "{base_url}{base_path}".format(base_url=self.base_request_url, base_path=self.base_request_path)
    response = requests.post(url, params={'access_token':self.access_token},json=params)
    respjson = response.json()
    self.response = respjson
    if response.status_code == 200:
      return respjson
    else: raise Exception('La solicitud fallo por favor revise los parametros')

  def send_to_address(self):
    params = self._base_params()
    try:
      params.update({
      'direccion_envio': self.sender_address,
      'correo': self.carrier,
      'calle': self.street,
      'numero': self.st_number,
      'codigo_postal': self.zip_code,
      'provincia': self.state,
      'localidad': self.city
      })
    except:
      raise Exception('All of the next attributes must be set to send with mode "D" carrier, street, st_number, zip_code, state, city')

    if self.floor:
      params['piso'] = self.floor
    if self.floor:
      params['depto'] = self.apartment
    if self.floor:
      params['referencia_domicilio'] = self.address_reference
    
    url = "{base_url}{base_path}".format(base_url=self.base_request_url, base_path=self.base_request_path)
    response = requests.post(url, params={'access_token':self.auth.access_token},json=params)
    respjson = response.json()
    self.response = respjson
    if response.status_code == 200:
      return respjson
    else: raise Exception(f'La solicitud fallo por favor revise los parametros \n {respjson}')
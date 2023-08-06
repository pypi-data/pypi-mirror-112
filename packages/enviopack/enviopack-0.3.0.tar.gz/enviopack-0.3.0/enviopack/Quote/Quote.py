# -*- coding: utf-8 -*-
import requests
from enviopack import Enviopack
from enviopack.constants import BASE_API_URL
from typing import List 
from enviopack import Auth

class Quote(Enviopack):
  """
  
  """
  _name = "Quote orders"


  state:str 
  "ID Provincia: Deberá informarse el valor ID devuelto por el webservice de provincias. Los IDs de provincias están bajo el estándar ISO_3166-2:AR sin el prefijo AR-."
  city:int 
  "ID Localidad: Deberá informarse el valor ID devuelto por el webservice de localidades."
  zip_code:int
  "Codigo postal: Entero de 4 dígitos"
  weight:float
  "Peso: Hasta 2 dígitos decimales"
  packages:str
  """Este parámetro espera un formato especial el cual debe indicar las dimensiones de los N paquetes que pueda tener el envio a cotizar.
      Ej: 20x2x10,20x2x10 indica que se envian 2 paquetes y cada uno tiene 20 cm de alto x 2 cm de ancho x 10 cm de largo.
      En caso de no recibir valor alguno, nuestro sistema asume por default el envio de un unico paquete de 1 x 1 x 1."""
  carrier:int
  "correo: Deberá informarse el valor ID devuelto por el webservice de correos. Por ejemplo para FastMail su ID es fastmail."
  dispatch:str
  """despacho: Indica si el operador logistico debe retirar el paquete por el deposito del vendedor o si el vendedor lo va a acercar a una sucursal.
    Los valores posibles son:
    - D: retiro por domicilio
    - S: despacho desde sucursal"""
  mode:str
  """modalidad
  Los valores posibles son:
    - D: para envíos a domicilio
    - S: para envíos a sucursal
  """
  service:str
  """servicio Los valores posibles son:
    - N: para el servicio estándar
    - P: para el servicio prioritario
    - X: para el servicio express
    - R: para el servicio de devoluciones"""
  dispatch_address:int
  """direccion_envio ID que identifica la dirección, por donde el correo pasara a retirar la mercadería a enviar.
  Podes obtenerlo ingresando en Configuración / Mis Direcciones
  Si bien este parámetro no es obligatorio es conveniente enviarlo, pues de esta manera la cotización sera más precisa.
  En caso de no recibir valor alguno, nuestro sistema asume que el envío se realizará desde la dirección de envio default. Si no existiera una dirección de envio default no sera posible devolver cotizaciones y el WS no informara resultados."""
  column_order:str
  """orden_columna: Los valores posibles son:
    - valor: para ordenar por precio (Default)
    - horas_entrega: para ordenar por velocidad de envío
    - cumplimiento: para ordenar por porcentaje de cumplimiento en envios de similares caracteristicas
    - anomalos: para ordenar por porcentaje de anómalos en envios de similares caracteristicas"""
  order_way:str
  """orden_sentido Los valores posibles son:
    - asc: para orden ascendente (Default)
    - desc: para orden descendente"""


  def __init__(self, state:str, zip_code:int, weight:float, auth:Auth, base_url=BASE_API_URL, base_path='/cotizar', **kwargs):
    """
    city:int=False
    packages:str=False
    carrier:int=False
    dispatch:str=False
    mode:str=False
    service:str=False
    dispatch_address:int=False
    column_order:str=False
    order_way:str=False

    """
    super(self,Quote).__init__(auth)
    self.state = state 
    self.zip_code = zip_code 
    self.weight = weight 
    for arg in kwargs:
      value =  kwargs.get(arg, False)
      if value:
        setattr(self, arg, value)
    self.base_request_url = base_url
    self.base_request_path = base_path

  def __repr__(self):
    return '(Quote: weight {weight}, state {state}, zip_code {zip_code})'.format(weight=self.weight,state=self.state, zip_code=self.zip_code)

  def quote_cost(self) -> dict:
    """
    GET /cotizar/costo
    Obtener el costo que abona el vendedor por el envío 
    Permite obtener un listado de cotizaciones brindando en cada una de ellas el valor que vendedor va a pagar por el envío:
    """
    url = "{base_url}{base_path}{endpoint}".format(base_url=self.base_request_url, base_path=self.base_request_path, endpoint="/costo")
    access_token = self.auth.access_token
    if not access_token:
      raise Exception('No access token defined')

    mandatory_params = {
      'access_token':access_token,
      'provincia':self.state,
      'codigo_postal': self.zip_code,
      'peso':self.weight
    }
    params = self._optional_params(mandatory_params, optional_fields={
      "packages":"packages",
      "carrier":"correo",
      "dispatch":"despacho",
      "mode":"modalidad",
      "service":"servicio",
      "dispatch_address":"direccion_envio",
      "column_order":"orden_columna",
      "order_way":"orden_sentido",
      })
    response = requests.get(url, params)
    if response.status_code == 200:
      return response.json()
    else:
      raise Exception('El pedido de costo fallo, revisar los parametros utilizados')
    
  def quote_price_to_address(self):
    """
      GET /cotizar/precio/a-domicilio
      Permite obtener un listado de cotizaciones brindando en cada una de ellas el valor que comprador va a pagar por el envío a domicilio.
      Los valores devueltos por este webservice pueden ser modificados desde la sección correos y tarifas para cada servicio en particular.
    """
    raise NotImplementedError

  def quote_price_to_post_office(self):
    """
      GET /cotizar/precio/a-sucursal
      Permite obtener un listado de cotizaciones brindando en cada una de ellas el valor que el comprador va a pagar por un envío a sucursal, retornando ademas toda la información de cada sucursal elegible.
      Este webservice esta diseñado para que tu comprador en el checkout de tu aplicación pueda cotizar y elegir en tiempo real en que sucursal quiere recibir su pedido.
      Los valores devueltos por este webservice pueden ser modificados desde la sección correos y tarifas para cada correo en particular.
    """
    raise NotImplementedError
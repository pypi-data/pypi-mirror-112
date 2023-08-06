# -*- coding: utf-8 -*-
"""
Base class for enviopack integration, common features for all modules
"""
from enviopack.constants import BASE_API_URL
# from enviopack import Auth

class Enviopack:
  _name = "Abstract class which contains url and other integration methods"

  
  base_request_url:str = BASE_API_URL
  base_request_path:str = '/'

  def __init__(self, auth, base_url=BASE_API_URL, base_path=None,  **kwargs):
    self.auth = auth
    for arg,value in kwargs.items():
      if value:
        setattr(self, arg, value)
    self.base_request_url = base_url
    if base_path:
      self.base_request_path = base_path

  def _set_attributes_from_response(self, vals:dict, mapping:dict):
    """
    @vals dict which contains the values with the response params as keys
    @mapping dict that contains the keys from the response that correspond to the object
    """
    for key,value in vals.items():
      object_key = mapping.get(key,False)
      if object_key:
        setattr(self, object_key, value)

  def _optional_params(self, mandatory_params:dict, optional_fields:dict) -> dict:
    """
    Update the params dict copied from mandatory_params by getting the attributes specified in optional_fields from the object.

    @mandatory_params is a dict which contains the field in the api as key, and its value.
    @optional_fields dict with the attribute as key and the param name for the api as value
    """
    params = mandatory_params.copy()
    for field in optional_fields:
      attr = getattr(self, field,False)
      if attr:
        params.update({
          optional_fields.get(field):attr
        })
    return params
# -*- coding: utf-8 -*-
"""
Auth Class to generate authentification to Envio Pack.

This will hold an access token and refresh token.
"""
import requests 
from enviopack import Enviopack
from enviopack.constants import BASE_API_URL
from datetime import datetime, timedelta

class Auth(Enviopack):
  _name = 'Authentication to Enviopack'

  api_key:str
  secret_key:str
  access_token:str 
  refresh_token:str
  token_datetime_due:datetime

  def __init__(self, access_token=False, refresh_token=False, api_key=False, secret_key=False, token_datetime_due=datetime.now()+timedelta(hours=4), base_url=BASE_API_URL, base_path='/auth'):
    self.api_key = api_key
    self.secret_key = secret_key
    self.base_request_url = base_url
    self.base_request_path = base_path
    self.access_token = access_token
    self.refresh_token = refresh_token
    self.token_datetime_due = token_datetime_due
  
  @classmethod
  def with_token(cls, access_token, refresh_token, token_datetime_due=datetime.now()+timedelta(hours=4)):
    return cls(access_token=access_token, refresh_token=refresh_token, token_datetime_due=token_datetime_due)
  
  @classmethod
  def with_api_key(cls, api_key, secret_key):
    auth = cls(api_key=api_key, secret_key=secret_key)
    auth._generate_auth_request()
    return auth

  def __repr__(self):
    access_token = self.access_token
    if access_token and datetime.now() < self.token_datetime_due:
      return 'Authenticated: Valid until {due_date}, Api {api_key}'.format(due_date=self.token_datetime_due, api_key=self.api_key)
    else:
      return 'Unauthenticated'

  def _generate_auth_request(self):
    uri = '{base_url}{base_path}'.format(base_url=self.base_request_url,base_path=self.base_request_path) 
    request = requests.post(url=uri, data={'api-key':self.api_key, 'secret-key':self.secret_key}, headers={'content-type':'application/x-www-form-urlencoded'} )
    if request.status_code == 200:
      jsonresponse:dict = request.json()
      if 'token' in jsonresponse and 'refresh_token' in jsonresponse:
        self.access_token = jsonresponse.get('token',False)
        self.refresh_token = jsonresponse.get('refresh_token',False)
        return request    
      else:
        raise Exception('token or refresh token missing on response, check the api docs and the data added as parameters')
    else:
      raise Exception('Request failed, please try again later and check the data introduced')



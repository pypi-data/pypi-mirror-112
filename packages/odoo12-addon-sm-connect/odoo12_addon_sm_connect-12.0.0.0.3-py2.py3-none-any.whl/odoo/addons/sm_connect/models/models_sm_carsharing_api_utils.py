# -*- coding: utf-8 -*-
import requests
import json

from odoo.addons.sm_connect.models.credential_loader import credential_loader

class sm_carsharing_api_utils(object):

  __instance = None
  __cs_url = None
  __apikey = None
  __admin_group = None

  @staticmethod
  def get_instance():
    if sm_carsharing_api_utils.__instance is None:
      sm_carsharing_api_utils()

    return sm_carsharing_api_utils.__instance

  def __init__(self):
    if sm_carsharing_api_utils.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      sm_carsharing_api_utils.__instance = self
      credentials_load = credential_loader.get_instance()
      api_credentials = credentials_load.get_carsharing_api_credentials()
      sm_carsharing_api_utils.__cs_url = api_credentials["cs_url"]
      sm_carsharing_api_utils.__apikey = api_credentials["apiKey"]
      sm_carsharing_api_utils.__admin_group = api_credentials["admin_group"]

  def get_endpoint_base(self,limit = ""):
    return self.__cs_url + "/api/admin/v1/" + self.__admin_group + "/" + limit

  def get_headers_base(self):
    return {'Content-type': 'application/json','apiKey': self.__apikey}

  def get_reservations(self,from_q=False,till_q=False):
    if from_q and till_q:
      return requests.get(
        self.get_endpoint_base("reservations"),
        params={'from': from_q,'till': till_q, 'group': 'sommobilitat'},
        headers=self.get_headers_base())
    return False

  def post_persons_send_registration_email(self,person_id=False,person_lang=False):
    if person_id and person_lang:
      endpoint = self.get_endpoint_base("persons")+ "/" + person_id + "/sendRegistrationEmail"
      return requests.post(endpoint, data=json.dumps({'language': 'ca'}), headers=self.get_headers_base())
    return False

  def get_persons(self,person_id=False):
    if person_id:
      return requests.get( self.get_endpoint_base("persons")+ "/" + person_id, headers=self.get_headers_base())
    return False

  def post_persons(self,data=False):
    if data:
      return requests.post(self.get_endpoint_base("persons"), data=json.dumps(data), headers=self.get_headers_base())
    return False

  def post_persons_groups(self,person_id=False,group_id=False,ba_id=False,create_ba=False):
    if person_id and group_id and create_ba:
      r_data = {"role":"user"}
      if ba_id:
        r_data['billingAccount'] = ba_id
      endpoint = self.get_endpoint_base("persons")+ "/" + person_id + "/groups/"+ group_id+"?createBillingAccount="+create_ba
      r = requests.post(endpoint,data=json.dumps(r_data), headers=self.get_headers_base())
      return r
    return False

  def delete_person_group(self, person_id=False, group_id=False):
    if person_id and group_id:
      endpoint = self.get_endpoint_base("persons")+ "/" + person_id + "/groups/"+ group_id
      response = requests.delete(endpoint, headers=self.get_headers_base())
      return response
    return False

  def put_billingaccount_transactions(self,ba_id=False,ttype=False,description=False,amount=False):
    if ba_id and ttype and description and amount:
      endpoint = self.get_endpoint_base("billingAccounts")+ "/" + ba_id + "/transactions"
      r_data = {
        "type": ttype,
        "description": description,
        "internalDescription": description,
        "amount": amount
      }
      return requests.put(endpoint, data=json.dumps(r_data), headers=self.get_headers_base())
    return False

  def validate_response(self,response=False):
    if response:
      if response.status_code != 200:
        return False
      return response.json()
    return False

  # def get_reservations_by_group(self,groupid=False,from_q=False,to_q=False):
  #   if groupid and from_q and to_q:
  #     return requests.get
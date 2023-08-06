# -*- coding: utf-8 -*-

import firebase_admin
from firebase_admin import auth as fire_auth, credentials, db
from odoo.addons.sm_connect.models.credential_loader import credential_loader

class sm_carsharing_db_utils(object):
  __instance = None
  __cred = None
  __sm_carsharing_app = None

  @staticmethod
  def get_instance():
    if sm_carsharing_db_utils.__instance is None:
      sm_carsharing_db_utils()

    token_info = sm_carsharing_db_utils.__cred.get_access_token()
    cred_info = sm_carsharing_db_utils.__cred.get_credential()

    token_is_expired = cred_info.expired

    if token_is_expired:
      firebase_admin.delete_app(app=sm_carsharing_db_utils.__sm_carsharing_app)

      credentials_load = credential_loader.get_instance()
      credentials_fire_priv = credentials_load.get_firebase_priv_auth_credentials()

      sm_carsharing_db_utils.__cred = credentials.Certificate(credentials_fire_priv)

      sm_carsharing_db_utils.__sm_carsharing_app = firebase_admin.initialize_app(sm_carsharing_db_utils.__cred, {
        'databaseURL': credentials_load.get_firebase_db_ref()
      })

    return sm_carsharing_db_utils.__instance

  def __init__(self):
    if sm_carsharing_db_utils.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      sm_carsharing_db_utils.__instance = self

    credentials_load = credential_loader.get_instance()
    credentials_fire_priv = credentials_load.get_firebase_priv_auth_credentials()

    sm_carsharing_db_utils.__cred = credentials.Certificate(credentials_fire_priv)

    sm_carsharing_db_utils.__sm_carsharing_app = firebase_admin.initialize_app(sm_carsharing_db_utils.__cred, {
      'databaseURL': credentials_load.get_firebase_db_ref()
    })

  def firebase_get(self, endpoint, key=False):
    if key:
      query = db.reference(path=endpoint).child(path=key)
    else:
      query = db.reference(path=endpoint)
    result = query.get()
    return result

  def firebase_put(self, endpoint, key, data):
    ref = db.reference(path=endpoint)
    key_child = ref.child(path=key)
    key_child.set(data)

  def firebase_update(self, endpoint, key, data):
    ref = db.reference(path=endpoint)
    key_child = ref.child(path=key)
    key_child.update(data)

  def delete_user_from_auth(self, uid=False):
    if uid:
      try:
        fire_auth.delete_user(uid, app=self.__sm_carsharing_app)
      except Exception:
        return False
      return True

    return False

  def get_uid_from_email(self, email):
    try:
      firebase_user_info = fire_auth.get_user_by_email(email, app=self.__sm_carsharing_app)
      return firebase_user_info.uid
    except:
      return False
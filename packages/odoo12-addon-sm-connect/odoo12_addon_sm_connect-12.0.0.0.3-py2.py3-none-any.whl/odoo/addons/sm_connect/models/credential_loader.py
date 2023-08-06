# -*- coding: utf-8 -*-

import json
import os


class credential_loader(object):
  __instance = None

  @staticmethod
  def get_instance():
    if credential_loader.__instance is None:
      credential_loader()
    return credential_loader.__instance

  def __init__(self):
    if credential_loader.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      credential_loader.__instance = self

  def get_carsharing_api_credentials(self):
    return {
      "apiKey": os.getenv('SM_CARSHARING_API_CREDENTIALS_API_KEY'),
      "cs_url": os.getenv('SM_CARSHARING_API_CREDENTIALS_CS_URL'),
      "admin_group": os.getenv('SM_CARSHARING_API_CREDENTIALS_ADMIN_GROUP')
    }

  def get_wordpress_db_credentials(self):
    return {
      "admin_data": {
        "host": os.getenv('SM_WORDPRESS_DB_CREDENTIALS_ADMIN_HOST'),
        "username": os.getenv('SM_WORDPRESS_DB_CREDENTIALS_ADMIN_USERNAME'),
        "password": os.getenv('SM_WORDPRESS_DB_CREDENTIALS_ADMIN_PASSWORD'),
      },
      "db_data": {
        "host": os.getenv('SM_WORDPRESS_DB_CREDENTIALS_DB_HOST'),
        "user": os.getenv('SM_WORDPRESS_DB_CREDENTIALS_DB_USER'),
        "password": os.getenv('SM_WORDPRESS_DB_CREDENTIALS_DB_PASSWORD'),
        "database": os.getenv('SM_WORDPRESS_DB_CREDENTIALS_DB_DATABASE'),
      }
    }
  def get_firebase_priv_auth_credentials(self):
    return {
      "type": os.getenv('SM_FIREBASE_AUTH_TYPE'),
      "project_id": os.getenv('SM_FIREBASE_AUTH_PROJECT_ID'),
      "private_key_id": os.getenv('SM_FIREBASE_AUTH_PRIVATE_KEY_ID'),
      "private_key": os.getenv('SM_FIREBASE_AUTH_PRIVATE_KEY').replace('\\n','\n'),
      "client_email": os.getenv('SM_FIREBASE_AUTH_CLIENT_EMAIL'),
      "client_id": os.getenv('SM_FIREBASE_AUTH_CLIENT_ID'),
      "auth_uri": os.getenv('SM_FIREBASE_AUTH_AUTH_URI'),
      "token_uri": os.getenv('SM_FIREBASE_AUTH_TOKEN_URI'),
      "auth_provider_x509_cert_url": os.getenv('SM_FIREBASE_AUTH_PROVIDER_X509'),
      "client_x509_cert_url": os.getenv('SM_FIREBASE_AUTH_CLIENT_X509'),
    }

  def get_firebase_db_ref(self):
    return os.getenv('SM_FIREBASE_DB_REF')

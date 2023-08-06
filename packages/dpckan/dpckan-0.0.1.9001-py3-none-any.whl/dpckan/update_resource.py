import urllib
import json
import pprint
import os
import requests
import json
import collections
import sys
import click
from ckanapi import RemoteCKAN
from dpckan.functions import (os_slash, buscaListaDadosAbertos, buscaDataSet,
                              buscaPastaArquivos, removePastaArquivos,
                              buscaArquivos, atualizaMeta, load_complete_datapackage,
                              resource_update, update_datapackage_json_resource, resource_create,
                              resources_metadata_create)

@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br")  # -H para respeitar convenção de -h ser help
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json')
@click.option('--resource-name', '-n', required=True,
              help="Nome do recurso a ser incluído. Chave 'name' do recurso dentro do arquivo datapackage.json")
@click.option('--resource-id', '-id', required=True,
              help="Id do recurso a ser incluído.")
def update_resource(ckan_host, ckan_key, datapackage, resource_name, resource_id):
  """
  Summary line.

  Extended description of function.

  Parameters
  ----------
  arg1 : int
      Description of arg1
  arg2 : str
      Description of arg2

  Returns
  -------
  int
      Description of return value

  """
  package = load_complete_datapackage(datapackage)
  # Show package to find datapackage.json resource id
  # Update datapakcage.json resource
  update_datapackage_json_resource(ckan_host, ckan_key, package.name)
  # Create new resource
  print(f"Atualizando recurso: {resource_name}")
  resource_update(ckan_host,
                  ckan_key,
                  resource_id,
                  package.get_resource(resource_name))
  resources_metadata_create(ckan_host,
                            ckan_key,
                            resource_id,
                            package.get_resource(resource_name))

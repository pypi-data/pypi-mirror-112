import urllib
import os
import requests
import json
import click
from dpckan.validations import run_validations
from dpckan.functions import (os_slash, datapackage_path, frictionless_to_ckan_dictionary,
                              delete_dataset, lerCaminhoRelativo, dataset_create,
                              is_dataset_alread_published)

@click.command()
@click.option('--ckan-host', '-H', envvar='CKAN_HOST', required=True,
              help="Ckan host, exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br")  # -H para respeitar convenção de -h ser help
@click.option('--ckan-key', '-k', envvar='CKAN_KEY', required=True,
              help="Ckan key autorizando o usuário a realizar publicações/atualizações em datasets")
@click.option('--datapackage', '-dp', required=True, default='datapackage.json')
def create(ckan_host, ckan_key, datapackage):
  """
  Função responsável pela publicação/atualização de um conjunto de dados no ambiente (host) desejado.

  Por padrão, função buscará host e key da instância CKAN para qual e deseja publicar/atualizar dataset
  nas variáveis de ambiente CKAN_HOST e CKAN_KEY cadastradas na máquina ou em arquivo .env na raiz do dataset.

  Parameters
  ----------
  host: string (não obrigatório caso variável CKAN_HOST esteja cadastrada na máquina ou em arquivo .env)
    host ou ambiente da instância CKAN para a qual se deseja publicar/atualizar dataset.
    Exemplo: http://dados.mg.gov.br ou https://dados.mg.gov.br
  key: string (não obrigatório caso variável CKAN_KEY esteja cadastrada na máquina ou em arquivo .env)
    Chave CKAN do usuário e ambiente para a qual se deseja publicar/atualizar dataset

  Returns
  -------
    Dataset publicado/atualizado no ambiente desejado
  """
  run_validations(ckan_host, ckan_key)
  dataset_dict = json.loads(frictionless_to_ckan_dictionary(datapackage))
  published_dataset = is_dataset_alread_published(ckan_host, dataset_dict['name'])
  if published_dataset:
    # Deleting dataset if it exists
    delete_dataset(ckan_host, ckan_key, dataset_dict['name'])
  dataset_create(ckan_host, ckan_key)
  

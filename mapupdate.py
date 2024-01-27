#!/usr/bin/env python3
import requests
import json
import logging

# Configurando o nível de log para debug
logging.basicConfig(level=logging.DEBUG)

# URL da API do Zabbix
url = 'http://zabbix.wgo.com.br/zabbix/api_jsonrpc.php'

# Cabeçalhos da requisição
headers = {
    'Content-Type': 'application/json'
}

# Token de autenticação
auth_token = '7fe375b90c85cffadd8ff18d6b7d40e91e9c82ab42a35be759cb9737281d8236'

# Função para verificar se o host possui um item com o nome "syslog"
def verificar_chave_syslog(host_id):
    # Dados da requisição para obter os itens do host
    item_request_data = {
        'jsonrpc': '2.0',
        'method': 'item.get',
        'params': {
            'output': 'extend',
            'hostids': host_id,
            'search': {
                'name': 'syslog'
            }
        },
        'auth': auth_token,
        'id': 1
    }

    # Envio da requisição para obter os itens do host
    item_response = requests.post(url, headers=headers, data=json.dumps(item_request_data))

    # Verificação da resposta para obter os itens do host
    if item_response.status_code == 200:
        item_result = item_response.json()

        # Verificação se a resposta contém os dados dos itens
        if 'result' in item_result and len(item_result['result']) > 0:
            item_id = item_result['result'][0]['itemid']
            print(f"Chave encontrada: {item_id}")
            return item_id
        else:
            print("Chave não encontrada")
    else:
        print(f"Erro na requisição de itens do host: {item_response.status_code}")
    
    return None

# Função para atualizar os elementos do mapa
def atualizar_elementos_do_mapa(sysmap_id, elementos):
    # Dados da requisição para atualizar os elementos do mapa
    update_request_data = {
        'jsonrpc': '2.0',
        'method': 'map.update',
        'params': {
            'sysmapid': sysmap_id,
            'selements': elementos
        },
        'auth': auth_token,
        'id': 1
    }

    # Envio da requisição para atualizar os elementos do mapa
    update_response = requests.post(url, headers=headers, data=json.dumps(update_request_data))

    # Verificação da resposta para atualizar os elementos do mapa
    if update_response.status_code == 200:
        update_result = update_response.json()

        # Verificação se a resposta contém o resultado da atualização
        if 'result' in update_result and update_result['result']['sysmapids']:
            print("Elementos atualizados com sucesso")
        else:
            print("Falha ao atualizar elementos do mapa")
    else:
        print(f"Erro na requisição de atualização de elementos do mapa: {update_response.status_code}")

# Dados da requisição para obter os mapas
map_request_data = {
    'jsonrpc': '2.0',
    'method': 'map.get',
    'params': {
        'output': 'extend',
        'selectSelements': 'extend',
        'selectLinks': 'extend',
        'selectUsers': 'extend',
        'selectUserGroups': 'extend',
        'selectShapes': 'extend',
        'selectLines': 'extend'
    },
    'auth': auth_token,
    'id': 1
}

# Envio da requisição para obter os mapas
map_response = requests.post(url, headers=headers, data=json.dumps(map_request_data))

# Log da requisição de mapas
logging.debug(f'Map Request URL: {url}')
logging.debug(f'Map Request Headers: {headers}')
logging.debug(f'Map Request Body: {json.dumps(map_request_data)}')

# Verificação da resposta para obter os mapas
if map_response.status_code == 200:
    map_result = map_response.json()

    # Log da resposta de mapas
    logging.debug(f'Map Response Code: {map_response.status_code}')
    logging.debug(f'Map Response Body: {map_result}')

    # Verificação se a resposta contém os dados dos mapas
    if 'result' in map_result:
        maps = map_result['result']

        # Iterar sobre cada mapa
        for map_data in maps:
            # Imprimir informações do mapa
            print(f"ID do mapa: {map_data['sysmapid']}")
            print(f"Nome do mapa: {map_data['name']}")
            print()

            # Verificação se o mapa possui elementos
            if 'selements' in map_data:
                elements = map_data['selements']

                # Iterar sobre cada elemento
                for element in elements:
                    # Imprimir informações do elemento
                    print(f"ID do elemento: {element['selementid']}")
                    print(f"Nome do elemento: {element['label']}")
                    
                    # Verificação se o tipo do elemento é 0 (host)
                    if element['elementtype'] == '0':
                        print(f"ID do host: {element['elements'][0]['hostid']}")
                        
                        # Verificar se o host possui um item com o nome "syslog"
                        item_id = verificar_chave_syslog(element['elements'][0]['hostid'])
                        
                        if item_id:
                            # Verificar se o elemento já possui uma URL syslog
                            if 'urls' in element and any(url.get('name') == 'SYSLOG' for url in element['urls']):
                                print("URL syslog já existe. Nenhuma ação necessária.")
                            else:
                                # Adicionar a URL syslog aos URLs do elemento
                                element.setdefault('urls', []).append({
                                    'name': 'SYSLOG',
                                    'url': f"history.php?action=showvalues&itemids%5B%5D={item_id}"
                                })
                                
                                print(f"URL syslog adicionada: {element['urls'][-1]['url']}")
                    
                    print(f"Tipo do elemento: {element['elementtype']}")
                    print()
                    
                # Atualizar os elementos do mapa
                atualizar_elementos_do_mapa(map_data['sysmapid'], elements)
                
            else:
                print("Nenhum elemento encontrado para este mapa.")
    else:
        print("Nenhum dado de mapa encontrado.")
else:
    print(f"Erro na requisição de mapas: {map_response.status_code}")


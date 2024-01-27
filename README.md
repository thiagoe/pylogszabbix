#

#  PyLogsZabbix

Bem-vindo ao repositório do Atualizador de Mapas Zabbix! 🚀

## Descrição

Este repositório contém um script em Python que permite atualizar elementos em mapas do Zabbix automaticamente. Se você está cansado de atualizar manualmente os mapas no seu sistema de monitoramento Zabbix, este script está aqui para salvar o dia!

![Map](https://github.com/thiagoe/pylogszabbix/assets/18621801/d839c765-0070-4bd8-94c6-b379779d3644)

![logs](https://github.com/thiagoe/pylogszabbix/assets/18621801/a59d3783-6eae-4e7b-aad2-36d072ec9c64)

## Integração Rsyslog-Zabbix
Este projeto demonstra uma integração entre o rsyslog, Zabbix e Python. Ele foi criado para capturar mensagens syslog usando o rsyslog, identificar o endereço IP do host de origem, obter o nome do host do Zabbix e, em seguida, enviar a mensagem de log para um item do Zabbix.
Um segundo Script faz a integraçao da URLs de logs nos mapas para facilitar os uso.

## Pré-requisitos
Antes de usar esta integração, certifique-se de que o seguinte esteja configurado:
Rsyslog: Configure o rsyslog para capturar mensagens syslog e encaminhá-las para o script Python.
Servidor Zabbix: Certifique-se de que o Zabbix esteja configurado e que os hosts tenham IP e nomes corretos.
Pacotes Python: Instale os pacotes Python necessários usando o seguinte comando:

> pip install pyzabbix

## Configuração
Ajuste as variáveis de configuração nos scripts Python para corresponder ao seu ambiente. Configurações importantes incluem:

URL do Servidor Zabbix, Nome de Usuário e Senha: Configure essas variáveis em envio.py.

Configuração do Rsyslog: Configure o rsyslog para encaminhar logs para o script Python. Você pode usar a configuração rsyslog fornecida em rsyslog.conf.

## Uso
Execute log.py: Execute log.py para começar a capturar mensagens syslog.

> python log.py

Configure o rsyslog: Certifique-se de que o rsyslog esteja configurado para encaminhar logs para o script Python.

Execute envio.py: Execute envio.py para enviar uma mensagem de log de exemplo para o Zabbix.


> python envio.py

## Atualização Mapas
## Recursos

- Obtém todos os mapas da sua instância do Zabbix.
- Verifica se há elementos do tipo host em cada mapa.
- Atualiza os elementos do host com uma URL de Syslog com base na existência de um item de syslog.
- Registra o processo e os resultados para sua conveniência.

## Como Funciona

1. O script se conecta à API do Zabbix para obter todos os mapas.
2. Para cada mapa, verifica se há elementos do tipo host.
3. Se forem encontrados elementos do host, verifica se há um item de syslog associado ao host.
4. Se um item de syslog existir, atualiza o elemento com a URL de Syslog.
5. O script registra o processo e os resultados, para que você possa acompanhar as atualizações.

## Primeiros Passos

Para começar com o Atualizador de Mapas Zabbix, siga estas etapas:

1. Clone este repositório em sua máquina local.
2. Instale as dependências necessárias executando `pip install -r requirements.txt`.
3. Atualize as variáveis `url`, `headers` e `auth_token` no script para corresponder à configuração da sua API do Zabbix.
4. Execute o script usando `python final.py`.
5. Relaxe e deixe o script atualizar seus mapas do Zabbix automaticamente.

Por favor, observe que você precisa ter o Python instalado em sua máquina e acesso a uma instância do Zabbix com a API habilitada.

## Configuração

Você pode personalizar o comportamento do script modificando as seguintes variáveis no script:

- `LOG_FILE`: O caminho para o arquivo de log onde o script irá escrever os registros.
- `LOG_LEVEL`: O nível de log para controlar a verbosidade dos registros. Você pode escolher entre `logging.CRITICAL`, `logging.ERROR`, `logging.WARNING`, `logging.INFO` ou `logging.DEBUG`.

Sinta-se à vontade para explorar o script e fazer as modificações necessárias para atender aos seus requisitos específicos.

## Contribuições

Contribuições para o Atualizador de Mapas Zabbix são bem-vindas! Se você tiver ideias, melhorias ou correções de bugs, sinta-se à vontade para enviar uma solicitação de pull. Juntos, podemos tornar o script ainda melhor.

## Licença

Este repositório está licenciado sob a Licença MIT. Você pode encontrar mais informações no arquivo [LICENSE](LICENSE).

## Aviso Legal

Este script é fornecido "como está" sem qualquer garantia. Por favor, use-o de forma responsável e certifique-se de ter backups adequados e procedimentos de teste antes de fazer qualquer atualização nos seus mapas do Zabbix.

Feliz monitoramento com o Atualizador de Mapas Zabbix! 🌟

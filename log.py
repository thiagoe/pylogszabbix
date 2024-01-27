#!/usr/bin/env python3
import sys
import logging
import re
import subprocess
from pyzabbix import ZabbixAPI

ZABBIX_API_URL = "http://192.168.22.233/zabbix/api_jsonrpc.php"
ZABBIX_UNAME = "Admin"
ZABBIX_PWORD = "Esfp$$#1040"
LOG_FILE = "/log/teste.log"
CACHE = {}

def initialize_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def get_host_name_by_ip(ip):
    global CACHE

    if ip in CACHE:
        return CACHE[ip]

    zabbix = ZabbixAPI(ZABBIX_API_URL)
    zabbix.login(ZABBIX_UNAME, ZABBIX_PWORD)

    host = zabbix.host.get(filter={"ip": ip}, selectInterfaces=["interfaceid", "ip", "dns", "hostid"])

    if host:
        hostname = host[0]['host']
        CACHE[ip] = hostname
        return hostname

    return None

def send_log_to_zabbix(hostname, log_message):
    zabbix_server = '192.168.22.233'
    item_key = 'syslog'

    command = [
        'zabbix_sender',
        '-z', zabbix_server,
        '-s', hostname,
        '-k', item_key,
        '-o', log_message
    ]

    try:
        subprocess.run(command, check=True)
        logging.info("Mensagem enviada com sucesso para o Zabbix.")
    except subprocess.CalledProcessError as e:
        logging.error("Erro ao enviar mensagem para o Zabbix: %s", e)

def process_message(message):
    regex = r'\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]'
    match = re.search(regex, message)
    if match:
        ip = match.group(1)
        hostname = get_host_name_by_ip(ip)
        if hostname:
            send_log_to_zabbix(hostname, message)
        else:
            logging.warning("Hostname não encontrado para o IP: %s", ip)

def on_init():
    initialize_logging()
    logging.debug("on_init called")

def on_exit():
    logging.debug("on_exit called")

def main():
    on_init()
    print("OK", flush=True)

    try:
        for line in sys.stdin:
            line = line.rstrip('\n')
            process_message(line)
            print("OK", flush=True)
    except Exception as e:
        logging.exception("Unrecoverable error, exiting program")

    on_exit()

if __name__ == "__main__":
    main()


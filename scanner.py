#!/usr/bin/python3
import sys
import time
import socket
import threading
from colorama import Fore, Style
BANNER_SCAN = f"""{Fore.BLUE}
 __  ___  __   ______        ______        _______ .__    __   __
|  |/  / |  | |   _  \      /  __  \      /       ||  |  |  | |  |
|  '  /  |  | |  |_)  |    |  |  |  |    |   (----`|  |__|  | |  |
|    <   |  | |      /     |  |  |  |     \   \    |   __   | |  |
|  .  \  |  | |  |\  \----.|  `--'  | .----)   |   |  |  |  | |  |
|__|\__\ |__| | _| `._____| \______/  |_______/    |__|  |__| |__|


{Style.RESET_ALL}"""

def port(ip, porta):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex((ip, porta))
        sock.close()
        return resultado == 0
    except Exception as e:
        print(f"{Fore.RED}Erro ao verificar porta {porta}: {e}{Style.RESET_ALL}")
        return False


def id(ip, porta):
    try:
        servico = socket.getservbyport(porta)
        banner = b''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((ip, porta))
            sock.send(b'GET / HTTP/1.0\r\n\r\n')
            banner = sock.recv(1024)
        return servico, banner.decode('utf-8').splitlines()[0]
    except Exception as e:
        print(f"{Fore.RED}Erro ao identificar serviço na porta {porta}: {e}{Style.RESET_ALL}")
        return "Desconhecido", ""

#anim
def anim():
    while True:
        for char in '/-\|':
            sys.stdout.write('\r' + f'Escaneando... {char}')
            sys.stdout.flush()
            time.sleep(0.1)

#Main func
def main():
    print(BANNER_SCAN)
    ip = input("Digite o endereço IP do alvo: ")

    animation_thread = threading.Thread(target=anim)
    animation_thread.daemon = True
    animation_thread.start()

    portas_comuns = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389]
    print(f"\n{Fore.CYAN}Escaneando portas...{Style.RESET_ALL}")
    for porta in portas_comuns:
        if port(ip, porta):
            servico, banner = id(ip, porta)
            print(f"{Fore.GREEN}Porta {porta} aberta: {servico} - {banner}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Porta {porta} fechada{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

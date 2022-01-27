from stem.control import Controller
from stem import Signal
from fake_useragent import UserAgent
import requests
from time import sleep

def renew_connection():

    ua=UserAgent()
    headers={"User-Agent":ua.random}
    proxies={
            "http":"socks5://127.0.0.1:9050",
            "https":"socks5://127.0.0.1:9050"
            }

    old_ip=requests.get("http://icanhazip.com",proxies=proxies,headers=headers).text

    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="mypasswordblablabla")
        controller.signal(Signal.NEWNYM)
        controller.close()

    new_ip=old_ip
    while new_ip==old_ip:
        sleep(0.05)
        new_ip=requests.get("http://icanhazip.com",proxies=proxies,headers=headers).text

    print("Your IP address {} is changed -> {}".format(old_ip,new_ip))

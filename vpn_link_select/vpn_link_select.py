#!/usr/bin/env python3
from datetime import datetime
from time import sleep
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def blankfunc(msg):
    pass
syslogging = blankfunc

loggerTag="VPN_LINK_SELECT"

hub1="HK1901"
link1="hk1901"
hub2="hkt"
link2="hkt"
password="KA3jRSrKeFE"
server="172.30.2.1"
port=5555
pingTimes=10
domain1="hk2.geoe.cn"
domain2="hkt.geoe.cn"

def GetSoftetherApiHeader(hub: str, hub_password: str) -> dict:
    return {
        "X-VPNADMIN-HUBNAME" : hub,
        "X-VPNADMIN-PASSWORD" : hub_password
    }

def GetOnline(hub: str, hub_password: str, link: str) -> bool:
    url = f"https://{server}:{port}/api/GetLink"
    parameters = {
        "HubName_Ex_str" : hub,
        "AccountName_utf" : link
    }
    resp = requests.get(url, params=parameters, headers = GetSoftetherApiHeader(hub, hub_password), verify=False)
    if resp.status_code == requests.codes.ok:
        resp_json = resp.json()
        return resp_json["result"]["Online_bool"]
    return False

def SetOnline(hub: str, hub_password: str, link: str) -> bool:
    url = f"https://{server}:{port}/api/SetLinkOnline"
    parameters = {
        "HubName_str" : hub,
        "AccountName_utf" : link
    }
    resp = requests.get(url, params=parameters, headers = GetSoftetherApiHeader(hub, hub_password), verify=False)
    if resp.status_code == requests.codes.ok:
        resp_json = resp.json()
        if resp_json["result"] == parameters:
            return GetOnline(hub, hub_password, link)
    return False

def SetOffline(hub: str, hub_password: str, link: str) -> bool:
    url = f"https://{server}:{port}/api/SetLinkOffline"
    parameters = {
        "HubName_str" : hub,
        "AccountName_utf" : link
    }
    resp = requests.get(url, params=parameters, headers = GetSoftetherApiHeader(hub, hub_password), verify=False)
    if resp.status_code == requests.codes.ok:
        resp_json = resp.json()
        if resp_json["result"] == parameters:
            return not GetOnline(hub, hub_password, link)
    return False

def InitLogging():
    global syslogging
    from sys import platform
    if platform == "linux" or platform == "linux2":
        import syslog
        syslog.openlog(loggerTag, syslog.LOG_PID, syslog.LOG_USER)
        syslogging = syslog.syslog

def Logging(msg: str) -> None:
    print(msg)
    syslogging(msg)


if __name__ == "__main__":
    InitLogging()
    now = datetime.now()
    operation = ''
    if 2 <= now.hour <= 19:
        if GetOnline(hub1, password, link1):
            operation = 'Keep'
        else:
            operation = 'Change'
        Logging(f"Current Time is {now}, {operation} to Link 1 [{domain1}].")
        SetOnline(hub1, password, link1)
        sleep(1)
        SetOffline(hub2, password, link2)
    else:
        if GetOnline(hub2, password, link2):
            operation = 'Keep'
        else:
            operation = 'Change'
        Logging(f"Current Time is {now}, {operation} to Link 2 [{domain2}].")
        SetOnline(hub2, password, link2)
        sleep(1)
        SetOffline(hub1, password, link1)


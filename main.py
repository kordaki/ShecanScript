from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString

resolvconf_file = '/etc/resolv.conf'
mock = """<span class="shecan-dns-ips" onclick="copyToClipboard(this)" onmouseenter="outFunc()" style="line-height: 1.5;">178.22.122.100</span><span class="shecan-dns-ips" onclick="copyToClipboard(this)" onmouseenter="outFunc()" style="line-height: 1.5;">185.51.200.2</span>"""

def getDnsFromElement(dnsBox):
    dnsList=[]
    for item in dnsBox:
        dnsList.append(item.get_text())
    return dnsList

def getSource(isMock):   
    if isMock:
        # For Develop Mode
        print("from mock")
        data = mock
    else:
        print("from web")
        webUrl = urlopen('https://shecan.ir/')
        data = webUrl.read()
    soup = BeautifulSoup(data, 'html.parser')
    dnsBox = soup.findAll('span', attrs={ 'class': 'shecan-dns-ips'})
    dnsList = getDnsFromElement(dnsBox)
    return dnsList

def updateResolver(dnsList):
    resolvconf = open(resolvconf_file, 'w') 
    outputList = []
    for dns in dnsList:
        outputList.append('nameserver ' + str(dns) + '\n')
    print(outputList)
    resolvconf.writelines(outputList) 
    resolvconf.close() 


if __name__ == "__main__":
    dnsList = getSource(False)
    updateResolver(dnsList)

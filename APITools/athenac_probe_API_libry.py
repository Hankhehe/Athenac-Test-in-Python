from APITools.DataModels.datamodel_apidata import HostAgentClientInfo
import requests,json,time
from requests_toolbelt.adapters.source import SourceAddressAdapter

class AthenacProbeAPILibry:
    def __init__(self,probeIP:str,nicip:str) -> None:
        self.probeIP = probeIP
        self.APIsource = requests.Session()
        self.APIsource.mount('http://',SourceAddressAdapter(nicip))
        self.APIsource.mount('https://',SourceAddressAdapter(nicip))
        self.APIsource.trust_env=False
    
    def SendInfoToProbeByAPI(self,data:HostAgentClientInfo)->None:
        path = '/api/HostAgent/ReportStatus'
        Header = {'Content-type': 'application/json'}
        self.APIsource.post(self.probeIP+path,headers=Header,data=json.dumps(data.__dict__),verify=False)
        
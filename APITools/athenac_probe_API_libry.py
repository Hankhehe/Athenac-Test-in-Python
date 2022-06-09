from APITools.DataModels.datamodel_apidata import HostAgentClientInfo
import requests,json,time

class AthenacProbeAPILibry:
    def __init__(self,probeIP:str) -> None:
        self.probeIP = probeIP
    
    def SendInfoToProbeByAPI(self,data:HostAgentClientInfo)->None:
        path = '/api/HostAgent/ReportStatus'
        Header = {'Content-type': 'application/json'}
        requests.post(self.probeIP+path,headers=Header,data=json.dumps(data.__dict__),verify=False)
        
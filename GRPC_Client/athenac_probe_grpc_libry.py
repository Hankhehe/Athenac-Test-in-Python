import grpc,datetime
from GRPC_Client.agent_host_info import agent_host_info_pb2
from GRPC_Client.agent_host_info import agent_host_info_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

class Athenac_Probe_GRPC_libry:
    def __init__(self,probeIP:str,nicIP:str) -> None:
        self.channel_options = [('grpc.local_bind_address', nicIP)]
        self.ProbeIP = probeIP

    def SendHostInfo(self,Hotstinfo:agent_host_info_pb2.HostReportRequest):
        stub = agent_host_info_pb2_grpc.HostAgentServiceStub(grpc.insecure_channel(f'{self.ProbeIP}:18002',options=self.channel_options))
        stub.SendHostReport(Hotstinfo)

    def Create_HostInfo(self,macs:list,DomainName:str,OSType:str,OS_Display_name:str,MotherBoard_Num:str = ''
                        ,Hostname:str='TestMachine',Logon_Users:list[dict]=[]
                        ,Share_Folder:list = [],Pending_Hotfix:list=[]
                        ,Local_Admin_Account:list[str]=[],Softwares:list[dict] = [], OS_Product :str =''
                        ,OS_Build:str = '', OS_Version:str =''
                        ) -> agent_host_info_pb2.HostReportRequest:
        Date_to_timestamp = Timestamp()
        Date_to_timestamp.FromDatetime(datetime.datetime(year = 1970, month = 1, day = 1, hour = 0, minute = 0, second = 0, microsecond = 0))
        Hostinfo_Sample = agent_host_info_pb2.HostReportRequest(
            host_name= Hostname,
            MACs=macs,
            domain_name= DomainName,
            logon_users=Logon_Users,
            #ex = [{'logon_account':'Local/Hank','remote_login':True,'gpo_result':''}]
            os_type= OSType,
            os_product= OS_Product,
            share_folder=Share_Folder,
            pending_hot_fix=Pending_Hotfix,
            # ex = ['Hotfix 123456 - KB123456','Hotfix 666666 - KB666666']
            windows_hot_fix_last_check_time=Date_to_timestamp,
            local_admin_account=Local_Admin_Account,
            timestamp=Date_to_timestamp,
            motherboard_serial_number=MotherBoard_Num,
            softwares=Softwares, 
            # ex = [{"DisplayName": "Hank_Program_hehe","DisplayVersion": "7.8.8.10","Publisher": "HankMaster","InstallDate": "20230101","EstimatedSize":"888"}]
            os_display_product = OS_Display_name,
            os_build = OS_Build,
            os_version = OS_Version
        )

        return Hostinfo_Sample



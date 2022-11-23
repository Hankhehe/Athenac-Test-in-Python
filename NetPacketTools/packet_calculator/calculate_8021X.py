from scapy.all import rdpcap,wrpcap,RadiusAttr_Message_Authenticator
import hashlib,hmac

class Calculate8021X():

    def CalculateHashFromPacket(self,pcapfilepath:str,RespounseIdx:int,RequestIdx:int,secrectkey:bytes):
        '''計算 Radius Challeng 和 accept 的 message-auth 和 authencatitor'''
        
        #使用前一包 Request 的 Authenticator 並將 Message Authenticator 變 0 計算
        #先 Hash 出 message-auth 後值填進去後再把 authencatitor 的值 Hash 出來
        radiuspacketpayload = rdpcap(pcapfilepath)[RespounseIdx-1]['Radius']
        radiuspacketpayload.authenticator = rdpcap(pcapfilepath)[RequestIdx-1]['Radius'].authenticator
        if RadiusAttr_Message_Authenticator in radiuspacketpayload :
            radiuspacketpayload['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
            radiuspacketpayload['RadiusAttr_Message_Authenticator'].value = bytes.fromhex(hmac.new(secrectkey,bytes(radiuspacketpayload),hashlib.md5).hexdigest())
            print('Message-Authen : ' +radiuspacketpayload['RadiusAttr_Message_Authenticator'].value.hex())
        print('authenticator : '+hashlib.md5(bytes(radiuspacketpayload)+secrectkey).hexdigest())

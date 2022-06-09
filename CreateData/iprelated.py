import ipaddress,re

def CreateIPDataByCIDROrPrifix(cidr:str) -> list:
    '''Create Data of range IP in IPv4 or IPv6'''
    cidr = ipaddress.ip_interface(cidr).network  # type: ignore
    return list(ipaddress.ip_network(cidr))

def ConvertIPv6ShortToIPv6Full(ipv6:str) -> str:
      iplist = ipv6.split('::')
      ipaddr = ['0000'] * 8
      preip = iplist[0].split(':')
      idx = 0
      for i in preip :
         ipaddr[idx] = i.zfill(4)
         idx += 1
      if len(iplist) == 2 :
         postip = iplist[1].split(':')
         idx = -1
         for i in postip[::-1] :
               ipaddr[idx] = i.zfill(4)
               idx -= 1
      return ':'.join(ipaddr)

def ConvertIPv6FulltoIPv6Short(ipv6:str) -> str:
   ipv6list = []
   for x in ipv6.split(':'):
      if x == '0000' or x == '0' :
         ipv6list.append('0')
      else :
         ipv6list.append(x.lstrip('0'))
   first, second = 0,0
   for i in range(len(ipv6list)-1) :
      if first == second and (ipv6list[i+1] != '0' or ipv6list[i] != '0'):
         continue
      elif first == second and (ipv6list[i] == '0' or ipv6list[i+1] == '0'):
         first, second = i ,i+1
      elif ipv6list[i] == '0':
         second +=1
      else: break
   if second == (len(ipv6list)-1) and ipv6list[-1] == '0':
      second +=1
   if first != second:
      a,b,c = ipv6list[0:first],ipv6list[first:second],ipv6list[second:]
      ret = ':'.join(a)+'::'+':'.join(c)
   else:
      ret = ':'.join(ipv6list)
   return ret

def GetMultcastInfoFromIPv6(ipv6:str) -> dict:
   ipv6full = ConvertIPv6ShortToIPv6Full(ipv6=ipv6)
   ipv6short = ConvertIPv6FulltoIPv6Short(ipv6=ipv6)
   dMACformulti = ':'.join( re.findall(r'.{2}','3333ff'+ ipv6full[-7:].replace(':','')))
   dipformulti = 'ff02::1:ff'+ipv6full[-7:]
   return {'IPv6full':ipv6full,'IPv6short':ipv6short,'TagetMAC':dMACformulti,'TagetIP':dipformulti}



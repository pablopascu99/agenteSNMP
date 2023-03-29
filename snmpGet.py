from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api

def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    print('cbFun is called')
    while wholeMsg:
        print('loop...')
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
            )
        print('Notification message from %s:%s: ' % (
            transportDomain, transportAddress
            )
        )
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                print('Enterprise: %s' % (
                    pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                    )
                )
                print('Agent Address: %s' % (
                    pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                    )
                )
                print('Generic Trap: %s' % (
                    pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                    )
                )
                print('Specific Trap: %s' % (
                    pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                    )
                )
                print('Uptime: %s' % (
                    pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                    )
                )
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
                print(varBinds)
            else:
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)
                print(varBinds)
            # print('Var-binds:')
            # for oid, val in varBinds:
            #     print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
    return wholeMsg

transportDispatcher = AsynsockDispatcher()

transportDispatcher.registerRecvCbFun(cbFun)

# UDP/IPv4
transportDispatcher.registerTransport(
    # CUIDADO!! Pongo puerto 163 porque en mi entorno local tengo en uso el 162
    udp.domainName, udp.UdpSocketTransport().openServerMode(('localhost', 163))
)

# UDP/IPv6
transportDispatcher.registerTransport(
    # CUIDADO!! Pongo puerto 163 porque en mi entorno local tengo en uso el 162
    udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::1', 163))
)

transportDispatcher.jobStarted(1)

try:
    # Dispatcher will never finish as job#1 never reaches zero
    print('run dispatcher')
    transportDispatcher.runDispatcher()
except:
    transportDispatcher.closeDispatcher()
    raise

##################################################################################################################################################
#                                                                                                                                                #
#  Ejemplo para prueba con snmptrapGen:                                                                                                          #
#  snmptrapGen -v:1 -c:public -r:127.0.0.1 -to:1.3.6.1.2.1.6.13 -eo:1.3.6.1.4.1.8072.3.2.10 -vid:1.3.6.1.2.1.6.13.1.1 -vtp:str -val:"1" -p:163   #
#                                                                                                                                                #
##################################################################################################################################################
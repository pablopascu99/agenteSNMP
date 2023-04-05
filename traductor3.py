# https://www.yaklin.ca/2022/01/14/compiling-mibs-for-pysnmp.html
# https://pysnmp.readthedocs.io/en/latest/faq/pass-custom-mib-to-manager.html

from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd

iterator = getCmd(
    SnmpEngine(),
    CommunityData('public'),
    UdpTransportTarget(('127.0.0.1', 162)),
    ContextData(),
    ObjectType(ObjectIdentity(
        'IF-MIB', 'ifInOctets', 1
        ).addAsn1MibSource(
            'file://.'
        )
    )
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)

elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))

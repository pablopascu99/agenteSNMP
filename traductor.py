from pysnmp.smi import view

# Carga el MIB correspondiente
mibViewController = view.MibViewController("./RFC1213-MIB.mib")
print(mibViewController)
# Define el OID a traducir
oid = '1.3.6.1.2.1.6.13.1.1'

# Traduce el OID a nombre de objeto
name, label, suffix = mibViewController.getNodeName(oid)
print('Nombre de objeto: %s' % name)

# También puedes traducir un nombre de objeto a OID
name = 'snmpTrapOID'
oid, label, suffix = mibViewController.getNodeLocation(name)
print('OID: %s' % oid)

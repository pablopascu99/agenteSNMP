#!/usr/bin/python3
from pysnmp.smi import builder, view, compiler, rfc1902
from pysnmp.debug import Debug, setLogger
from pysmi import debug as pysmi_debug

# Assemble MIB browser
mibBuilder = builder.MibBuilder()

#compiler.addMibCompiler(mibBuilder, sources=['file:///home/josedu/Local_Proyectos/pruebas/mibs'])
# MIBDIR = '/home/josedu/Local_Proyectos/pruebas/mibs/compiled'
#mibSources = mibBuilder.getMibSources() + (builder.DirMibSource(MIBDIR),)
#mibBuilder.setMibSources(*mibSources)

# SI NO FUNCIONA DESCOMENTAR. AQUI SE VE LA RUTA QUE COGE LOS MIBs
# pysmi_debug.setLogger(pysmi_debug.Debug('compiler'))


# compiler.addMibCompiler(mibBuilder, sources = ['file:///home/josedu/Local_Proyectos/pruebas/mibs/compiled', ])
compiler.addMibCompiler(mibBuilder)
mibViewController = view.MibViewController(mibBuilder)

#setLogger(Debug('all'))

# Pre-load MIB modules we expect to work with
#mibBuilder.loadModules('SNMPv2-MIB')
mibBuilder.loadModules('IF-MIB')
#, 'SNMP-COMMUNITY-MIB','IF-MIB','SNMPv2-SMI','SNMPv2-TC','SNMPv2-CONF','IANAifType-MIB')


#modName = mibViewController.getFirstModuleName()


#def doit(*poargs):
#    print(rfc1902.ObjectIdentity(*poargs).resolveWithMib(mibViewController).getMibSymbol())

# This is what we can get in TRAP PDU
varBinds = [
    ('1.3.6.1.6.3.1.1.4.1.0', '1.3.6.1.6.3.1.1.5.1',),
    ('1.3.6.1.6.3.1.1.4.1.0', '1.3.6.1.6.3.1.1.5.2',),
    ('1.3.6.1.6.3.1.1.4.1.1', '1.3.6.1.6.3.1.1.5.3',),
    ('1.3.6.1.6.3.1.1.4.1.0', '1.3.6.1.6.3.1.1.5.4',),
    ('1.3.6.1.6.3.1.1.4.1.1', '1.3.6.1.6.3.1.1.5.5',),
]

# Run var-binds through MIB resolver
# You may want to catch and ignore resolution errors here
varBinds = [rfc1902.ObjectType(rfc1902.ObjectIdentity(x[0]), x[1]).resolveWithMib(mibViewController)
            for x in varBinds]

#for x in varBinds:
#    print (rfc1902.ObjectIdentity(x[0]).resolveWithMib(mibViewController).getMibSymbol())
#doit('.1.3.6.1.6.3.1.1.5.3')
#doit('.1.3.6.1.6.3.1.1.5.4')

for varBind in varBinds:
    print(varBind.prettyPrint())

from pysnmp.smi import builder, view, compiler, rfc1902
# from pysnmp.debug import Debug, setLogger
# from pysmi import debug as pysmi_debug
from datetime import datetime
import time

# Assemble MIB browser
mibBuilder = builder.MibBuilder()

# SI NO FUNCIONA DESCOMENTAR. AQUI SE VE LA RUTA QUE COGE LOS MIBs
# pysmi_debug.setLogger(pysmi_debug.Debug('compiler'))

compiler.addMibCompiler(mibBuilder)
mibViewController = view.MibViewController(mibBuilder)

# Pre-load MIB modules we expect to work with
mibBuilder.loadModules('IF-MIB')

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
resolvedVarBinds = []
for x in varBinds:
    resolvedVarBind = rfc1902.ObjectType(rfc1902.ObjectIdentity(x[0]), x[1]).resolveWithMib(mibViewController)
    resolvedVarBinds.append(resolvedVarBind)

# Add timestamp to each varBind
varBindsWithTimestamp = []
for varBind in resolvedVarBinds:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    varBindWithTimestamp = (varBind[0].prettyPrint(),varBind[1].prettyPrint(), timestamp)
    print(varBindWithTimestamp)
    varBindsWithTimestamp.append(varBindWithTimestamp)
    time.sleep(2)

# Print varBinds with timestamps
# for varBind, timestamp in varBindsWithTimestamp:
#     print(f"{timestamp} - {varBind.prettyPrint()}")
# for i in varBindsWithTimestamp:
#     print(i)
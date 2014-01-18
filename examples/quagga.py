#!/usr/bin/python

"Create a network consisting of Quagga routers"

import inspect, os, atexit
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI

from collections import namedtuple

LegacyRouter = namedtuple("LegacyRouter", "name ip")
net = None

class QuaggaTopo( Topo ):
    "Quagga topology example."

    def __init__( self ):

        # Initialize topology
        Topo.__init__( self )

        # Directory where this file / script is located
        scriptdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

        # Baseline configs
        quaggaBaseConfigPath=scriptdir + '/quaggacfgs/'
        quaggaBaseRunPath='/run/quagga-'
        quaggaBaseLogPath='/var/log/quagga-'

        # Prep list of legacyRouterConfigs
        legacyRouterConfigs = []
        legacyRouterConfigs.append(LegacyRouter(name = 'a1', ip = '172.0.0.1/16'))
        legacyRouterConfigs.append(LegacyRouter(name = 'b1', ip = '172.0.0.11/16'))
        legacyRouterConfigs.append(LegacyRouter(name = 'c1', ip = '172.0.0.21/16'))
        legacyRouterConfigs.append(LegacyRouter(name = 'c2', ip = '172.0.0.22/16'))
        legacyRouterConfigs.append(LegacyRouter(name = 'd1', ip = '172.0.0.31/16'))
        legacyRouterConfigs.append(LegacyRouter(name = 'rs', ip = '172.0.254.254/16'))

        # Add legacy switch
        ixpfabric = self.addLegacySwitch( 'ixpfabric' )

        # Setup each legacy router, add a link between it and the IXP fabric
        for legacyRouterConfig in legacyRouterConfigs:
            routerName = legacyRouterConfig.name
            routerIP = legacyRouterConfig.ip
            legacyRouter = self.addLegacyRouter( routerName,
                                                 quaggaConfigPath=quaggaBaseConfigPath+routerName,
                                                 quaggaRunPath=quaggaBaseRunPath+routerName,
                                                 quaggaLogPath=quaggaBaseLogPath+routerName,
                                                 ip=routerIP,
                                                 checkPerms=True,
                                                 fixPerms=True,
                                                 createDirsIfNeeded=True,
                                                 manageServices=True )
            self.addLink( legacyRouter, ixpfabric )

def startNetwork():
    info( '** Creating Quagga network\n' )
    topo = QuaggaTopo()
    global net
    net = Mininet(topo, controller=None )
    net.start()

    info( '** Dumping host connections\n' )
    dumpNodeConnections(net.legacyRouters)

    info( '** Testing network connectivity\n' )
    net.ping(net.legacyRouters)

    info( '** Collecting BGP neighbors\n' )
    for router in net.legacyRouters:
        quagga_cmd = "show ip bgp summary"
        result = router.cmd('vtysh -c \"%s\"' % quagga_cmd)
        info("*** %s:\n%s" % (router, result))

    info( '** Running CLI\n' )
    CLI( net )

def stopNetwork():
    if net is not None:
        info( '** Tearing down Quagga network\n' )
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
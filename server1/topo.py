from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class CustomTopology(Topo):
    """
    Topology for left part
    h1(ping) - s1 - r1
    """
    def build(self):
        "Create custom topo"

        # Add host, router, switch
        host1Ping = self.addHost("h_1")
        switch1 = self.addSwitch("s_1")
        router1 = self.addHost("r_1", cls=LinuxRouter)

        # Add links
        self.addLink(host1Ping, switch1)
        self.addLink(switch1,
                    router1,
                    intfName2='r1-eth1')



def run():
    topo = Topo1()
    net = Mininet(topo=topo)

    net.start()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()



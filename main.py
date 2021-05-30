import argparse
import os
import sys

from mininet.net import Mininet
from mininet.cli import CLI
from utils import get_topology, create_tunnel, create_session
from mininet.net import Intf

FRR_BIN_DIR = "/usr/lib/frr"
DAEMONS = ["zebra", "staticd", "bgpd"]


def start_daemon(node, daemon, conf_file):
    """Start one FRR daemon on a given node.

    """
    node.cmd("{bin_dir}/{daemon}"
             " -f {conf_file}"
             " -d"
             " -i /tmp/{node_name}-{daemon}.pid"
             " > /tmp/{node_name}-{daemon}.out 2>&1"
             .format(bin_dir=FRR_BIN_DIR,
                     daemon=daemon,
                     conf_file=conf_file,
                     node_name=node.name))
    node.waitOutput()


def clean():
    """Clean all state left over from a previous experiment.

    """
    os.system("rm -f /tmp/R*.log /tmp/R*.pid /tmp/R*.out")
    os.system("rm -f /tmp/h*.log /tmp/h*.pid /tmp/h*.out")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 {} > /dev/null 2>&1"
              .format(' '.join(os.listdir(FRR_BIN_DIR))))


def run(topology, topology_name, daemons):
    """Start a network experiment.

    """

    # Clean up any state from previous experiments.
    clean()
    root_dir = os.path.dirname(sys.modules['__main__'].__file__)

    # Start Mininet.
    net = Mininet(topo=topology())

    # TODO: add ip to comand line arguments
    create_tunnel('10.10.240.22', '10.10.244.65', 1000)
    for node_name in topology.TUNNELS.keys():
        for int_name in topology.TUNNELS[node_name]:
            create_session(int_name)
            Intf(int_name, node=net.getNodeByName(node_name))

    net.start()

    for node in net.hosts:
        for daemon in daemons:
            conf_file = os.path.join(root_dir, topology_name, 'conf', daemon, f'{node.name}.conf')
            if os.path.exists(conf_file):
                start_daemon(node, daemon, conf_file)

        if node.name.startswith('r'):
            # Enable IP forwarding
            node.cmd("sysctl -w net.ipv4.ip_forward=1")
            node.waitOutput()

    CLI(net)
    net.stop()
    if daemons:
        os.system("killall -9 {}".format(' '.join(daemons)))


def main():
    """Route 0 entry point.

    """

    parser = argparse.ArgumentParser(
        description='Launch an FRR network experiment in Mininet.')
    parser.add_argument('-t', '--topology', required=True,
                        help='the topology of the network')
    args = parser.parse_args()

    run(get_topology(args.topology), args.topology, DAEMONS)


if __name__ == "__main__":
    main()

# Adding support of node migration for multimode mininet setup with config

## Task:
1. Have at least 3 FRR routers in a cluster (2 routers on one server and one on another)<br/>
2. Verify connectivity between all routers<br/>
3. Do some runtime configuration on the routers. (IP, files, etc.)<br/>
4. Migrate one router from the server with two routers to another server.<br/>
5. Verify connectivity.<br/>
6. Do configuration in a way that 2 additional hosts won’t lose connectivity during node migration.<br/>


## Topology:
![Topology](other/adv-net-pr2.png?raw=true "Title")

## Plan:
1. **DONE** Create Basic Topology
2. **DONE** Create Server1 config and test it
3. **DONE** Create Server2 config and test it
4. Test connectivity between servers
5. Send running config from Server2 to Server1
6. Migrate R3
7. Write tests
8. Create presentation

## Bottlenecks:


## Todo:
* Write script that deletes autoconfigured links/IP's


## Other notes:

* There are two files topo1.py and topo2.py for two parts of topology

* To add internet to Mininet: `sudo dhclient eth1`

* Add l2tp tunnel: `sudo ip l2tp add tunnel tunnel_id 1000 peer_tunnel_id 1000 encap udp local <LOCAL_IP> remote <REMOTE_IP> udp_sport 60000 udp_dport 60000`
* Add session: `sudo ip l2tp add session name eth12 tunnel_id 1000 session_id 2000 peer_session_id 2000`

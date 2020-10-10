from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

#command: sudo mn --custom primera_parte.py --topo personalTopo

class MyTopo(Topo):
	#simple topology
	def __init__(self):
		#creating custom topo
		Topo.__init__(self)

		print("Introduce un numero para la variable fo:")
		fo = input()

		ts = self.addSwitch('TS', cls=OVSKernelSwitch, dpid='0000001')

		#creamos lo switches de tal manera que fo = switches
		for i in range(0, fo):
			new_switch = self.addSwitch('s' + str(i+1), cls=OVSKernelSwitch, dpid='000000'+str(i+1))

			#linkeamos el ts con los switches
			self.addLink(new_switch, ts)

			#creamos fo hosts por switch y linkeamos cada host al switch
			for j in range(0, fo):

				new_host = self.addHost('h_s'+str(i+1)+'_n'+str(j+1), cls=Host, ip='10.0.'+str(i+1)+'.'+str(j+1)+'/16')
				self.addLink(new_host, new_switch)
                                
topos = { 'personalTopo': (lambda : MyTopo())}






	


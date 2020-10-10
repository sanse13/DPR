from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log = core.getLogger()

class Controlador(object):
	def __init__(self, connection):
		self.connection = connection #establezco conexion
		connection.addListeners(self)
	
		self.dpid = connection.dpid
		ts_dpid = hex(0000001)

		if self.dpid == ts_dpid:
			for i in range(1, fo+1):
				msg = of.ofp_flow_mod()
				msg.match.dl_type = 0x800
				msg.match.nw_dst = '10.0.'+str(i)+'.0/16'
				#enviar paquete por todos los puertos menos por el que llego
				msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
				self.connection.send(msg)
		else:
			switch_dpid = hex(self.dpid)
			for i in range(1, fo+1):
				msg = of.ofp_flow_mod()
				msg.match.dl_type = 0x800
				msg.match.nw_dst = '10.0.'+str(s-1)+'.'+str(i)
				msg.actions.append(of.ofp_action_output(port = i+1))
				self.connection.send(msg)

def launch():
	def start_switch(event):
		log.debug("Controlling %s" % (event.connection))
		NewSwitch(event.connection)
	core.openflow.addListenerByName("ConnectionUp", start_switch)

				

		
		



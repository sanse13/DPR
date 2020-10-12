from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log = core.getLogger()

#el objetivo del controlador es establecer las tablas de los switches
#inicializamos con ./pox.py log.level --DEBUG misc.mi_controlador

def initialize(event):
		
	
	#obtenemos el dpid con la que la conexion se ha establecido
	dpid = event.dpid

	#obtengo el fo viendo el total de las conexiones que se han establecido
	fo = len(core.openflow.connections.values())-1 #el openflow nos indica el fo

	#vemos si el dpid es del padre o es del resto de switches, porque si estamos
	#en el padre, inundamos

	if dpidToStr(dpid) == '0000001':
			
		msg = of.ofp_flow_mod()
		msg.match.dl_type = ethernet.ARP_TYPE

		#como estamos en el padre, inundamos 
		msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
		event.connection.send(msg)
			
		for i in range(1, fo+1):
			msg = of.ofp_flow_mod()
			#activamos la tabla match
			msg.match.dl_type = 0x800
	
			msg.match.nw_dst = '10.0.'+str(i)+'.0/16'
			#enviar paquete por todos los puertos menos por el que llego

			msg.actions.append(of.ofp_action_output(port=i+1))
			msg.priority = 50
			event.connection.send(msg)
	else:

		#nos encontramos en los switches del segundo nivel			

		switch_dpid = dpidToStr(dpid)[6]
		for i in range(1, fo+1):
			msg = of.ofp_flow_mod()
			msg.match.dl_type = 0x800
			msg.match.nw_dst = '10.0.'+switch_dpid+'.'+str(i)
			msg.priority = 50
			msg.actions.append(of.ofp_action_output(port = i+1))
			event.connection.send(msg)

		#para cuando no encuentra el destino
			
		msg = of.ofp_flow_mod()
		msg.match.dl_type = 0x800
		msg.match.nw_dst = '10.0.0.0/16'
		msg.actions.append(of.ofp_action_output(port=1))
		msg.priority = 30
		event.connection.send(msg)

def launch():
	
	#lanzamos el controlador
	core.openflow.addListenerByName("ConnectionUp", initialize)

				

		
		


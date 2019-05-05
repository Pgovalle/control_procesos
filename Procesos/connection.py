from opcua import Client
from opcua import ua
from time import sleep


def GetConnection():
    client=Client("opc.tcp://192.168.1.23:4840/freeopcua/server/")
    try:
        client.connect()
        objectsNode = client.get_objects_node()
        print("conectando")
        u1 = objectsNode.get_child(['2:Proceso_Tanques','2:Valvulas','2:Valvula1','2:u'])
        u2 = objectsNode.get_child(['2:Proceso_Tanques','2:Valvulas','2:Valvula2','2:u'])
        g1 = objectsNode.get_child(['2:Proceso_Tanques','2:Razones','2:Razon1','2:gamma'])
        g2 = objectsNode.get_child(['2:Proceso_Tanques','2:Razones','2:Razon2','2:gamma'])
        t1 = objectsNode.get_child(['2:Proceso_Tanques','2:Tanques','2:Tanque1','2:h'])
        t2 = objectsNode.get_child(['2:Proceso_Tanques','2:Tanques','2:Tanque2','2:h'])
        t3 = objectsNode.get_child(['2:Proceso_Tanques','2:Tanques','2:Tanque3','2:h'])
        t4 = objectsNode.get_child(['2:Proceso_Tanques','2:Tanques','2:Tanque4','2:h'])
        print("CONECTADO")
        return dict(u1=u1,u2=u2,g1=g1,g2=g2,t1=t1,t2=t2,t3=t3,t4=t4)
        
    except:
        client.disconnect()
        print(2)
        return {}


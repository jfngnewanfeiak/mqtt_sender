from mqtt_interface_pub import MQTT_PUB
from socket import gethostname,gethostbyname
from definition_mqttmsg import RobotActionMsg
your_ip = gethostbyname(gethostname())

if __name__ == "__main__":
    pub = MQTT_PUB()
    pub.pub_con(broker_ip=your_ip,topic_name='req/move/robot',pubmsg="None")

    while True:
        num = int(input("type 0,1,2"))
        if num == 0:
            pub.pubmsg_setter(RobotActionMsg.ReqRobot0)
        elif num == 1:
            pub.pubmsg_setter(RobotActionMsg.ReqRobot1)
        elif num == 2:
            pub.pubmsg_setter(RobotActionMsg.ReqRobot2)
        else:
            break

        pub.pub_run()
    print('break')
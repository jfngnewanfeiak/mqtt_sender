from mqtt_interface_pub import MQTT_PUB
from mqtt_interface_sub import MQTT_SUB
from paho.mqtt import client as mqtt
flag = False # flag用
def sub_callback():
    if flag == False:
        print("aaa")
        flag = True
        


if __name__ == "__main__":
    # パブリッシャーの設定
    req_pub = MQTT_PUB()
    req_pub.pub_con(broker_ip="192.168.2.102", topic_name="req/turtle", pubmsg="aaa")

    # サブスクライバーの設定
    req_sub = MQTT_SUB()
    req_sub.sub_run(broker_ip="192.168.2.102", topic_name="req/manage", cb=sub_callback)
    while True:
        pass


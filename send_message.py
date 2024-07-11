from mqtt_interface_pub import MQTT_PUB
from mqtt_interface_sub import MQTT_SUB


if __name__ == "__main__":
    # パブリッシャーの設定
    req_pub = MQTT_PUB()
    req_pub.pub_con(broker_ip="10.77.96.1", topic_name="req/turtle", pubmsg="")

    # サブスクライバーの設定
    req_sub = MQTT_SUB()
    req_sub.sub_run(broker_ip="10.77.96.1", topic_name="req/manage")



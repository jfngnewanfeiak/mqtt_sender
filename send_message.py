from mqtt_interface_pub import MQTT_PUB
from mqtt_interface_sub import MQTT_SUB
from postgresql import POSTGRESQL
from time import sleep
from socket import gethostname,gethostbyname

# ip取得
your_ip = gethostbyname(gethostname())

# フラグ用のやつ
DB = POSTGRESQL()
DB.setting_connection(host='localhost',user='postgres',database='mytable')
DB.connect_DB()

def sub_callback(msg):
    # update文を書く
    DB.exec_update("UPDATE data_bridge SET value = 'True' where value='False'")
    print("callbackが走りました")
    # この後に、リクエストを
    print(msg)
    print('受け取ったmsg')
    aaa = msg.split('/')
    print(aaa[2])


if __name__ == "__main__":
    # パブリッシャーの設定
    req_pub = MQTT_PUB()
    req_pub.pub_con(broker_ip=your_ip, topic_name="req/turtle", pubmsg="aaa")

    # サブスクライバーの設定
    req_sub = MQTT_SUB()
    req_sub.sub_run(broker_ip=your_ip, topic_name="req/manage", cb=sub_callback)
    while True:
        select_data = DB.exec_select('select value from data_bridge')
        print(select_data)
        sleep(1)
        if select_data[0][0] == 'True':
            break
    
    print('処理抜けた')


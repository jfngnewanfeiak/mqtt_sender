#! /usr/bin/env python3
import rospy

from mqtt_interface_pub import MQTT_PUB
from mqtt_interface_sub import MQTT_SUB
from postgresql import POSTGRESQL
from robot_position_name import RobotPositionName
from time import sleep
from socket import gethostname,gethostbyname

status_callback_flag = True

# topic status_updateで使う
# cureent_positionを変更する、フラグ変数を変える役割
def status_callback(msg):
    print("status update")
    print(msg)
    msg = msg.split("/")
    global status_callback_flag
    b = f"update robot_status set current_position='{msg[1]}',isactive=false where id={msg[2]};"
    print(b)
    # split_msgの番号のやつでpositonとIDで切り替え
    # DB.exec_update(f"update robot_status set current_position={msg[1]},isactive=false where id='{msg[2]};'")
    DB.exec_update(b)
    status_callback_flag = False
# ip取得
your_ip = gethostbyname(gethostname())

# フラグ用のやつ、ロボットの状態のやつも
DB = POSTGRESQL()
DB.setting_connection(host='192.168.11.54',user='postgres',database='test')
DB.connect_DB()

robot_state_sub = MQTT_SUB()
robot_state_sub.sub_run(broker_ip='localhost',topic_name='status_update',cb=status_callback)

r0_mqtt = MQTT_PUB()
r1_mqtt = MQTT_PUB()
r2_mqtt = MQTT_PUB()
# robotとmqtt通信する方のプログラム
r0_mqtt.pub_con(broker_ip='localhost',topic_name='robot_sub0',pubmsg='None')
r1_mqtt.pub_con(broker_ip='localhost',topic_name='robot_sub1',pubmsg="None")
r2_mqtt.pub_con(broker_ip='localhost',topic_name='robot_sub2',pubmsg='None')



#  topic_name='req/move/robot',pubmsg="req/robot/1"
def sub_callback(msg):
    # update文を書く
    DB.exec_update("UPDATE data_bridge SET value = 'True' where value='False'")
    print("callbackが走りました")
    # この後に、リクエストを
    print(msg)
    print('受け取ったmsg')
    split_msg = msg.split('/')
    if msg == "req/robot/1":
        create_flow(msg=split_msg[2])

def create_flow(msg):
    # Robot_Statusは2次元配列を想定
    Robot_Status = DB.exec_select(f"select current_position from robot_status where id={msg};")

    move_list = []  # 動くロボットのidの順番を保存
    destination_list = []  # 目的地を保存,indexはmove_listより
    if Robot_Status[0][0] == RobotPositionName.warehouse0:
        # warehouse1とwarehouse2にロボットがいるかDBより確認
        # warehouse1とwarehouse2にいるロボットのidを返す
        temp=DB.exec_select("select id from robot_status where current_position='warehouse1' or current_position='warehouse2';")
        # warehouse2,1,0の順番でmove_listにappend
        pass
    elif Robot_Status[0][0] == RobotPositionName.warehouse1:
        # warehouse2にロボットがいるか確認
        temp=DB.exec_select("select id from robot_status where current_position='warehouse2';")
        # warehouse2,1の順にmove_listにappend
        if temp[0][0] == 0:
            move_list.append(temp[0][0])  # id = 0
            move_list.append(1)  # id = 1
        else:
            move_list.append(temp[0][0])
        pass
    else:
        move_list.append(msg)

    exec_move_robot(move_list)



# mqtt通信で各ロボットに行先を送信
def exec_move_robot(move_list):
    global status_callback_flag
    # mqttにて動かすロボットくりけす
    for i in range(len(move_list)):
        DB.exec_update(f"update robot_status set isactive=True where id={move_list[i]};")
        if move_list[i] == 0:
            if i == 0:
                r0_mqtt.pubmsg_setter("req/go/temp_posi")
            else:
                r0_mqtt.pubmsg_setter("req/go/destination")
            r0_mqtt.pub_run()
        elif move_list[i] == 1:
            if i == 0:
                r1_mqtt.pubmsg_setter("req/go/temp_posi")
            else:
                r1_mqtt.pubmsg_setter("req/go/destination")
            r1_mqtt.pub_run()
        else:
            pass
        while status_callback_flag:
            pass
        status_callback_flag = True

    
# DB    
def search_destination() -> list:
    a = [RobotPositionName.waitposition0,RobotPositionName.waitposition1,RobotPositionName.waitposition2]
    des_list = []
    # DBよりwaitpointにいるやつ検索する
    # select current_position from robot_status where current_position like 'waitposition%';
    robot_state = DB.exec_select("select current_position from robot_status where current_position like 'waitposition%';")
    # 
    y = 0
    for x in range(len(robot_state[0])):
        for i in range(y,len(robot_state[0])):
            if robot_state[0][x] != a[i]:
                des_list.append(a[i])
                y = i
                break
    return des_list
    

# MQTT && DB
def req_RobotState():
    # 流れ
    # MQTTよりロボットにリクエスト

    # リクエストで得た最新の位置情報を更新(DBに更新)
    DB.exec_update()
    pass




if __name__ == "__main__":
    # rospy.init_node("fnjeoaijefiopa",anonymous=True)
    # DB.exec_select()はlistで返ってきてその中身はタプル
    # DBの初期化
    DB.exec_update("update data_bridge set value='false';")
    DB.exec_update("update robot_status set isactive=false;")
    DB.exec_update("update robot_status set current_position='warehouse2' where id=0;")
    DB.exec_update("update robot_status set current_position='warehouse1' where id=1;")
    DB.exec_update("update robot_status set current_position='nnn' where id=2;")
    temp = DB.exec_select("select id from robot_status where current_position='warehouse2';")


    # パブリッシャーの設定
    # req_pub = MQTT_PUB()
    # req_pub.pub_con(broker_ip=your_ip, topic_name="req/turtle", pubmsg="aaa")

    # サブスクライバーの設定
    # req_sub = MQTT_SUB()
    # req_sub.sub_run(broker_ip=your_ip, topic_name="req/manage", cb=sub_callback)
    req_robot_sub = MQTT_SUB()
    req_robot_sub.sub_run(broker_ip='localhost', topic_name='req/move/robot', cb=sub_callback)
    req_robot_pub = MQTT_PUB()
    req_robot_pub.pub_con(broker_ip='localhost', topic_name='req/move/robot',pubmsg="req/robot/1")
    req_robot_pub.pub_run()
    while True:
        pass
    # rospy.spin()
    # while True:
    #     select_data = DB.exec_select('select value from data_bridge')
    #     print(select_data)
    #     sleep(1)


    # print('処理抜けた')


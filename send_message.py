from mqtt_interface_pub import MQTT_PUB
from mqtt_interface_sub import MQTT_SUB
from postgresql import POSTGRESQL
from robot_position_name import RobotPositionName
from time import sleep
from socket import gethostname,gethostbyname

# ip取得
your_ip = gethostbyname(gethostname())

# フラグ用のやつ、ロボットの状態のやつも
DB = POSTGRESQL()
DB.setting_connection(host='localhost',user='postgres',database='mytable')
DB.connect_DB()

r0_mqtt = MQTT_PUB()
r1_mqtt = MQTT_PUB()
r2_mqtt = MQTT_PUB()
# robotとmqtt通信する方のプログラム
r0_mqtt.pub_con(broker_ip='localhost',topic_name='robot_sub0',pubmsg='None')
r1_mqtt.pub_con(broker_ip='localhost',topic_name='robot_sub1',pubmsg="None")
r2_mqtt.pub_con(broker_ip='localhost',topic_name='robot_sub2',pubmsg='None')



def sub_callback(msg):
    # update文を書く
    DB.exec_update("UPDATE data_bridge SET value = 'True' where value='False'")
    print("callbackが走りました")
    # この後に、リクエストを
    print(msg)
    print('受け取ったmsg')
    split_msg = msg.split('/')
    if split_msg[0] == "ReqRobot":
        create_flow(msg=split_msg[2])

def create_flow(msg):
    split_msg = msg.split("/")
    # 最新のロボットの情報をDBにて更新
    req_RobotState()

    # Robot_Statusは2次元配列を想定
    Robot_Status = get_RobotState()
    move_list = [] # 動くロボットのidの順番を保存
    destination_list = [] # 目的地を保存,indexはmove_listより
    if Robot_Status[msg][2] == RobotPositionName.warehouse0:
        # warehouse1とwarehouse2にロボットがいるかDBより確認
        # warehouse1とwarehouse2にいるロボットのidを返す
        temp=DB.exec_select("select id from robot_status where current_position='waitposition0' or current_position='waitposition1';")
        # warehouse2,1,0の順番でmove_listにappend
        
        pass
    elif Robot_Status[msg][2] == RobotPositionName.warehouse1:
        # warehouse2にロボットがいるか確認
        DB.exec_select("select id from robot_status where current_position='waitposition1';")
        # warehouse2,1の順にmove_listにappend
        pass
    else:
        move_list.append(msg)
    
    destination_list = search_destination()


# mqtt通信で各ロボットに行先を送信
def exec_move_robot(move_list,destination_list):
    pass
    
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

# MQTT && DB
def get_RobotState():
    pass


if __name__ == "__main__":
    # パブリッシャーの設定
    req_pub = MQTT_PUB() 
    req_pub.pub_con(broker_ip=your_ip, topic_name="req/turtle", pubmsg="aaa")

    # サブスクライバーの設定
    req_sub = MQTT_SUB()
    req_sub.sub_run(broker_ip=your_ip, topic_name="req/manage", cb=sub_callback)
    req_robot_sub = MQTT_SUB()
    req_robot_sub.sub_run(broker_ip=your_ip,topic_name='req/move/robot',cb=sub_callback)
    while True:
        select_data = DB.exec_select('select value from data_bridge')
        print(select_data)
        sleep(1)
    
    
    print('処理抜けた')


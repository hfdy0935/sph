import random
import json
import os


# 已注册用户
users_path = os.path.dirname(__file__) + '\\..\\data\\users.json'
# 注册中用户
registering_path =  os.path.dirname(__file__) + '\\..\\data\\registering.json'


# 创建文件
def init():
    if not os.path.exists(users_path):
        with open(users_path, 'w', encoding = 'utf-8') as f:
            pass
    if not os.path.exists(registering_path):
        with open(registering_path, 'w', encoding = 'utf-8') as f:
            pass
# 获取注册中的用户列表
def get_registering_list() -> list:
    registering_list = []
    with open(registering_path, 'r', encoding = 'utf-8') as f:
        try:
            registering_list = json.load(f)
            registering_list = [] if registering_list == None else registering_list
        except:
            pass
    return registering_list
    
# 获取已注册的用户列表
def get_users_list() -> list:
    users_list = []
    with open(users_path, 'r', encoding = 'utf-8') as f:
        try:
            users_list = json.load(f)
            users_list = [] if users_list == None else users_list
        except:
            pass
    return users_list

# 写入注册中的用户列表
def write_registering_list(new_data: list):
    with open(registering_path, 'w', encoding = 'utf-8') as f:
        json.dump(new_data, f, ensure_ascii = False, indent = 2)

# 写入已注册用户列表
def write_users_list(new_data: list):
     with open(users_path, 'w', encoding = 'utf-8') as f:
        json.dump(new_data, f, ensure_ascii = False, indent = 2)

# 随机六位数验证码
def get_random_id_code():
    l = [random.randint(0, 9) for i in range(6)]
    return str(l).replace(',','').replace('[','').replace(']','').replace(' ','')
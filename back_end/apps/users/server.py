# cSpell:ignore fastapi, pydantic

from fastapi import APIRouter, Body
from pydantic import BaseModel
import random
import time

from .methods.function import (
    init,
    get_registering_list,
    get_users_list,
    write_registering_list,
    write_users_list,
    get_random_id_code
)


user = APIRouter(
    prefix = '/api/user', 
    tags = ['用户注册和登录部分']
)

    

@user.post('/register/reqIdCode/{time}')
def reqIdCode(tel = Body(..., description = '获取验证码请求')):
    init()
    # 后端用户列表
    old_users_list = get_users_list()
    # 后端注册中列表
    old_registering_list = get_registering_list()
    # 如果原文件有用户信息
    if old_users_list:
        for user in old_users_list:
            if user['tel'] == tel['tel']:
                return {'message': '该手机号已被注册'}
    if old_registering_list:
        for user in old_registering_list:
            if user['tel'] == tel['tel']:
                return {'message': '该手机号正在注册中，请稍后再试'}
    # 原来为空
    # 生成随机验证码
    id_code = get_random_id_code()
    # 把接收验证码这个用户写入注册中的列表
    write_registering_list(old_registering_list + [{'tel': tel['tel'], 'id_code': id_code}])
    time.sleep(random.randint(1,3))
    return {'message': 'OK', 'idCode': id_code}


class RegisterItem(BaseModel):
    tel: str
    idCode: str
    password: str
    registerTime: str


@user.post('/register/{time}')
def register(item: RegisterItem  = Body(..., description = '注册请求')):
    old_users_list = get_users_list()
    for user in old_users_list:
        if item.tel == user['tel']:
            return {'message': '该手机号已注册'}
    # 正常注册
    data = [{'tel': item.tel, 'password': item.password, 'registerTime': item.registerTime}]
    write_users_list(old_users_list + data)
    # 释放注册中列表中的这个用户
    registering_list = get_registering_list()
    for index,user1 in enumerate(registering_list):
        if user1['tel'] == item.tel:
            registering_list.pop(index)
            # 重新写入
            write_registering_list(registering_list)
    return {'message': '注册成功'}


class LoginItem(BaseModel):
    tel: str
    password: str


@user.post('/login/{time}')
def login(item: LoginItem = Body(..., description = '登录请求')):
    user_list = get_users_list()
    tel, pwd = item.tel, item.password
    print(tel, pwd)
    for i in user_list:
        if tel == i['tel'] and pwd == i['password']:
            return {'message': '登录成功'}
    return {'message': '登录失败'}
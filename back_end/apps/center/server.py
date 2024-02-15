# cSpell:ignore fastapi
from fastapi import APIRouter, Body
import json
import os

center = APIRouter(
    prefix = '/api/center',
    tags = ['个人中心']
)

base_path = os.path.dirname(__file__)
base_path = base_path.split('\\')
base_path = '\\'.join(base_path[:len(base_path) - 1]) + '\\trade\\data\\'

@center.post('/{time}')
def get_center_data(item = Body(...)):
    user_name = item['userName']
    record_path = base_path + user_name + '.json'
    print(record_path)
    if not os.path.exists(record_path):
        with open(record_path, 'w', encoding = 'utf-8') as f:
            pass
    original_data = []
    with open(record_path, 'r', encoding = 'utf-8') as f:
        try:
            original_data = json.load(f)
        except Exception as a:
            print(a)
    
        
    return {'message': 'OK', 'data': original_data}





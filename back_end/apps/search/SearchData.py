import random
import numpy as np
import os
import time


base_path = os.path.dirname(__file__)
def get_search_response( tmList, price_range, item ):
    '''
    接收参数：查询的品牌列表，价格范围，请求体
    '''
    lp,hp = int(price_range.split('-')[0]),int(price_range.split('-')[1])
    # 生成随机品牌
        
    tradeMarkList = [
        {'tmId':1, 'tmName':'华为', 'isImage':False},
        {'tmId':2, 'tmName':'苹果', 'isImage':False},
        {'tmId':3, 'tmName':'三星', 'isImage':False},
        {'tmId':4, 'tmName':'OPPO', 'isImage':False},
        {'tmId':5, 'tmName':'VIVO', 'isImage':False},
        {'tmId':6, 'tmName':'小米', 'isImage':False},
        {'tmId':7, 'tmName':'山寨机', 'isImage':False},
    ]
    for index,pic in enumerate(os.listdir(f'{base_path}/images/phones'), start = 8):
        pic_name = pic.split('.')[0]
        tradeMarkList.append({'tmId':index, 'tmUrl':f'http://127.0.0.1:8000/api/search/goodsBrandImage/{pic}', 'tmName':pic_name, 'isImage':True})
        
    attrsList = ([
            {
                "attrId": 1,
                "attrValueList": [
                    "500-999",
                    "1000-1999",
                    "2000-2999",
                    "3000-4999",
                    "5000-9999",
                    "10000-13999"
                ],
                "attrName": "价格"
            },
            {
                "attrId": 2,
                "attrValueList": [
                    "GSM（移动/联通2G）",
                    "电信2G",
                    "电信3G",
                    "移动3G",
                    "联通3G",
                    "联通4G"
                ],
                "attrName": "网制格式"
            },
            {
                "attrId": 3,
                "attrValueList": [
                    "4.0-4.9英寸",
                    "5.0-5.9英寸",
                    "6.0-6.9英寸"
                ],
                "attrName": "显示屏尺寸"
            },
            {
                "attrId": 4,
                "attrValueList": [
                    "800-999万",
                    "1000-1199万",
                    "1200-1399万",
                    "1400-1599万",
                    "1600-1799万"
                ],
                "attrName": "摄像头像素"
            },
            {
                "attrId": 5,
                "attrValueList": [
                    "特点",
                    "系统",
                    "内存",
                    "单卡双卡",
                    "其他"
                ],
                "attrName": "更多筛选项"
            },
        ])
    
    goodsList = []
    # 每种商品的种子
    seed_str = str(item.category1Id) + str(item.category2Id) + str(item.category3Id) + str(item.keyword) + str(item.props) + str(item.tradeMark)
    random.seed(seed_str)
    # 最后一页商品数量
    last_page_goods_num = random.randint(1,20)
    # 总商品数量
    total_goods_num = random.randint(100,15000)
    # 总页数
    total_pages_num = total_goods_num//20+1
    # 每页的种子
    seed_str1 = str(item.category1Id) + str(item.category2Id) + str(item.category3Id) + str(item.keyword) + str(item.props) + str(item.tradeMark) + str(item.pageNo)
    for i in range(1, last_page_goods_num if item.pageNo == total_pages_num else 21):
        # 每页每件商品的种子
        random.seed(seed_str1 + str(i))
        random_mobile = random.choice(tmList)
        random_price = random.randint(lp//100,hp//100)*100 + 99
        random_sales_num = int(random.randint(300,15000))
         
        goodsList.append(
        {
            "id": i,
            "defaultImg": f"http://127.0.0.1:8000/api/search/goodsImage/{item.pageNo}/{random.randint(1,42)}",
            "title": '山寨机清仓大甩卖' if '山寨机' in random_mobile else f"{random_mobile}手机清仓大甩卖",
            "price": random_price,
            # "createTime": time.time()*1000,
            "tmId": random.randint(0,9999999),
            "tmName": '',
            "category1Id": item.category1Id,
            "category1Name": item.category1Name,
            "category2Id": item.category2Id,
            "category2Name": item.category2Name,
            "category3Id": item.category3Id,
            "category3Name": item.category3Name,
            "hotScore": random.choice([round(i,1) for i in np.arange(1.0,5.0,0.1)]),
            "attrs": '',
            'sales': random_sales_num
        },
    )
    
    searchResponse = {
        "code": 200,
        "message": "成功",
        "data": {
            "tradeMarkList": tradeMarkList,
            "attrsList": attrsList,
            "goodsList": goodsList,
            "totalGoodsNum": total_goods_num,
            "perPageGoodsNum": 20,
            "currentPage": item.pageNo,
            "totalPagesNum": total_pages_num
        },
        "ok": True
    }
    return searchResponse


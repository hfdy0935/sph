# cSpell:ignore fastapi, pydantic

from fastapi import APIRouter, Body, Path
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Annotated
import os

from .SearchData import get_search_response

base_path = os.path.dirname(__file__)

search = APIRouter(
    prefix = '/api/search', 
    tags = ['search相关的路由']
)


# 商品信息请求体模板
class Item(BaseModel):
    category1Id: str | None = None
    category2Id: str | None = None
    category3Id: str | None = None
    category1Name: str | None = None
    category2Name: str | None = None
    category3Name: str | None = None
    keyword: str | None = None
    props: list | None = None
    tradeMark: str | None = None
    order: str | None = None
    pageNo: int | None = None
    pageSize: int | None = None



@search.post('/goods/{now_time}')
def f(item: Item = Body(..., description = '请求商品信息')):
    tmList = [item.tradeMark] if item.tradeMark else ['苹果','华为','三星', 'OPPO','VIVO','小米','山寨机']
    price_range = [i['attrValue'] for i in item.props if i['attrName'] == '价格'][0] if item.props and '价格'in str(item.props) else '500-13999'
    return get_search_response(tmList, price_range, item)


# 商品信息中的商品图片
@search.get('/goodsImage/{pageNo}/{i}')
def goodsSearchImage(
    pageNo: Annotated[int, Path(description = '页数')],
    i: Annotated[int, Path(description = '商品序号')]
):
    images = os.listdir(f'{base_path}/images/mobiles')
    index = pageNo + i - 1 if pageNo + i -1 <= 41 else (pageNo + i - 1) % 41 -1
    type_ = images[index].split('.')[-1]
    return FileResponse(f'{base_path}/images/mobiles/' + images[index], media_type = f'image/{type_}')
    

# 商品信息中的品牌图片
@search.get('/goodsBrandImage/{name}')
def phone_brand(name: Annotated[str, Path(description = '品牌名')]):
    postfix = name[-3:]
    return FileResponse(f'{base_path}/images/phones/{name}', media_type = f'image/{postfix}')


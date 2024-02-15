# cSpell:ignore fastapi
from fastapi import APIRouter
from .HomeData import TypeNavDic, banner, floor_


home = APIRouter(
    prefix = '/api/home',
    tags = ['home页面的路由']
)


@home.get('/getBaseCategoryList')
def getBaseCategoryList():
    return TypeNavDic


@home.get('/getBannerList')
def getBannerList():
    return banner


@home.get('/getFloorList')
def getFloorList():
    return floor_


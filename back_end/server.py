# cSpell:ignore fastapi, uvicorn, aiofiles

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import aiofiles


from apps.home.server import home
from apps.search.server import search
from apps.shopping_cart.server import shopping_cart
from apps.users.server import user
from apps.trade.server import trade
from apps.center.server import center


app = FastAPI()

# Vue设置了代理，这里不用设置了
# app.add_middleware(
#     CORSMiddleware, 
#     allow_origins = ['*'],
#     allow_methods = ['*'],
#     allow_headers = ['*'],
# )
app.include_router(router = home)
app.include_router(router = search)
app.include_router(router = shopping_cart)
app.include_router(router = user)
app.include_router(router = trade)
app.include_router(router = center)

# 上线时用
# @app.get('/') 
# def home_response():
#     with open('../dist/index.html', encoding = 'utf-8') as f:
#         return HTMLResponse(content = f.read(), media_type = 'text/html')
    
# @app.get('/assets/{filename}')
# async def get_file(filename: str):
#     postfix = filename.split('.')[-1]
#     dic1 = {
#         'css': 'text/css',
#         'js': 'application/javascript',
#         'ico': 'image/x-icon',
#         'json': 'application/json',
#         'map': 'application/json',
#     }
#     dic2 = {
#         'png': 'image/png',
#         'jpg': 'image/jpeg',
#         'jpeg': 'image/jpeg',
#         'gif': 'image/gif',
#         'svg': 'image/svg+xml',
#     }
#     if postfix in dic1:
#         async with aiofiles.open(f'../dist/assets/{filename}', 'r', encoding = 'utf-8') as f:
#             return Response(await f.read(), media_type = dic1[postfix])
#     elif postfix in dic2:
#        async with aiofiles.open(f'../dist/assets/{filename}', 'rb') as f:
#         return Response(await f.read(), media_type = dic2[postfix])


# app.mount('/', StaticFiles(directory = '../dist'), name = 'static')

if __name__ == '__main__':
    uvicorn.run(app = 'server:app', host = '127.0.0.1', port = 8000, reload = True)

    

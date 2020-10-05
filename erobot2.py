# インストールした discord.py を読み込む
import asyncio
import time
import discord
from discord.ext import commands
from datetime import datetime as dt
from datetime import timedelta
import csv
import os
import math
import random
import gspread
import json


# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ['DISCORD_BOT_TOKEN']
#SPREADSHEET_KEY =os.environ['GSS_CAMA']

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


# ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# 認証情報設定
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('camarade-secret_key.json', scope)

# OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

# 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1HsQ_p2Hsg2g4tb8bXClOqseIhCYoI-4-FaWNrlktdnE'

@client.event
async def on_message(message):
    a_channel = client.get_channel(762669239588487208)  # 本番用
    b_channel = client.get_channel(762669299248398366)  # 本番用
    c_channel = client.get_channel(762669351064305724)
    d_channel = client.get_channel(762669465891504169)
    e_channel = client.get_channel(762669524771274802)
    worksheet_event = gc.open_by_key(SPREADSHEET_KEY).worksheet('event')
    entry_channel = client.get_channel(737598436693770282)

    if message.author == client.user:
        return

    elif message.content.startswith('挨拶しなよえろぼっと'):
        await entry_channel.send('はじめまして。イベント採点に来ました。\n権限付与をお願いします。')

    elif message.content.startswith('csc'):
        if message.channel.id == 762669239588487208:
            point = worksheet_event.cell(2, 2).value
            point = int(point) + int(1)
            worksheet_event.update_cell(2, 2, str(point))
            total = worksheet_event.cell(2, 8).value
            await a_channel.send('Cスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669299248398366:
            point = worksheet_event.cell(3, 2).value
            point = int(point) + int(1)
            worksheet_event.update_cell(3, 2, str(point))
            total = worksheet_event.cell(3, 8).value
            await b_channel.send('Cスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669351064305724:
            point = worksheet_event.cell(4, 2).value
            point = int(point) + int(1)
            worksheet_event.update_cell(4, 2, str(point))
            total = worksheet_event.cell(4, 8).value
            await c_channel.send('Cスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669465891504169:
            point = worksheet_event.cell(5, 2).value
            point = int(point) + int(1)
            worksheet_event.update_cell(5, 2, str(point))
            total = worksheet_event.cell(5, 8).value
            await d_channel.send('Cスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669524771274802:
            point = worksheet_event.cell(6, 2).value
            point = int(point) + int(1)
            worksheet_event.update_cell(6, 2, str(point))
            total = worksheet_event.cell(6, 8).value
            await e_channel.send('Cスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )

    elif message.content.startswith('bsc'):
        if message.channel.id == 762669239588487208:
            point = worksheet_event.cell(2, 3).value
            point = int(point) + int(2)
            worksheet_event.update_cell(2, 3, str(point))
            total = worksheet_event.cell(2, 8).value
            await a_channel.send('Bスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669299248398366:
            point = worksheet_event.cell(3, 3).value
            point = int(point) + int(2)
            worksheet_event.update_cell(3, 3, str(point))
            total = worksheet_event.cell(3, 8).value
            await b_channel.send('Bスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669351064305724:
            point = worksheet_event.cell(4, 3).value
            point = int(point) + int(2)
            worksheet_event.update_cell(4, 3, str(point))
            total = worksheet_event.cell(4, 8).value
            await c_channel.send('Bスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669465891504169:
            point = worksheet_event.cell(5, 3).value
            point = int(point) + int(2)
            worksheet_event.update_cell(5, 3, str(point))
            total = worksheet_event.cell(5, 8).value
            await d_channel.send('Bスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669524771274802:
            point = worksheet_event.cell(6, 3).value
            point = int(point) + int(2)
            worksheet_event.update_cell(6, 3, str(point))
            total = worksheet_event.cell(6, 8).value
            await e_channel.send('Bスクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )

    elif message.content.startswith('blue'):
        if message.channel.id == 762669239588487208:
            point = worksheet_event.cell(2, 4).value
            point = int(point) + int(2)
            worksheet_event.update_cell(2, 4, str(point))
            total = worksheet_event.cell(2, 8).value
            await a_channel.send('青ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669299248398366:
            point = worksheet_event.cell(3, 4).value
            point = int(point) + int(2)
            worksheet_event.update_cell(3, 4, str(point))
            total = worksheet_event.cell(3, 8).value
            await b_channel.send('青ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669351064305724:
            point = worksheet_event.cell(4, 4).value
            point = int(point) + int(2)
            worksheet_event.update_cell(4, 4, str(point))
            total = worksheet_event.cell(4, 8).value
            await c_channel.send('青ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669465891504169:
            point = worksheet_event.cell(5, 4).value
            point = int(point) + int(2)
            worksheet_event.update_cell(5, 4, str(point))
            total = worksheet_event.cell(5, 8).value
            await d_channel.send('青ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669524771274802:
            point = worksheet_event.cell(6, 4).value
            point = int(point) + int(2)
            worksheet_event.update_cell(6, 4, str(point))
            total = worksheet_event.cell(6, 8).value
            await e_channel.send('青ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )

    elif message.content.startswith('祝福'):
        if message.channel.id == 762669239588487208:
            point = worksheet_event.cell(2, 5).value
            point = int(point) + int(3)
            worksheet_event.update_cell(2, 5, str(point))
            total = worksheet_event.cell(2, 8).value
            await a_channel.send('祝福付与スクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669299248398366:
            point = worksheet_event.cell(3, 5).value
            point = int(point) + int(3)
            worksheet_event.update_cell(3, 5, str(point))
            total = worksheet_event.cell(3, 8).value
            await b_channel.send('祝福付与スクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669351064305724:
            point = worksheet_event.cell(4, 5).value
            point = int(point) + int(3)
            worksheet_event.update_cell(4, 5, str(point))
            total = worksheet_event.cell(4, 8).value
            await c_channel.send('祝福付与スクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669465891504169:
            point = worksheet_event.cell(5, 5).value
            point = int(point) + int(3)
            worksheet_event.update_cell(5, 5, str(point))
            total = worksheet_event.cell(5, 8).value
            await d_channel.send('祝福付与スクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669524771274802:
            point = worksheet_event.cell(6, 5).value
            point = int(point) + int(3)
            worksheet_event.update_cell(6, 5, str(point))
            total = worksheet_event.cell(6, 8).value
            await e_channel.send('祝福付与スクのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )

    elif message.content.startswith('red'):
        if message.channel.id == 762669239588487208:
            point = worksheet_event.cell(2, 6).value
            point = int(point) + int(5)
            worksheet_event.update_cell(2, 6, str(point))
            total = worksheet_event.cell(2, 8).value
            await a_channel.send('赤ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669299248398366:
            point = worksheet_event.cell(3, 6).value
            point = int(point) + int(5)
            worksheet_event.update_cell(3, 6, str(point))
            total = worksheet_event.cell(3, 8).value
            await b_channel.send('赤ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669351064305724:
            point = worksheet_event.cell(4, 6).value
            point = int(point) + int(5)
            worksheet_event.update_cell(4, 6, str(point))
            total = worksheet_event.cell(4, 8).value
            await c_channel.send('赤ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669465891504169:
            point = worksheet_event.cell(5, 6).value
            point = int(point) + int(5)
            worksheet_event.update_cell(5, 6, str(point))
            total = worksheet_event.cell(5, 8).value
            await d_channel.send('赤ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669524771274802:
            point = worksheet_event.cell(6, 6).value
            point = int(point) + int(5)
            worksheet_event.update_cell(6, 6, str(point))
            total = worksheet_event.cell(6, 8).value
            await e_channel.send('赤ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )

    elif message.content.startswith('purple'):
        if message.channel.id == 762669239588487208:
            point = worksheet_event.cell(2, 7).value
            point = int(point) + int(10)
            worksheet_event.update_cell(2, 7, str(point))
            total = worksheet_event.cell(2, 8).value
            await a_channel.send('紫ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669299248398366:
            point = worksheet_event.cell(3, 7).value
            point = int(point) + int(10)
            worksheet_event.update_cell(3, 7, str(point))
            total = worksheet_event.cell(3, 8).value
            await b_channel.send('紫ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669351064305724:
            point = worksheet_event.cell(4, 7).value
            point = int(point) + int(10)
            worksheet_event.update_cell(4, 7, str(point))
            total = worksheet_event.cell(4, 8).value
            await c_channel.send('紫ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669465891504169:
            point = worksheet_event.cell(5, 7).value
            point = int(point) + int(10)
            worksheet_event.update_cell(5, 7, str(point))
            total = worksheet_event.cell(5, 8).value
            await d_channel.send('紫ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
        elif message.channel.id == 762669524771274802:
            point = worksheet_event.cell(6, 7).value
            point = int(point) + int(10)
            worksheet_event.update_cell(6, 7, str(point))
            total = worksheet_event.cell(6, 8).value
            await e_channel.send('紫ドロップのポイントを登録しました。\n現在のポイントは' + str(total) + 'です。' )
            
    elif message.content.startswith('del '):
        del_list = message.content.split()
        del_grade = del_list[1]
        if del_grade == 'csc':
            if message.channel.id == 762669239588487208:
                point = worksheet_event.cell(2, 2).value
                point = int(point) - int(1)
                worksheet_event.update_cell(2, 2, str(point))
                total = worksheet_event.cell(2, 8).value
                await a_channel.send('Cスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669299248398366:
                point = worksheet_event.cell(3, 2).value
                point = int(point) - int(1)
                worksheet_event.update_cell(3, 2, str(point))
                total = worksheet_event.cell(3, 8).value
                await b_channel.send('Cスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669351064305724:
                point = worksheet_event.cell(4, 2).value
                point = int(point) - int(1)
                worksheet_event.update_cell(4, 2, str(point))
                total = worksheet_event.cell(4, 8).value
                await c_channel.send('Cスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669465891504169:
                point = worksheet_event.cell(5, 2).value
                point = int(point) - int(1)
                worksheet_event.update_cell(5, 2, str(point))
                total = worksheet_event.cell(5, 8).value
                await d_channel.send('Cスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669524771274802:
                point = worksheet_event.cell(6, 2).value
                point = int(point) - int(1)
                worksheet_event.update_cell(6, 2, str(point))
                total = worksheet_event.cell(6, 8).value
                await e_channel.send('Cスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')

        elif del_grade == 'bsc':
            if message.channel.id == 762669239588487208:
                point = worksheet_event.cell(2, 3).value
                point = int(point) - int(2)
                worksheet_event.update_cell(2, 3, str(point))
                total = worksheet_event.cell(2, 8).value
                await a_channel.send('Bスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669299248398366:
                point = worksheet_event.cell(3, 3).value
                point = int(point) - int(2)
                worksheet_event.update_cell(3, 3, str(point))
                total = worksheet_event.cell(3, 8).value
                await b_channel.send('Bスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669351064305724:
                point = worksheet_event.cell(4, 3).value
                point = int(point) - int(2)
                worksheet_event.update_cell(4, 3, str(point))
                total = worksheet_event.cell(4, 8).value
                await c_channel.send('Bスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669465891504169:
                point = worksheet_event.cell(5, 3).value
                point = int(point) - int(2)
                worksheet_event.update_cell(5, 3, str(point))
                total = worksheet_event.cell(5, 8).value
                await d_channel.send('Bスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669524771274802:
                point = worksheet_event.cell(6, 3).value
                point = int(point) - int(2)
                worksheet_event.update_cell(6, 3, str(point))
                total = worksheet_event.cell(6, 8).value
                await e_channel.send('Bスクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')

        elif del_grade == 'blue':
            if message.channel.id == 762669239588487208:
                point = worksheet_event.cell(2, 4).value
                point = int(point) - int(2)
                worksheet_event.update_cell(2, 4, str(point))
                total = worksheet_event.cell(2, 8).value
                await a_channel.send('青ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669299248398366:
                point = worksheet_event.cell(3, 4).value
                point = int(point) - int(2)
                worksheet_event.update_cell(3, 4, str(point))
                total = worksheet_event.cell(3, 8).value
                await b_channel.send('青ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669351064305724:
                point = worksheet_event.cell(4, 4).value
                point = int(point) - int(2)
                worksheet_event.update_cell(4, 4, str(point))
                total = worksheet_event.cell(4, 8).value
                await c_channel.send('青ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669465891504169:
                point = worksheet_event.cell(5, 4).value
                point = int(point) - int(2)
                worksheet_event.update_cell(5, 4, str(point))
                total = worksheet_event.cell(5, 8).value
                await d_channel.send('青ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669524771274802:
                point = worksheet_event.cell(6, 4).value
                point = int(point) - int(2)
                worksheet_event.update_cell(6, 4, str(point))
                total = worksheet_event.cell(6, 8).value
                await e_channel.send('青ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')

        elif del_grade == '祝福':
            if message.channel.id == 762669239588487208:
                point = worksheet_event.cell(2, 5).value
                point = int(point) - int(3)
                worksheet_event.update_cell(2, 5, str(point))
                total = worksheet_event.cell(2, 8).value
                await a_channel.send('祝福付与スクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669299248398366:
                point = worksheet_event.cell(3, 5).value
                point = int(point) - int(3)
                worksheet_event.update_cell(3, 5, str(point))
                total = worksheet_event.cell(3, 8).value
                await b_channel.send('祝福付与スクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669351064305724:
                point = worksheet_event.cell(4, 5).value
                point = int(point) - int(3)
                worksheet_event.update_cell(4, 5, str(point))
                total = worksheet_event.cell(4, 8).value
                await c_channel.send('祝福付与スクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669465891504169:
                point = worksheet_event.cell(5, 5).value
                point = int(point) - int(3)
                worksheet_event.update_cell(5, 5, str(point))
                total = worksheet_event.cell(5, 8).value
                await d_channel.send('祝福付与スクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669524771274802:
                point = worksheet_event.cell(6, 5).value
                point = int(point) - int(3)
                worksheet_event.update_cell(6, 5, str(point))
                total = worksheet_event.cell(6, 8).value
                await e_channel.send('祝福付与スクのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')

        elif del_grade == 'red':
            if message.channel.id == 762669239588487208:
                point = worksheet_event.cell(2, 6).value
                point = int(point) - int(5)
                worksheet_event.update_cell(2, 6, str(point))
                total = worksheet_event.cell(2, 8).value
                await a_channel.send('赤ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669299248398366:
                point = worksheet_event.cell(3, 6).value
                point = int(point) - int(5)
                worksheet_event.update_cell(3, 6, str(point))
                total = worksheet_event.cell(3, 8).value
                await b_channel.send('赤ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669351064305724:
                point = worksheet_event.cell(4, 6).value
                point = int(point) - int(5)
                worksheet_event.update_cell(4, 6, str(point))
                total = worksheet_event.cell(4, 8).value
                await c_channel.send('赤ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669465891504169:
                point = worksheet_event.cell(5, 6).value
                point = int(point) - int(5)
                worksheet_event.update_cell(5, 6, str(point))
                total = worksheet_event.cell(5, 8).value
                await d_channel.send('赤ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669524771274802:
                point = worksheet_event.cell(6, 6).value
                point = int(point) - int(5)
                worksheet_event.update_cell(6, 6, str(point))
                total = worksheet_event.cell(6, 8).value
                await e_channel.send('赤ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')

        elif del_grade == 'purple':
            if message.channel.id == 762669239588487208:
                point = worksheet_event.cell(2, 7).value
                point = int(point) - int(10)
                worksheet_event.update_cell(2, 7, str(point))
                total = worksheet_event.cell(2, 8).value
                await a_channel.send('紫ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669299248398366:
                point = worksheet_event.cell(3, 7).value
                point = int(point) - int(10)
                worksheet_event.update_cell(3, 7, str(point))
                total = worksheet_event.cell(3, 8).value
                await b_channel.send('紫ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669351064305724:
                point = worksheet_event.cell(4, 7).value
                point = int(point) - int(10)
                worksheet_event.update_cell(4, 7, str(point))
                total = worksheet_event.cell(4, 8).value
                await c_channel.send('紫ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669465891504169:
                point = worksheet_event.cell(5, 7).value
                point = int(point) - int(10)
                worksheet_event.update_cell(5, 7, str(point))
                total = worksheet_event.cell(5, 8).value
                await d_channel.send('紫ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')
            elif message.channel.id == 762669524771274802:
                point = worksheet_event.cell(6, 7).value
                point = int(point) - int(10)
                worksheet_event.update_cell(6, 7, str(point))
                total = worksheet_event.cell(6, 8).value
                await e_channel.send('紫ドロップのポイントを減算しました。\n現在のポイントは' + str(total) + 'です。')

    elif message.content.startswith('elist'):
        if message.channel.id == 762669239588487208:
            worksheet_event = gc.open_by_key(SPREADSHEET_KEY).worksheet('event')
            r_list = list()
            for num in range(5):
                num_row = int(2) + num
                ch_no = worksheet_event.cell(num_row, 1).value
                get_id = worksheet_event.cell(num_row, 2).value
                get_boss = worksheet_event.cell(num_row, 3).value
                get_item = worksheet_event.cell(num_row, 4).value
                get_name = worksheet_event.cell(num_row, 5).value
                get_date = worksheet_event.cell(num_row, 6).value
                get_p = worksheet_event.cell(num_row, 7).value
                total_p = worksheet_event.cell(num_row, 8).value
                r_list.append(ch_no + ' :\t' +total_p + '  ('+ get_id + '\t/ ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date + '\t/' + get_p + ' )')
                await asyncio.sleep(1)
            r_list = '\n'.join(r_list)
            get_r = discord.Embed(title='EVENT POINT LIST',
                                  description='TEAM\t: Total point\t (C-SC \t/ B-SC \t/ BLUE \t/ 祝福 \t/ RED \t/ PURPLE)',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(r_list), inline=True)
            await a_channel.send(embed=get_r)
            return


client.run(TOKEN)

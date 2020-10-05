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
    culc_channel = client.get_channel(740355050182017135)  # 本番用
    wai_channel = client.get_channel(658468918243098626)  # 本番用
    ami_channel = client.get_channel(675359824803790850)
    list_channel = client.get_channel(743314066713477251)
    regi_channel = client.get_channel(744727455293767711)
    test_channel = client.get_channel(722253470023024640)
    zatsu_channel = client.get_channel(658468918243098626)

    if message.author == client.user:
        return

    elif message.content.startswith('最近仕事が？'):
        if message.channel.id == 658468918243098626:
            await zatsu_channel.send('忙しすぎや！( ；∀；)')

    elif message.content.startswith('roze '):
        if message.channel.id == 658468918243098626:
            worksheet_event = gc.open_by_key(SPREADSHEET_KEY).worksheet('event')
            drop_high_list = message.content.split()
            drop_grade = drop_high_list[1]
            if drop_grade == str('csc'):
                point = worksheet_event.cell(2, 2).value
                point = int(point) + int(1)
                worksheet_event.update_cell(2, 2, str(point))
                await zatsu_channel.send('Cスクのポイント登録しました。\n現在のポイントは' + str(point) + 'です。' )
                return
            if drop_grade == str('bsc'):
                point = worksheet_event.cell(2, 3).value
                point = int(point) + int(1)
                worksheet_event.update_cell(2, 3, str(point))
                await zatsu_channel.send('Bスクのポイント登録しました。\n現在のポイントは' + str(point) + 'です。' )
                return
            if drop_grade == str('blue'):
                point = worksheet_event.cell(2, 4).value
                point = int(point) + int(1)
                worksheet_event.update_cell(2, 4, str(point))
                await zatsu_channel.send('青ドロップのポイント登録しました。\n現在のポイントは' + str(point) + 'です。' )
                return
            if drop_grade == str('red'):
                point = worksheet_event.cell(2, 5).value
                point = int(point) + int(1)
                worksheet_event.update_cell(2, 5, str(point))
                await zatsu_channel.send('赤ドロップのポイント登録しました。\n現在のポイントは' + str(point) + 'です。' )
                return
            if drop_grade == str('purple'):
                point = worksheet_event.cell(2, 6).value
                point = int(point) + int(1)
                worksheet_event.update_cell(2, 6, str(point))
                await zatsu_channel.send('紫ドロップのポイント登録しました。\n現在のポイントは' + str(point) + 'です。' )
                return


    elif message.content.startswith('elist'):
        if message.channel.id == 658468918243098626:
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
                total_p = worksheet_event.cell(num_row, 7).value
                r_list.append(ch_no + ' :\t' +total_p + '  ('+ get_id + '\t/ ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date + ' )')
                await asyncio.sleep(1)
            r_list = '\n'.join(r_list)
            get_r = discord.Embed(title='EVENT POINT LIST',
                                  description='TEAM\t: Total point\t (C-SC \t/ B-SC \t/ BLUE \t/ RED \t/ PURPLE)',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(r_list), inline=True)
            await zatsu_channel.send(embed=get_r)
            return

client.run(TOKEN)

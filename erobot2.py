# インストールした discord.py を読み込む
import asyncio
import time
import discord
from discord.ext import commands, tasks
from datetime import datetime as dt
from datetime import timedelta
import csv
import os
import math
import random
import gspread
import json
import sys
import discord.user
import discord.reaction

# 自分のBotのアクセストークンに置き換えてください

TOKEN = os.environ['DISCORD_BOT_TOKEN']
# SPREADSHEET_KEY =os.environ['GSS_CAMA']

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
    time_check.start()

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

@tasks.loop(seconds=120)
async def time_check():
    sleepTime = 0
    # 現在の時刻
    loop_time = dt.now().strftime('%Y/%m/%d %H:%M')
    # print(loop_time)
    # now2 = dt.now().strftime('%Y%m%d%H%M')
    # print(now2)
    #now3 = int(dt.now().strftime('%Y%m%d%H%M')) + 1
    #print(now3)
    # # await SendMessage()
    # #該当時間だった場合は２重に投稿しないよう３０秒余計に待機
    await asyncio.sleep(120)

@client.event
async def on_raw_reaction_add(payload):
    dist_channel = client.get_channel(816859921810194472)  # 本番用

    if payload.user_id == 689736979075825706:
        return
    elif payload.user_id == 754892023613620316:
        return
    #
    # elif payload.channel_id == 732658643740262553:
    #     channel = client.get_channel(722253361159864479)
    #     now = dt.now()
    #     now1 = str(now)
    #     await channel.send(
    #         'Date&Time:\n' + now1 + '\nmessage channel & id\n' + str(payload.channel_id) + '\nmessage-id\n' + str(
    #             payload.message_id) + '\nreaction-user-id\r\n' + str(payload.user_id) + '\n_')

    elif payload.channel_id == 816859921810194472:
        msg_id = payload.message_id
        #        test_channel = client.get_channel(722253470023024640)
        msg = await dist_channel.fetch_message(msg_id)
        msg2 = str(msg.content)
        author = str(msg.author)
        if author == str('えろぼっと#4774') or author == str('えろぼっと弐号機#6410'):
            # print(msg2.startswith('<@'))
            # print(msg2.startswith('~~'))
            if msg2.startswith('<@'):
                await msg.edit(content="~~" + str(msg2) + "~~")
#                await msg.clear_reactions()
            elif msg2.startswith('~~'):
                msg1 = discord.utils.escape_markdown(msg.content)
                # print(msg1)
                msg1 = msg1.strip('\~')
                # print(msg1)
                # msg1 = msg1.rstrip("~~")
                await msg.edit(content=msg1)
                await msg.clear_reactions()
            else:
                # print('りたーん！')
                return
        else:
            #            print('えろぼっと以外へのリアクション！')
            return
    else:
        return


@client.event
async def on_message(message):
    ami_channel = client.get_channel(818338382526414868)
    list_channel = client.get_channel(816985751253942332)
    regi_channel = client.get_channel(799093019189444618)
    test_channel = client.get_channel(722253470023024640)
    sell_channel = client.get_channel(817318661076549663)
    drop_regi_channel = client.get_channel(798521158302826525)

    shokai_channel = client.get_channel(812169081003442236)
    wai_channel = client.get_channel(813791302504284240)  # 本番用
    dist_channel = client.get_channel(816859921810194472)
    b_regi_channel = client.get_channel(816858586717093898)
    r_regi_channel = client.get_channel(816859050624811028)
    if message.author == client.user:
        return

    elif message.content.startswith('test'):
        if message.channel.id == 722253470023024640:
            await test_channel.send('<@592253165068615680>')
        return

    elif message.content.startswith('えろぼっと、自己紹介！'):
        if message.channel.id == 722253470023024640:
            await wai_channel.send('これから立上げやりますので、試行でうるさくなるかもしれないけど許してね！！\nさるじへの罵倒は遠慮なく宜しくお願いします。(⌒∇⌒)')


        ###############!bunと!diceを封印格納##################
    elif message.content.startswith('!start'):
        time_check.start()

    # elif message.content.startswith('!bun '):
    #     m_num = message.content.strip('!bun ')
    #     m_list = m_num.split()
    #     # 人数ppとdiaに分ける。
    #     pp = int(m_list[0])
    #     dia = int(m_list[1])
    #
    #     if pp < 10 and dia < 5000:
    #         bunpa = dia / pp
    #         if bunpa < 50:
    #             dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
    #             await dist_channel.send(
    #                 '分配が50dia未満(' + str(math.floor(bunpa)) + 'dia/人)なので、抽選を行います。\nリアクション表示の上から ' + str(
    #                     dice) + ' 番目の方に ' + str(dia) + ' diaを渡してください。\nリアクション表示と人数が異なる場合は別途抽選を行ってください。')
    #         else:
    #             await dist_channel.send(
    #                 '10人未満,5000dia未満なので以下となります。\n分配：' + str(math.floor(bunpa)) + 'dia\n血盟資金、分配者手数料はありません。')
    #             return
    #
    #     elif pp < 10 and dia >= 5000:
    #         ketsu = dia * 0.03
    #         bunpb = (dia - ketsu * 3) / pp
    #         await dist_channel.send(
    #             '10人未満, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
    #                 math.floor(bunpb)) + 'diaになります。\n分配者手数料は１０人未満なのでありません。')
    #         return
    #
    #     else:
    #         if 10 <= pp < 25 and dia >= 5000:
    #             ketsu = dia * 0.03
    #             tema = dia * 0.05
    #             if tema < 500:
    #                 bunpb = (dia - ketsu * 3 - tema) / pp
    #                 await dist_channel.send(
    #                     '10人以上, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
    #                         math.floor(bunpb)) + 'diaになります。\nちなみに手間賃は' + str(math.floor(tema)) + 'diaです。')
    #                 return
    #             elif tema >= 500:
    #                 tema = 500
    #                 bunpb = (dia - ketsu * 3 - tema) / pp
    #                 await dist_channel.send(
    #                     '10人以上, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
    #                         math.floor(bunpb)) + 'diaになります。\nちなみに手間賃は上限の' + str(math.floor(tema)) + 'diaです。')
    #                 return
    #             else:
    #                 await dist_channel.send('えろてろまで問い合わせを。')
    #
    #         elif 10 <= pp < 25 and dia < 5000:
    #             tema = dia * 0.05
    #             bunpb = (dia - tema) / pp
    #             if bunpb < 50:
    #                 dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
    #                 await dist_channel.send(
    #                     '分配が50dia未満(' + str(math.floor(bunpb)) + 'dia/人)なので、抽選を行います。\nリアクション表示の上から ' + str(
    #                         dice) + ' 番目の方に' + str(dia) + 'diaを渡してください。\nリアクション表示と人数が異なる場合は別途抽選を行ってください。')
    #                 return
    #             else:
    #                 await dist_channel.send(
    #                     '10人以上, 5000dia未満なので以下となります。\n分配：' + str(math.floor(bunpb)) + 'diaになります。\n分配者手数料は' + str(
    #                         math.floor(tema)) + 'diaです。\n血盟資金はありません。')
    #                 return
    #
    #         else:
    #             if pp >= 25 and dia >= 5000:
    #                 ketsushi = dia * 0.03
    #                 bunpc = (dia - ketsushi * 3) / pp
    #                 if bunpc < 100:
    #                     meishubun1 = dia / 3
    #                     await dist_channel.send('25人以上 / 分配 100dia未満なので全額血盟資金となります。\n３等分した' + str(
    #                         math.floor(meishubun1)) + 'diaを各盟主に渡してください。\n分配者手数料、血盟資金はありません。')
    #                     return
    #                 else:
    #                     await dist_channel.send('25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。\n' + str(
    #                         math.floor(bunpc)) + ' × 各血盟の対象人数 + ' + str(
    #                         math.floor(ketsushi)) + 'dia(血盟資金）の合計を各盟主に渡してください。\n分配者手数料はありません。')
    #                     return
    #             elif pp >= 25 and dia < 5000:
    #                 bunpd = dia / pp
    #                 if bunpd < 100:
    #                     meishubun2 = dia / 3
    #                     await dist_channel.send('25人以上で分配が100dia/人 未満なので全額血盟資金となります。\n' + str(
    #                         math.floor(meishubun2)) + 'diaを各盟主に渡してください。\n分配者手数料、血盟資金はありません。')
    #                     return
    #                 else:
    #                     await dist_channel.send(
    #                         '25人以上で分配が100dia/人 以上なので以下に従って盟主と取引して下さい。\n今回は盟主が分配するため、血盟資金 + 各血盟の対象人数 × ' + str(
    #                             math.floor(bunpd)) + 'diaを各盟主に渡してください。\n分配者手数料はありません。')
    #                     return
    #             else:
    #                 await dist_channel.send('えろてろまで問い合わせを。')

    # elif message.content.startswith('!dice '):
    #     if message.channel.id == 675359824803790850:
    #         rami_num = message.content.strip('!dice ')
    #         rami_list = rami_num.split()
    #         # 人数ppとdiaに分ける。
    #         rami_rand = int(rami_list[0])
    #         rami_dice = random.randint(1, rami_rand)  # サイコロを振る。出る目を指定。
    #         await ami_channel.send('抽選した結果、' + str(rami_dice) + ' 番が当選！オーメデトーゴーザイマース！')
    #         return
    #     return

    elif message.content.startswith('ami '):
        if message.channel.id == 818338382526414868:
            nami_num = message.content.strip('ami')
            nami_list = nami_num.split()
            nami_rand = random.choice(nami_list)
            await ami_channel.send('抽選した結果、' + str(nami_rand) + ' が当選！オーメデトーゴーザイマース！')
            return
        return

    elif message.content.startswith('ワイが'):
        if message.author.id == 591281241798737938:
            await wai_channel.send('アンタ誰や？下の板言うてないで狩りしーや？')
            return
        else:
            await wai_channel.send(message.author.name + 'や。さるじやあらへん。\nあいつは今びっくり焼きを調べるのに夢中やで！')
            return

    elif message.content.endswith('さるじや'):
        if message.content.startswith('ワイが'):
            if message.author.id == 591281241798737938:
                await wai_channel.send('パカラッパカラッ！\nヒヒーン(*´ω｀*)')
            else:
                await wai_channel.send('さるじのケツでも蹴っとき！')
        else:
            await wai_channel.send('さるじなら100dia罰金な')

    elif message.content.startswith('残高照会'):
        if message.author.id == 591281241798737938:
            await wai_channel.send('どうせまた借金するんやろ？')
        else:
            await wai_channel.send('さるじさん６万')

    elif message.content.startswith('え、またさるじが？'):
        if message.author.id == 591281241798737938:
            await wai_channel.send('はよ金かえしや？')
        else:
            await wai_channel.send('また魚雷さんんから金借りたで？')

    elif message.content.startswith('なんや'):
        if message.author.id == 591281241798737938:
            await wai_channel.send('1万D')
        else:
            await wai_channel.send('・・・')

    elif message.content.startswith('バナナ'):
        if message.author.id == 591281241798737938:
            await wai_channel.send('1万D')
        else:
            await wai_channel.send('さるじ')

    # **********************************#
    # アイテム管理用リアクション追加
    # **********************************#

    elif message.content.startswith('get '):
        if message.channel.id == 816859050624811028:
            drop_high_list = message.content.split()
            drop_high_boss = drop_high_list[1]
            drop_high_item = drop_high_list[2]
            today = dt.now()
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_rare')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_ID_LIST')
            id_total = worksheet_id.cell(4, 8).value
            id_num = worksheet_id.cell(4, 10).value
            input_id = int(id_total) + 2
            id_no = int(id_num) + int(1)
            worksheet_list.update_cell(input_id, 1, 'r' + str(id_no))
            worksheet_list.update_cell(input_id, 2, str(drop_high_boss))
            worksheet_list.update_cell(input_id, 3, str(drop_high_item))
            worksheet_list.update_cell(input_id, 4, str('rare'))
            worksheet_list.update_cell(input_id, 5, str(message.author.name))
            worksheet_list.update_cell(input_id, 6, str(today.year) + '/' + str(today.month) + '/' + str(today.day))
            worksheet_list.update_cell(input_id, 7, str('none'))
            worksheet_list.update_cell(input_id, 8, str(message.id))
            worksheet_list.update_cell(input_id, 12, str(message.author.id))
            worksheet_list.update_cell(input_id, 168, 1)
            drp = discord.Embed(title='ID: r' + str(id_no) + ' / " ' + str(drop_high_boss) + ' " / " ' + str(drop_high_item) + ' "\n拾得者:' + str(message.author.name), description=' 参加者はリアクションして下さい。/Please reaction!', color=discord.Colour.red())
            msg = await r_regi_channel.send(embed=drp)  # debag
            emoji1 = '\U0001F947'
            await msg.add_reaction(emoji1)
            worksheet_list.update_cell(input_id, 8, str(msg.id))
            return

        elif message.channel.id == 816858586717093898:
            drop_high_list = message.content.split()
            drop_high_boss = drop_high_list[1]
            drop_high_item = drop_high_list[2]
            today = dt.now()
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_normal')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_ID_LIST')
            id_total = worksheet_id.cell(8, 8).value
            id_num = worksheet_id.cell(8, 9).value
            input_id = int(id_total) + 2
            id_no = int(id_num) + int(1)
            worksheet_list.update_cell(input_id, 1, 'n' + str(id_no))
            worksheet_list.update_cell(input_id, 2, str(drop_high_boss))
            worksheet_list.update_cell(input_id, 3, str(drop_high_item))
            worksheet_list.update_cell(input_id, 4, str('normal'))
            worksheet_list.update_cell(input_id, 5, str(message.author.name))
            worksheet_list.update_cell(input_id, 6, str(today.year) + '/' + str(today.month) + '/' + str(today.day))
            worksheet_list.update_cell(input_id, 7, str('none'))
            worksheet_list.update_cell(input_id, 8, str(message.id))
            worksheet_list.update_cell(input_id, 12, str(message.author.id))
            worksheet_list.update_cell(input_id, 168, 1)
            #idとか格納の名前に、ID番号を付与してあげると重複しなくなる？
            #ここに別鯖に保管しているMSGIDを固定で入力。流れはfetchして格納→INTにして+1→editして再保管。その数値をそのまま使う。
            limit_hour = int(today.hour) + int(1)
            limit_min = int(today.minute)
            drp = discord.Embed(title='ID: n' + str(id_no) + ' / " ' + str(drop_high_boss) + ' " / " ' + str(
                drop_high_item) + ' "\n拾得者:' + str(message.author.name),
                                description='参加者はリアクションして下さい。\n受付終了は' + str(today.month) + '月' + str(today.day) + '日' + str(limit_hour) + '時' + str(limit_min) + '分です。', color=discord.Colour.red())
            msg = await b_regi_channel.send(embed=drp)  # debag
            emoji1 = '\U0001F947'
            await msg.add_reaction(emoji1)
            # await asyncio.sleep(10)
            # await blue_channel.send('ID: n' + str(id_no) + ' の受付終了(抽選開始)まで@3hrです')
            # await asyncio.sleep(10)
            # await blue_channel.send('ID: n' + str(id_no) + ' の受付終了(抽選開始)まで@1hrです')
            # await asyncio.sleep(10)
            # await blue_channel.send('ID: n' + str(id_no) + ' の受付終了(抽選開始)まで@30minです')
            await asyncio.sleep(21600)
            entry_msg = await b_regi_channel.fetch_message(msg.id)  # BOTのメッセージ情報を格納
            reaction_num = int(entry_msg.reactions[0].count)
            reac_users = await entry_msg.reactions[0].users().flatten()  # botのメッセージ情報からリアクションユーザー情報を格納。
            reac_user = list()
            for num in range(int(reaction_num)):
                reac_user.append(str(reac_users[num].id))
            if str(754892023613620316) in reac_user:
                reac_user.remove(str(754892023613620316))  # bot idをリアクション情報から削除
            if str(689736979075825706) in reac_user:
                reac_user.remove(str(689736979075825706))  # bot idをリアクション情報から削除
            ran_men = random.choice(reac_user)
            await dist_channel.send('ID: n' + str(id_no) + ' が定刻になりましたので抽選を行います。\n~~~~~当選者~~~~~\n★　<@' + str(
                ran_men) + '>　★ \n~~~~~~~~~~~~~~~\n当選者は<@' + str(message.author.id) + '>と' + str(
                drop_high_boss) + ' " / " ' + str(
                drop_high_item) + ' の取引を行ってください。')

    #
    # elif message.content.startswith('!del '):
    #     if message.channel.id == 743314066713477251:
    #         if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
    #             worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
    #             del_list = message.content.split()
    #             del_cell = worksheet_find.findall(str(del_list[1]))
    #             del_id = worksheet_find.cell(del_cell[0].row, 1).value
    #             #                worksheet_find.update_cell(del_cell[0].row, 1, '')
    #             worksheet_find.update_cell(del_cell[0].row, 2, '-')
    #             worksheet_find.update_cell(del_cell[0].row, 3, '-')
    #             #                worksheet_find.update_cell(del_cell[0].row, 4, '')
    #             worksheet_find.update_cell(del_cell[0].row, 5, '-')
    #             worksheet_find.update_cell(del_cell[0].row, 6, '-')
    #             worksheet_find.update_cell(del_cell[0].row, 7, 'delete')
    #             worksheet_find.update_cell(del_cell[0].row, 10, '')
    #             worksheet_find.update_cell(del_cell[0].row, 11, '')
    #             del_p = int(worksheet_find.cell(del_cell[0].row, 166).value)
    #             for num in range(del_p):
    #                 num = num + int(12)
    #                 worksheet_find.update_cell(del_cell[0].row, num, '')
    #             await list_channel.send(del_id + 'を削除しました。')
    #
    # elif message.content.startswith('!back '):
    #     if message.channel.id == 743314066713477251:
    #         if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
    #             worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
    #             del_list = message.content.split()
    #             del_cell = worksheet_find.findall(str(del_list[1]))
    #             del_id = worksheet_find.cell(del_cell[0].row, 1).value
    #             worksheet_find.update_cell(del_cell[0].row, 7, 'none')
    #             worksheet_find.update_cell(del_cell[0].row, 10, '-')
    #             await list_channel.send(del_id + 'を未分配に戻しました。')
    #
    # elif message.content.startswith('!fin '):
    #     if message.channel.id == 743314066713477251:
    #         if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
    #             worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
    #             fin_list = message.content.split()
    #             fin_dia = fin_list[2]
    #             fin_cell = worksheet_find.findall(str(fin_list[1]))
    #             fin_id = worksheet_find.cell(fin_cell[0].row, 1).value
    #             worksheet_find.update_cell(fin_cell[0].row, 7, 'finish')
    #             worksheet_find.update_cell(fin_cell[0].row, 10, str(fin_dia))
    #             await list_channel.send(fin_id + 'を分配完了にしました。')
    #
    # elif message.content.startswith('!own_change '):
    #     if message.channel.id == 743314066713477251:
    #         worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
    #         che_list = message.content.split()
    #         che_cell = worksheet_find.findall(str(che_list[1]))
    #         worksheet_find.update_cell(che_cell[0].row, 5, str(che_list[2]))
    #
    # elif message.content.startswith('list'):
    #     if message.channel.id == 743314066713477251:
    #         worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
    #         worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
    #         cell_list = worksheet_find.findall('none')
    #         # print(cell_list)
    #         deal_count = worksheet_id.cell(5, 8).value
    #         r_list = list()
    #         for num in range(int(deal_count)):
    #             get_id = worksheet_find.cell(cell_list[num].row, 1).value
    #             get_boss = worksheet_find.cell(cell_list[num].row, 2).value
    #             get_item = worksheet_find.cell(cell_list[num].row, 3).value
    #             get_name = worksheet_find.cell(cell_list[num].row, 5).value
    #             get_date = worksheet_find.cell(cell_list[num].row, 6).value
    #             r_list.append(get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
    #             await asyncio.sleep(4)
    #             if num == 20:
    #                 r_list = '\n'.join(r_list)
    #                 get_r = discord.Embed(title='DROP ITEM LIST (GRADE: ALL)',
    #                                       description='ID \t:\t  boss \t/  item \t/  holder \t/  date',
    #                                       color=discord.Colour.red())
    #                 get_r.add_field(name='---------------------------------------------', value=str(r_list),
    #                                 inline=True)
    #                 await list_channel.send(embed=get_r)
    #                 await list_channel.send('以下にまだ続きます。もうしばらくお待ちください。')
    #                 r_list = list()
    #         r_list = '\n'.join(r_list)
    #         get_r = discord.Embed(title='DROP ITEM LIST (GRADE: ALL)',
    #                               description='ID \t:\t  boss \t/  item \t/  holder \t/  date',
    #                               color=discord.Colour.red())
    #         get_r.add_field(name='---------------------------------------------', value=str(r_list), inline=True)
    #         await list_channel.send(embed=get_r)
    #         return

    elif message.content.startswith('mylist'):
        if message.channel.id == 816985751253942332:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_rare')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_ID_LIST')
            cell_list = worksheet_find.findall(str(message.author.id))
            #            cell_list = worksheet_find.findall(str('CAMARADE＠どすこい'))
            # print(cell_list)
            deal_count = len(cell_list)
            confirm_list = list()
            for num in range(int(deal_count)):
                # print(int(cell_list[num].col))
                if cell_list[num].col == 12:
                    confirm_list.append(cell_list[num])
            confirm_count = len(confirm_list)
            # print(confirm_count)
            # print(confirm_list)
            if confirm_count == 0:
                await list_channel.send('ご苦労様です。\n' + str(message.author.name) + ' さんの未分配案件はありません。')
                return
            r_list = list()
            # print(confirm_count)
            par_read = 0
            par_msg = await list_channel.send('Load progress...' + str(par_read) + '%')
            for num in range(int(confirm_count)):
                par_read = int(num) / int(confirm_count) * 100
                await par_msg.edit(content='Load progress...' + str(math.floor(par_read)) + '%')
                # print(num)
                # print(worksheet_find.cell(confirm_list[num].row, 7).value)
                if worksheet_find.cell(confirm_list[num].row, 7).value == str('none'):
                    get_id = worksheet_find.cell(confirm_list[num].row, 1).value
                    get_boss = worksheet_find.cell(confirm_list[num].row, 2).value
                    get_item = worksheet_find.cell(confirm_list[num].row, 3).value
                    get_name = worksheet_find.cell(confirm_list[num].row, 5).value
                    get_date = worksheet_find.cell(confirm_list[num].row, 6).value
                    r_list.append(
                        get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
                    await asyncio.sleep(2)
                    # print(r_list)
                else:
                    await asyncio.sleep(1)
                # print(r_list)
                # print(len(r_list))
                r_count = int(len(r_list))
            await par_msg.edit(content='Load progress...100%')
            if r_count == 0:
                await list_channel.send('ご苦労様です。\n' + str(message.author.name) + ' さんの未分配案件はありません。\n全て完了していました。')
                # print('ハズレー')
                return
            if num == 20:
                r_list = '\n'.join(r_list)
                get_r = discord.Embed(title='DROP ITEM LIST (GRADE: ALL)',
                                      description='ID \t:\t  boss \t/  item \t/  holder \t/  date',
                                      color=discord.Colour.red())
                get_r.add_field(name='---------------------------------------------', value=str(r_list),
                                inline=True)
                await list_channel.send(embed=get_r)
                await list_channel.send('以下にまだ続きます。もうしばらくお待ちください。')
                r_list = list()
            r_list = '\n'.join(r_list)
            get_r = discord.Embed(title='DROP ITEM LIST (GRADE: ALL)',
                                  description='ID \t:\t  boss \t/  item \t/  holder \t/  date',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(r_list), inline=True)
            await list_channel.send(embed=get_r)
            return

    elif message.content.startswith('bun '):
        if message.channel.id == 816859921810194472:
            await dist_channel.send('Please wait...')
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_rare')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_ID_LIST')
            rbun_list = message.content.split()
            rbun_id = rbun_list[1]  # idを格納
            rbun_dia = rbun_list[2]  # diaを格納
            id_cell = worksheet_list.find(str(rbun_id))  # idからスプシの行を検索
            if worksheet_list.cell(id_cell.row, 7).value == 'finish':
                await dist_channel.send(str(rbun_id) + 'は分配案内が完了しています。\n' + str(rbun_id) + ' was finished.\n')
                return

            entry_msg_id = worksheet_list.cell(id_cell.row, 8).value  # BOTのメッセージIDを格納
            entry_msg = await r_regi_channel.fetch_message(entry_msg_id)  # BOTのメッセージ情報を格納
            reaction_num = int(entry_msg.reactions[0].count)  # botのリアクション数を格納。
            reac_users = await entry_msg.reactions[0].users().flatten()  # botのメッセージ情報からリアクションユーザー情報を格納。
            reac_user = list()
            for num in range(int(reaction_num)):
                reac_user.append(str(reac_users[num].id))
            own_id = str(worksheet_list.cell(id_cell.row, 12).value)  # スプシから拾得者IDを格納。
            if str(754892023613620316) in reac_user:
                reac_user.remove(str(754892023613620316))  # bot idをリアクション情報から削除
            if str(689736979075825706) in reac_user:
                reac_user.remove(str(689736979075825706)) # bot idをリアクション情報から削除
            if not own_id in str(reac_user):  # 登録者（拾得者）がリアクションしていた場合　（していない場合、reac_userに追加する）
                reac_user.append(str(own_id))  # リアクション情報から登録者IDを追加
            buyer_id = str(worksheet_list.cell(id_cell.row, 11).value)  # 購入者のidを格納
            boss = str(worksheet_list.cell(id_cell.row, 2).value)
            items = str(worksheet_list.cell(id_cell.row, 3).value)
            buyer_check = int(0)
            pp = int(len(reac_user))
            if buyer_id in str(reac_user):  # 購入者が参加者にいるか確認
                await dist_channel.send(str(rbun_id) + 'には購入者が含まれています。\n' + str(rbun_id) + ' is include buyer.')
                buyer_check = int(1)
            worksheet_list.update_cell(id_cell.row, 7, str('progress'))  # 分配進行フラグ変更
            worksheet_list.update_cell(id_cell.row, 10, str(rbun_dia))  # 分配ダイア入力
            dia = int(rbun_dia)
            cama_list = list()
            ten_list = list()
            samurai_list = list()

            if pp < 10 and dia < 5000:
                bunpa = dia / pp
                if bunpa < 50:
                    ran_men = random.choice(reac_user)
                    if buyer_check == int(1):
                        if buyer_id == ran_men:
                            while buyer_id == ran_men:
                                ran_men = random.choice(reac_user)
                    worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                    await dist_channel.send(
                        str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(dia) + ' dia. \nDistributor: <@' + str(
                            own_id) + '>\n抽選します!! / hold a lottery !!\nWinner =>> <@' + str(
                            ran_men) + '> !!\nPlease would like a transaction. ')
                    return
                else:
                    if buyer_check == int(1):
                        bunpa = dia / (pp - int(1))
                    await dist_channel.send(str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(
                        dia) + ' dia.\nDistributor: <@' + str(own_id) + '>\ndividend：' + str(
                        math.floor(bunpa)) + ' dia\nReceiver')

                    for num in range(pp):
                        if not reac_user[num] == buyer_id:
                            await dist_channel.send('<@' + str(reac_user[num]) + '>')
                    worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                    await dist_channel.send('finish')
                    return
            elif pp < 10 and dia >= 5000:
                if buyer_check == int(1):
                    ketsu = dia * 0.03
                    bunpb = (dia - ketsu * 3) / (pp - 1)
                else:
                    ketsu = dia * 0.03
                    bunpb = (dia - ketsu * 3) / pp
                await dist_channel.send(
                    str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(
                        dia) + ' dia.\nDistributor : "<@' + str(own_id) + '>"\nClan resource : ' + str(
                        math.floor(
                            ketsu)) + 'dia\nClan resource receiver(血盟資金受取者)\n<@363032621845839892>\n<@477504935727071232>\n<@477111013590695936>\n\ndividend ' + str(
                        math.floor(
                            bunpb)) + ' dia.\nReceiver\n')
                for num in range(pp):
                    if not reac_user[num] == buyer_id:
                        await dist_channel.send('<@' + str(reac_user[num]) + '>')

                worksheet_list.update_cell(id_cell.row, 7, str('finish'))

                await dist_channel.send('finish')
                return
            else:
                if 10 <= pp < 25 and dia >= 5000:
                    ketsu = dia * 0.03
                    tema = dia * 0.05
                    if tema < 500:
                        if buyer_check == int(1):
                            bunpb = (dia - ketsu * 3 - tema) / (pp - 1)
                        else:
                            bunpb = (dia - ketsu * 3 - tema) / pp

                        await dist_channel.send(
                            str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(
                                dia) + ' dia.\nDistributor : "<@' + str(own_id) + '>"\nClan resource : ' + str(
                                math.floor(
                                    ketsu)) + 'dia\nClan resource receiver(血盟資金受取者)\n<@363032621845839892>\n<@477504935727071232>\n<@477111013590695936>\n\ndividend ' + str(
                                math.floor(
                                    bunpb)) + ' dia.(手間賃は割愛）\nReceiver\n')

                        for num in range(pp):
                            if not reac_user[num] == buyer_id:
                                await dist_channel.send('<@' + str(reac_user[num]) + '>')

                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        await dist_channel.send('finish')
                    elif tema >= 500:
                        tema = 500
                        if buyer_check == int(1):
                            bunpb = (dia - ketsu * 3 - tema) / (pp - 1)
                        else:
                            bunpb = (dia - ketsu * 3 - tema) / pp
                        await dist_channel.send(
                            str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(
                                dia) + ' dia.\nDistributor : "<@' + str(own_id) + '>"\nClan resource : ' + str(
                                math.floor(
                                    ketsu)) + 'dia\nClan resource receiver(血盟資金受取者)\n<@363032621845839892>\n<@477504935727071232>\n<@477111013590695936>\n\ndividend ' + str(
                                math.floor(
                                    bunpb)) + ' dia.(手間賃は割愛）\nReceiver\n')
                        for num in range(pp):
                            if not reac_user[num] == buyer_id:
                                await dist_channel.send('<@' + str(reac_user[num]) + '>')
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        await dist_channel.send('finish!')
                    else:
                        await dist_channel.send('えろてろまで問い合わせを。')
                    return
                elif 10 <= pp < 25 and dia < 5000:
                    tema = dia * 0.05
                    if buyer_check == int(1):
                        bunpb = (dia - tema) / (pp - 1)
                    else:
                        bunpb = (dia - tema) / pp
                    if bunpb < 50:
                        ran_men = random.choice(reac_user)
                        if buyer_check == int(1):
                            if buyer_id == ran_men:
                                while buyer_id == ran_men:
                                    ran_men = random.choice(reac_user)
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        await dist_channel.send(
                            str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(
                                dia) + ' dia. \nDistributor: <@' + str(
                                own_id) + '>\n抽選します!! / hold a lottery !!\nWinner =>> <@' + str(
                                ran_men) + '> !!\nPlease would like a transaction. ')
                        await dist_channel.send('finish!')
                        return
                    else:
                        await dist_channel.send(str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(
                            dia) + ' dia.\nDistributor: <@' + str(own_id) + '>\ndividend：' + str(
                            math.floor(bunpb)) + ' dia(手間賃は割愛）\nReceiver')

                        for num in range(pp):
                            if not reac_user[num] == buyer_id:
                                await dist_channel.send('<@' + str(reac_user[num]) + '>')
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        await dist_channel.send('finish!')
                        return
                else:
                    if pp >= 25 and dia >= 5000:
                        ketsushi = dia * 0.03
                        bunpc = (dia - ketsushi * 3) / pp
                        if bunpc < 100:
                            meishubun1 = dia / 3
                            await dist_channel.send(
                                str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(
                                    dia) + ' dia.\nDistributor : "<@' + str(own_id) + '>"\nClan resource : ' + str(
                                    math.floor(
                                        ketsushi)) + 'dia\nClan resource receiver(血盟資金受取者)\n<@363032621845839892>\n<@477504935727071232>\n<@477111013590695936>')
                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                            await dist_channel.send('finish!')
                            return
                        else:
                            cama_num = 0
                            ten_num = 0
                            samurai_num = 0
                            cama_member = list()
                            ten_member = list()
                            samurai_member = list()
                            cama_member = [591281241798737938, 352019449022251009,
                                           648874408630550530, 498797752050909184, 593978426185220137,
                                           787341771042062336, 608663618963243031, 598899242718855169,
                                           572992862682087424, 633837702776881192, 814113620718780476,
                                           601044406824337438, 715840411364491305, 799941467908603904,
                                           477504935727071232, 640848694035480576, 610405882970374144,
                                           361082138197491712, 381442228419297292, 608712090882146374,
                                           617742185311502346, 598823438521597965, 592253165068615680,
                                           206754555147321344, 814787444524056577, 598806516635533313,
                                           814131018964402216, 684800253228351609, 462190506655612929,
                                           386438573508788227, 582904777722036224, 585823046338609163,
                                           598834500025450517, 713334687354978304, 232492256047792128,
                                           689731790935425034, 399894319965929472, 363427335220887552,
                                           608641992267661352, 470896836471947281, 612143447956258825,
                                           471100732183937024, 630939307913510925, 624407030794551296,
                                           567827459706191892]

                            ten_member = [279366431701860354, 383942877153329153, 487312403344785409,
                                          582886453814493185, 249699780324884491, 743873630303158314,
                                          587946802607685643, 593220004531535872, 366813477102288896,
                                          597217127027572773, 584738856759328769, 588742391582687232,
                                          581306432306282497, 627007978708533270, 593786971474624512,
                                          600714140654370829, 584886819003432990, 452822134134276116,
                                          680080893133848591, 312616730549813248, 676413785921159170,
                                          693108538678968401, 678479687063961611, 598430494798905369,
                                          465005064344305686, 594514512691068969, 599258155544739850,
                                          597633205142814731, 595568702057873418, 283952097534148608,
                                          653180752762109955, 605356086291202081, 635427428839194634,
                                          582699931978956830, 477111013590695936, 713375398162858065,
                                          582775090178162691, 401754760044085249, 596465179500478464,
                                          661110540893945896, 619043196403580937, 282817087284707330,
                                          608636538510901258, 269092285994500096, 584691376504045568,
                                          588526302747820090, 648129386729570306, 609377883676213288,
                                          594497202789941258, 582924064083935233, 587415835455258666,
                                          309380609162346506, 589530506757144576, 358589597187571723,
                                          688196103002259604, 586151450607091717, 592279144893644811,
                                          597427127847223296, 598870533924323348, 475681787306049567,
                                          303786534925238282]

                            samurai_member = [668433312678674432, 421674740751532032, 698984669622042645,
                                              665400023491674112, 686580674135719948, 668439280573612052,
                                              326741192739913728, 687997488204087396, 614397835705712651,
                                              589380212962230283, 736172855280140429, 576802484773715969,
                                              523678876686090260, 676076916813463553, 523142685205463050,
                                              368074547150454792, 516046250538434578, 414947776586186765,
                                              609561458811863076, 363032621845839892, 468054964615512084,
                                              614863681351712781, 668372877510443009, 701801263930671145,
                                              611228472911724583, 574902915391684608, 381412006969868290,
                                              673508187302920192, 488936383902384129, 686580275957727269,
                                              595625719451877376, 588029745745231937, 695600188617916446,
                                              668433882743308307, 671650108391030784, 333511394010071051,
                                              670962542025375744, 586782561745764354, 364785331163234304,
                                              375534189162004482, 686492852737540116, 563048784569827347]

                            for num in range(pp):
                                if not reac_user[num] == buyer_id:
                                    if reac_user[num] in cama_member:
                                        cama_list.append('<@' + str(reac_user[num]) + '>')
                                        cama_num = cama_num + 1
                                    elif reac_user[num] in ten_member:
                                        ten_list.append('<@' + str(reac_user[num]) + '>')
                                        ten_num = ten_num + 1
                                    elif reac_user[num] in samurai_member:
                                        samurai_list.append('<@' + str(reac_user[num]) + '>')
                                        samurai_num = samurai_num + 1
                            cama_list = '\n'.join(cama_list)
                            ten_list = '\n'.join(ten_list)
                            samurai_list = '\n'.join(samurai_list)
                            bun_cama = bunpc * cama_num + ketsushi
                            bun_ten = bunpc * ten_num + ketsushi
                            bun_samurai = bunpc * samurai_num + ketsushi
                            await dist_channel.send(
                                str(rbun_id) + 'の' + str(boss) + '/' + str(
                                    items) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                     5).value) + 'と取引を行って下さい。\n25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。\n尚、血盟資金 ' + str(
                                    math.floor(ketsushi)) + 'diaも含まれています。\n\n<@477504935727071232>さん： ' + str(
                                    math.floor(bun_cama)) + ' diaを受取り、以下の方に ' + str(
                                    math.floor(bunpc)) + ' diaを分配下さい。\n' + str(
                                    cama_list) + '\n\n<@363032621845839892>さん： ' + str(
                                    math.floor(bun_samurai)) + ' diaを受取り、以下の方に ' + str(
                                    math.floor(bunpc)) + ' diaを分配下さい。\n' + str(
                                    samurai_list) + '\n\n<@477111013590695936>さん： ' + str(
                                    math.floor(bun_ten)) + ' diaを受取り、以下の方に ' + str(
                                    math.floor(bunpc)) + ' diaを分配下さい。\n ' + str(ten_list))
                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                            await dist_channel.send('finish!')
                            return

                    elif pp >= 25 and dia < 5000:
                        # print('ここまできたよ')
                        bunpd = dia / pp
                        if bunpd < 100:
                            meishubun2 = dia / 3
                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))

                            await dist_channel.send(
                                str(rbun_id) + 'の' + str(boss) + '/' + str(
                                    items) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                     5).value) + 'と取引を行って下さい。\n25人以上で分配が100dia/人 未満なので全額血盟資金となります。\n' + str(
                                    math.floor(
                                        meishubun2)) + 'diaを各盟主に渡してください。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@477111013590695936>\n分配者手数料はありません。\n\nfinish!')
                            return
                        else:
                            cama_num = 0
                            ten_num = 0
                            samurai_num = 0
                            cama_member = list()
                            ten_member = list()
                            samurai_member = list()
                            cama_member = [591281241798737938, 352019449022251009, 567827459706191892,
                                           648874408630550530, 498797752050909184, 593978426185220137,
                                           787341771042062336, 608663618963243031, 598899242718855169,
                                           572992862682087424, 633837702776881192, 814113620718780476,
                                           601044406824337438, 715840411364491305, 799941467908603904,
                                           477504935727071232, 640848694035480576, 610405882970374144,
                                           361082138197491712, 381442228419297292, 608712090882146374,
                                           617742185311502346, 598823438521597965, 592253165068615680,
                                           206754555147321344, 814787444524056577, 598806516635533313,
                                           814131018964402216, 684800253228351609, 462190506655612929,
                                           386438573508788227, 582904777722036224, 585823046338609163,
                                           598834500025450517, 713334687354978304, 232492256047792128,
                                           689731790935425034, 399894319965929472, 363427335220887552,
                                           608641992267661352, 470896836471947281, 612143447956258825,
                                           471100732183937024, 630939307913510925, 624407030794551296,
                                           567827459706191892]

                            ten_member = [279366431701860354, 383942877153329153, 487312403344785409,
                                          582886453814493185, 249699780324884491, 743873630303158314,
                                          587946802607685643, 593220004531535872, 366813477102288896,
                                          597217127027572773, 584738856759328769, 588742391582687232,
                                          581306432306282497, 627007978708533270, 593786971474624512,
                                          600714140654370829, 584886819003432990, 452822134134276116,
                                          680080893133848591, 312616730549813248, 676413785921159170,
                                          693108538678968401, 678479687063961611, 598430494798905369,
                                          465005064344305686, 594514512691068969, 599258155544739850,
                                          597633205142814731, 595568702057873418, 283952097534148608,
                                          653180752762109955, 605356086291202081, 635427428839194634,
                                          582699931978956830, 477111013590695936, 713375398162858065,
                                          582775090178162691, 401754760044085249, 596465179500478464,
                                          661110540893945896, 619043196403580937, 282817087284707330,
                                          608636538510901258, 269092285994500096, 584691376504045568,
                                          588526302747820090, 648129386729570306, 609377883676213288,
                                          594497202789941258, 582924064083935233, 587415835455258666,
                                          309380609162346506, 589530506757144576, 358589597187571723,
                                          688196103002259604, 586151450607091717, 592279144893644811,
                                          597427127847223296, 598870533924323348, 475681787306049567]

                            samurai_member = [668433312678674432, 421674740751532032, 698984669622042645,
                                              665400023491674112, 686580674135719948, 668439280573612052,
                                              326741192739913728, 687997488204087396, 614397835705712651,
                                              589380212962230283, 736172855280140429, 576802484773715969,
                                              523678876686090260, 676076916813463553, 523142685205463050,
                                              368074547150454792, 516046250538434578, 414947776586186765,
                                              609561458811863076, 363032621845839892, 468054964615512084,
                                              614863681351712781, 668372877510443009, 701801263930671145,
                                              611228472911724583, 574902915391684608, 381412006969868290,
                                              673508187302920192, 488936383902384129, 686580275957727269,
                                              595625719451877376, 588029745745231937, 695600188617916446,
                                              668433882743308307, 671650108391030784, 333511394010071051,
                                              670962542025375744, 586782561745764354, 364785331163234304,
                                              375534189162004482, 686492852737540116, 563048784569827347]

                            for num in range(pp):
                                if not reac_user[num] == buyer_id:
                                    if reac_user[num] in cama_member:
                                        cama_list.append('<@' + str(reac_user[num]) + '>')
                                        cama_num = cama_num + 1
                                    elif reac_user[num] in ten_member:
                                        ten_list.append('<@' + str(reac_user[num]) + '>')
                                        ten_num = ten_num + 1
                                    elif reac_user[num] in samurai_member:
                                        samurai_list.append('<@' + str(reac_user[num]) + '>')
                                        samurai_num = samurai_num + 1
                            cama_list = '\n'.join(cama_list)
                            ten_list = '\n'.join(ten_list)
                            samurai_list = '\n'.join(samurai_list)
                            await dist_channel.send(
                                str(rbun_id) + 'の' + str(boss) + '/' + str(
                                    items) + ' が' + str(
                                    dia) + ' diaで売れました。\n25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。')
                            if cama_num == 0:
                                cama_bun_total = 0
                            else:
                                cama_bun_total = bunpd * cama_num
                            if ten_num == 0:
                                ten_bun_total = 0
                            else:
                                ten_bun_total = bunpd * ten_num
                            if samurai_num == 0:
                                samurai_bun_total = 0
                            else:
                                samurai_bun_total = bunpd * samurai_num
                            await dist_channel.send(
                                '<@477504935727071232>さんに' + str(math.floor(cama_bun_total)) + ' dia を渡してください。')
                            await dist_channel.send(
                                '<@363032621845839892>さんに' + str(math.floor(samurai_bun_total)) + ' dia を渡してください。')
                            await dist_channel.send(
                                '<@477111013590695936>さんに' + str(math.floor(ten_bun_total)) + ' dia を渡してください。')
                            cama_bun_total = cama_bun_total * 0.95
                            ten_bun_total = ten_bun_total * 0.95
                            samurai_bun_total = samurai_bun_total * 0.95
                            await dist_channel.send('以下に分配対象者を列挙しますので、別のコマンド入力はやめてください。')

                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                            if cama_num >= 10:
                                cama_ketsu = cama_bun_total * 0.03
                                cama_bun = (cama_bun_total - cama_ketsu) / cama_num
                                await dist_channel.send('<@477504935727071232>さんは以下の方々に' + str(
                                    math.floor(cama_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                    math.floor(cama_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(cama_list))

                                if ten_num >= 10:
                                    ten_ketsu = ten_bun_total * 0.03
                                    ten_bun = (ten_bun_total - ten_ketsu) / ten_num
                                    await dist_channel.send('<@477111013590695936>さんは以下の方々に' + str(
                                        math.floor(ten_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                        math.floor(ten_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(ten_list))

                                    if samurai_num >= 10:
                                        samurai_ketsu = samurai_bun_total * 0.03
                                        samurai_bun = (samurai_bun_total - samurai_ketsu) / samurai_num
                                        await dist_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                            math.floor(samurai_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                            math.floor(samurai_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(
                                            samurai_list))
                                    else:
                                        samurai_bun_total = bunpd * samurai_num
                                        samurai_bun = samurai_bun_total / samurai_num
                                        await dist_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                            math.floor(samurai_bun)) + ' dia を渡してください。\n' + str(samurai_list))
                                else:
                                    ten_bun_total = bunpd * ten_num
                                    ten_bun = ten_bun_total / ten_num
                                    await dist_channel.send('<@477111013590695936>さんは以下の方々に' + str(
                                        math.floor(ten_bun)) + ' dia を渡してください。\n' + str(ten_list))
                                    if samurai_num >= 10:
                                        samurai_ketsu = samurai_bun_total * 0.03
                                        samurai_bun = (samurai_bun_total - samurai_ketsu) / samurai_num
                                        await dist_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                            math.floor(samurai_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                            math.floor(samurai_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(
                                            samurai_list))
                                    else:
                                        samurai_bun_total = bunpd * samurai_num
                                        samurai_bun = samurai_bun_total / samurai_num
                                        await dist_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                            math.floor(samurai_bun)) + ' dia を渡してください。\n' + str(samurai_list))
                            else:
                                cama_bun_total = bunpd * cama_num
                                cama_bun = cama_bun_total / cama_num
                                await dist_channel.send(
                                    '<@477504935727071232>さんに' + str(math.floor(cama_bun_total)) + ' dia を渡してください。')
                                await dist_channel.send('<@477504935727071232>さんは以下の方々に' + str(
                                    math.floor(cama_bun)) + ' dia を渡してください。\n' + str(cama_list))
                                if ten_num >= 10:
                                    ten_ketsu = ten_bun_total * 0.03
                                    ten_bun = (ten_bun_total - ten_ketsu) / ten_num
                                    await dist_channel.send('<@477111013590695936>さんは以下の方々に' + str(
                                        math.floor(ten_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                        math.floor(ten_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(ten_list))

                                    if samurai_num >= 10:
                                        samurai_ketsu = samurai_bun_total * 0.03
                                        samurai_bun = (samurai_bun_total - samurai_ketsu) / samurai_num
                                        await dist_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                            math.floor(samurai_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                            math.floor(samurai_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(
                                            samurai_list))
                                    else:
                                        samurai_bun_total = bunpd * samurai_num
                                        samurai_bun = samurai_bun_total / samurai_num
                                        await dist_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                            math.floor(samurai_bun)) + ' dia を渡してください。\n' + str(samurai_list))
                                else:
                                    ten_bun_total = bunpd * ten_num
                                    ten_bun = ten_bun_total / ten_num
                                    await dist_channel.send('<@477111013590695936>さんは以下の方々に' + str(
                                        math.floor(ten_bun)) + ' dia を渡してください。\n' + str(ten_list))
                                    if samurai_num >= 10:
                                        samurai_ketsu = samurai_bun_total * 0.03
                                        samurai_bun = (samurai_bun_total - samurai_ketsu) / samurai_num
                                        await dist_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                            math.floor(samurai_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                            math.floor(samurai_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(
                                            samurai_list))
                                    else:
                                        samurai_bun_total = bunpd * samurai_num
                                        samurai_bun = samurai_bun_total / samurai_num
                                        await dist_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                            math.floor(samurai_bun)) + ' dia を渡してください。\n' + str(samurai_list))
                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                            await dist_channel.send('finish!')
                    else:
                        await dist_channel.send('えろてろまで問い合わせを。')


    #########高額レア販売システム#########
    elif message.content.startswith('sell1'):
        #        if not message.channel.id == 363032621845839892 or message.channel.id == 689731790935425034:
        #            return
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_rare')
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('k01_ID_LIST')
        worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
        id_count = worksheet_id.cell(6, 8).value

        await sell_channel.send('初回販売品\n参加者50% OFF, 未参加者20% OFF\n')
        for num in range(int(id_count)):
            sell_row = 3 + num
            count_checker = worksheet_sell.cell(sell_row, 8).value
            if int(count_checker) == 1:
                id = worksheet_sell.cell(sell_row, 1).value
                date = worksheet_sell.cell(sell_row, 6).value
                item = worksheet_sell.cell(sell_row, 3).value
                owner = worksheet_sell.cell(sell_row, 5).value
                price = worksheet_sell.cell(sell_row, 7).value
                sellm = discord.Embed(title='" ' + str(id) + ' : ' + str(item),
                                      description='Date: ' + str(date) + '\nOwner: ' + str(owner) + '\nPrice: ' + str(
                                          price), color=discord.Colour.red())
                msg = await sell_channel.send(embed=sellm)
                emoji1 = '\U0001F947'
                await msg.add_reaction(emoji1)
                worksheet_sell.update_cell(sell_row, 9, str(msg.id))
                await sell_channel.send('-------------------------------')
        await sell_channel.send('====================')

    elif message.content.startswith('sell2'):
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
        id_count = worksheet_id.cell(6, 8).value
        await sell_channel.send('====================')
        await sell_channel.send('第二回販売品\n参加者、未参加者共に50%OFF\n')
        for num in range(int(id_count)):

            sell_row = 3 + num
            count_checker = worksheet_sell.cell(sell_row, 8).value
            if int(count_checker) == 2:
                id = worksheet_sell.cell(sell_row, 1).value
                date = worksheet_sell.cell(sell_row, 6).value
                item = worksheet_sell.cell(sell_row, 3).value
                owner = worksheet_sell.cell(sell_row, 5).value
                price = worksheet_sell.cell(sell_row, 7).value
                sellm = discord.Embed(title='" ' + str(id) + ' : ' + str(item),
                                      description='Date: ' + str(date) + '\nOwner: ' + str(owner) + '\nPrice: ' + str(
                                          price), color=discord.Colour.red())
                msg = await sell_channel.send(embed=sellm)
                emoji1 = '\U0001F947'
                await msg.add_reaction(emoji1)
                worksheet_sell.update_cell(sell_row, 9, str(msg.id))
                await sell_channel.send('-------------------------------')
        await sell_channel.send('====================')

    elif message.content.startswith('sell3'):
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
        id_count = worksheet_id.cell(6, 8).value
        await sell_channel.send('第三回販売品\n参加者、未参加者共に50%OFF\n購入制限無し（購入制限中の方でも購入可）\n')
        for num in range(int(id_count)):
            sell_row = 3 + num
            count_checker = worksheet_sell.cell(sell_row, 8).value
            if int(count_checker) == 3:
                id = worksheet_sell.cell(sell_row, 1).value
                date = worksheet_sell.cell(sell_row, 6).value
                item = worksheet_sell.cell(sell_row, 3).value
                owner = worksheet_sell.cell(sell_row, 5).value
                price = worksheet_sell.cell(sell_row, 7).value
                sellm = discord.Embed(title='" ' + str(id) + ' : ' + str(item),
                                      description='Date: ' + str(date) + '\nOwner: ' + str(owner) + '\nPrice: ' + str(
                                          price), color=discord.Colour.red())
                msg = await sell_channel.send(embed=sellm)
                emoji1 = '\U0001F947'
                await msg.add_reaction(emoji1)
                worksheet_sell.update_cell(sell_row, 9, str(msg.id))
                await sell_channel.send('-------------------------------')
        await sell_channel.send('====================')

    elif message.content.startswith('sell4'):
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
        id_count = worksheet_id.cell(6, 8).value
        await sell_channel.send(
            '第四回販売品\n参加者、未参加者共に50%OFF\n購入制限無し（購入制限中の方でも購入可）\n赤レア制限の範囲外（第四回販売から購入しても、次回の赤レア購入に制限がかかりません）\n初回～第三回の販売とリアクション並行可（ただし、落札時には他メンバー優先）')
        for num in range(int(id_count)):
            sell_row = 3 + num
            count_checker = worksheet_sell.cell(sell_row, 8).value
            if int(count_checker) == 4:
                id = worksheet_sell.cell(sell_row, 1).value
                date = worksheet_sell.cell(sell_row, 6).value
                item = worksheet_sell.cell(sell_row, 3).value
                owner = worksheet_sell.cell(sell_row, 5).value
                price = worksheet_sell.cell(sell_row, 7).value
                sellm = discord.Embed(title='" ' + str(id) + ' : ' + str(item),
                                      description='Date: ' + str(date) + '\nOwner: ' + str(owner) + '\nPrice: ' + str(
                                          price), color=discord.Colour.red())
                msg = await sell_channel.send(embed=sellm)
                emoji1 = '\U0001F947'
                await msg.add_reaction(emoji1)
                worksheet_sell.update_cell(sell_row, 9, str(msg.id))
                await sell_channel.send('-------------------------------')

        await sell_channel.send('<@everyone>購入希望者はリアクションよろしく！')

    elif message.content.startswith('soldout'):
        if not message.author.id == 363032621845839892:
            if not message.author.id == 689731790935425034:
                return
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
        id_count = worksheet_id.cell(6, 8).value
        count1 = worksheet_id.cell(7, 8).value
        count2 = worksheet_id.cell(7, 9).value
        count3 = worksheet_id.cell(7, 10).value
        count4 = worksheet_id.cell(7, 11).value
        sell1_counter = 0
        sell2_counter = 0
        sell3_counter = 0
        sell4_counter = 0
        await sell_channel.send('購入者が確定しました。以下一覧を参照の上、購入者は取引を開始して下さい。\nこれから読み込みますのでコマンドを打たずに少々お待ちください。')
        sell1_list = list()
        sell2_list = list()
        sell3_list = list()
        sell4_list = list()
        sell1_2_list = list()
        sell2_2_list = list()
        sell3_2_list = list()
        sell4_2_list = list()
        sell1_3_list = list()
        sell2_3_list = list()
        sell3_3_list = list()
        sell4_3_list = list()
        par_read = 0
        par_msg = await sell_channel.send('progress...' + str(par_read) + '%')
        await asyncio.sleep(1)
        for num in range(int(id_count)):
            par_read = int(num) / int(id_count) * 100
            await par_msg.edit(content='progress...' + str(math.floor(par_read)) + '%')
            sell_row = 3 + num
            entry_msg_id = str(worksheet_sell.cell(sell_row, 9).value)    # BOTのメッセージIDを格納
            entry_msg = await sell_channel.fetch_message(entry_msg_id)  # BOTのメッセージ情報を格納
            uid_count = int(entry_msg.reactions[0].count)
            if uid_count == 1:
                id = worksheet_sell.cell(sell_row, 1).value
                item = worksheet_sell.cell(sell_row, 3).value
                price = worksheet_sell.cell(sell_row, 7).value
                sell_num = worksheet_sell.cell(sell_row, 8).value
                sell_num = int(sell_num)
                owner = worksheet_sell.cell(sell_row, 5).value
                await asyncio.sleep(4)

                if sell_num == 1:
                    if sell1_counter <= 10:
                        sell1_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell1_counter = sell1_counter + 1
                    elif 11 <= sell1_counter < 21:
                        sell1_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell1_counter = sell1_counter + 1
                    elif 21 <= sell1_counter:
                        sell1_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell1_counter = sell1_counter + 1
                    else:
                        sell_channel.send('sell1の'+sell1_counter+'でエラーがおきてるー！')
                        return
                elif sell_num == 2:
                    if sell2_counter <= 10:
                        sell2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell2_counter = sell2_counter + 1
                    elif 11 <= sell2_counter < 21:
                        sell2_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell2_counter = sell2_counter + 1
                    elif 21 <= sell2_counter:
                        sell2_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell2_counter = sell2_counter + 1
                    else:
                        sell_channel.send('sell2の'+sell2_counter+'でエラーがおきてるー！')
                        return
                elif sell_num == 3:
                    if sell3_counter <= 10:
                        sell3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell3_counter = sell3_counter + 1
                    elif 11 <= sell3_counter < 21:
                        sell3_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell3_counter = sell3_counter + 1
                    elif 21 <= sell3_counter:
                        sell3_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell3_counter = sell3_counter + 1
                    else:
                        sell_channel.send('sell3の'+sell3_counter+'でエラーがおきてるー！')
                        return
                elif sell_num == 4:
                    if sell4_counter <= 10:
                        sell4_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell4_counter = sell4_counter + 1
                    elif 11 <= sell4_counter < 21:
                        sell4_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell4_counter = sell4_counter + 1
                    elif 21 <= sell4_counter:
                        sell4_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : -')
                        sell4_counter = sell4_counter + 1
                    else:
                        sell_channel.send('sell4の'+sell4_counter+'でエラーがおきてるー！')
                        return
                else:
                    await sell_channel.send('エラー発生。えろてろへ連絡を。')
            elif uid_count >= 2:
                reac_users = await entry_msg.reactions[0].users().flatten()  # botのメッセージ情報からリアクションユーザー情報を格納。
                reac_user = list()
                for num in range(int(uid_count)):    #ユーザーIDだけ抽出
                    reac_user.append(reac_users[num].id)
                reac_user.remove(754892023613620316)  # bot idをリアクション情報から削除
                uid_count = int(len(reac_user))
                if int(uid_count) == 1:
                    id = worksheet_sell.cell(sell_row, 1).value
                    item = worksheet_sell.cell(sell_row, 3).value
                    buyer = str(reac_user[0])
                    price = worksheet_sell.cell(sell_row, 7).value
                    sell_num = int(worksheet_sell.cell(sell_row, 8).value)
                    owner = worksheet_sell.cell(sell_row, 5).value
                    serch_id = worksheet_find.find(id)
                    worksheet_find.update_cell(serch_id.row, 11, str(buyer))
                    await asyncio.sleep(4)

                    if sell_num == 1:
                        if sell1_counter <= 10:
                            sell1_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell1_counter = sell1_counter + 1
                        elif 11 <= sell1_counter < 21:
                            sell1_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell1_counter = sell1_counter + 1
                        elif 21 <= sell1_counter:
                            sell1_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell1_counter = sell1_counter + 1
                        else:
                            sell_channel.send('sell1の'+sell1_counter+'でエラーがおきてるー！')
                            return
                    elif sell_num == 2:
                        if sell2_counter <= 10:
                            sell2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell2_counter = sell2_counter + 1
                        elif 11 <= sell2_counter < 21:
                            sell2_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell2_counter = sell2_counter + 1
                        elif 21 <= sell2_counter:
                            sell2_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell2_counter = sell2_counter + 1
                            sell_channel.send('sell2の'+sell2_counter+'でエラーがおきてるー！')
                            return
                    elif sell_num == 3:
                        if sell3_counter <= 10:
                            sell3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell3_counter = sell3_counter + 1
                        elif 11 <= sell3_counter < 21:
                            sell3_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell3_counter = sell3_counter + 1
                        elif 21 <= sell3_counter:
                            sell3_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell3_counter = sell3_counter + 1
                        else:
                            sell_channel.send('sell3の'+sell3_counter+'でエラーがおきてるー！')
                            return
                    elif sell_num == 4:
                        if sell4_counter <= 10:
                            sell4_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell4_counter = sell4_counter + 1
                        elif 11 <= sell4_counter < 21:
                            sell4_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell4_counter = sell4_counter + 1
                        elif 21 <= sell4_counter:
                            sell4_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell4_counter = sell4_counter + 1
                        else:
                            sell_channel.send('sell4の'+sell4_counter+'でエラーがおきてるー！')
                            return

                elif int(uid_count) >= 2:
                    print(str(sell_row))
                    id = worksheet_sell.cell(sell_row, 1).value
                    item = worksheet_sell.cell(sell_row, 3).value
                    buyer = str(random.choice(reac_user))
                    price = worksheet_sell.cell(sell_row, 7).value
                    sell_num = int(worksheet_sell.cell(sell_row, 8).value)
                    owner = worksheet_sell.cell(sell_row, 5).value
                    serch_id = worksheet_find.find(id)
                    worksheet_find.update_cell(serch_id.row, 11, str(buyer))
                    await asyncio.sleep(4)

                    if sell_num == 1:
                        if sell1_counter <= 10:
                            sell1_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell1_counter = sell1_counter + 1
                        elif 11 <= sell1_counter < 21:
                            sell1_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell1_counter = sell1_counter + 1
                        elif 21 <= sell1_counter:
                            sell1_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell1_counter = sell1_counter + 1
                        else:
                            sell_channel.send('sell1の'+sell1_counter+'でエラーがおきてるー！')
                            return
                    elif sell_num == 2:
                        if sell2_counter <= 10:
                            sell2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell2_counter = sell2_counter + 1
                        elif 11 <= sell2_counter < 21:
                            sell2_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell2_counter = sell2_counter + 1
                        elif 21 <= sell2_counter:
                            sell2_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell2_counter = sell2_counter + 1
                            sell_channel.send('sell2の'+sell2_counter+'でエラーがおきてるー！')
                            return
                    elif sell_num == 3:
                        if sell3_counter <= 10:
                            sell3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell3_counter = sell3_counter + 1
                        elif 11 <= sell3_counter < 21:
                            sell3_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell3_counter = sell3_counter + 1
                        elif 21 <= sell3_counter:
                            sell3_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell3_counter = sell3_counter + 1
                        else:
                            sell_channel.send('sell3の'+sell3_counter+'でエラーがおきてるー！')
                            return
                    elif sell_num == 4:
                        if sell4_counter <= 10:
                            sell4_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell4_counter = sell4_counter + 1
                        elif 11 <= sell4_counter < 21:
                            sell4_2_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell4_counter = sell4_counter + 1
                        elif 21 <= sell4_counter:
                            sell4_3_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                            sell4_counter = sell4_counter + 1
                        else:
                            sell_channel.send('sell4の'+sell4_counter+'でエラーがおきてるー！')
                            return

        sell1_list = '\n-\n'.join(sell1_list)
        sell2_list = '\n-\n'.join(sell2_list)
        sell3_list = '\n-\n'.join(sell3_list)
        sell4_list = '\n-\n'.join(sell4_list)
        sell1_2_list = '\n-\n'.join(sell1_2_list)
        sell2_2_list = '\n-\n'.join(sell2_2_list)
        sell3_2_list = '\n-\n'.join(sell3_2_list)
        sell4_2_list = '\n-\n'.join(sell4_2_list)
        sell1_3_list = '\n-\n'.join(sell1_3_list)
        sell2_3_list = '\n-\n'.join(sell2_3_list)
        sell3_3_list = '\n-\n'.join(sell3_3_list)
        sell4_3_list = '\n-\n'.join(sell4_3_list)
        
        await par_msg.edit(content='progress...100%')
        sell1_r = discord.Embed(title='第1回販売結果',
                                description='以下の方々は取引を開始して下さい。',
                                color=discord.Colour.red())
        sell1_r.add_field(name='-', value=str(sell1_list), inline=True)
        await sell_channel.send(embed=sell1_r)
        if 11 <= sell1_counter:
            sell1_2_r = discord.Embed(title='第1回販売結果(続き)',
                                      description='以下の方々は取引を開始して下さい。',
                                      color=discord.Colour.red())
            sell1_2_r.add_field(name='-', value=str(sell1_2_list), inline=True)
            await sell_channel.send(embed=sell1_2_r)
            if 21 <= sell1_counter:
                sell1_3_r = discord.Embed(title='第1回販売結果(続き)',
                                          description='以下の方々は取引を開始して下さい。',
                                          color=discord.Colour.red())
                sell1_3_r.add_field(name='-', value=str(sell1_3_list), inline=True)
                await sell_channel.send(embed=sell1_3_r)

        sell2_r = discord.Embed(title='第2回販売結果',
                                description='以下の方々は取引を開始して下さい。',
                                color=discord.Colour.red())
        sell2_r.add_field(name='-', value=str(sell2_list), inline=True)

        await sell_channel.send(embed=sell2_r)
        if 11 <= sell2_counter:
            sell2_2_r = discord.Embed(title='第2回販売結果(続き)',
                                      description='以下の方々は取引を開始して下さい。',
                                      color=discord.Colour.red())
            sell2_2_r.add_field(name='-', value=str(sell2_2_list), inline=True)
            await sell_channel.send(embed=sell2_2_r)
            if 21 <= sell2_counter:
                sell2_3_r = discord.Embed(title='第2回販売結果(続き)',
                                          description='以下の方々は取引を開始して下さい。',
                                          color=discord.Colour.red())
                sell2_3_r.add_field(name='-', value=str(sell2_3_list), inline=True)
                await sell_channel.send(embed=sell2_3_r)
                
                
        sell3_r = discord.Embed(title='第3回販売結果',
                                description='以下の方々は取引を開始して下さい。',
                                color=discord.Colour.red())
        sell3_r.add_field(name='-', value=str(sell3_list), inline=True)
        await sell_channel.send(embed=sell3_r)
        if 11 <= sell3_counter:
            sell3_2_r = discord.Embed(title='第3回販売結果(続き)',
                                      description='以下の方々は取引を開始して下さい。',
                                      color=discord.Colour.red())
            sell3_2_r.add_field(name='-', value=str(sell3_2_list), inline=True)
            await sell_channel.send(embed=sell3_2_r)
            if 21 <= sell3_counter:
                sell3_3_r = discord.Embed(title='第3回販売結果(続き)',
                                          description='以下の方々は取引を開始して下さい。',
                                          color=discord.Colour.red())
                sell3_3_r.add_field(name='-', value=str(sell3_3_list), inline=True)
                await sell_channel.send(embed=sell3_3_r)

        sell4_r = discord.Embed(title='第4回販売結果',
                                description='以下の方々は取引を開始して下さい。',
                                color=discord.Colour.red())
        sell4_r.add_field(name='-', value=str(sell4_list), inline=True)
        await sell_channel.send(embed=sell4_r)
        if 11 <= sell4_counter:
            sell4_2_r = discord.Embed(title='第4回販売結果(続き)',
                                      description='以下の方々は取引を開始して下さい。',
                                      color=discord.Colour.red())
            sell4_2_r.add_field(name='-', value=str(sell4_2_list), inline=True)
            await sell_channel.send(embed=sell4_2_r)
            if 21 <= sell4_counter:
                sell4_3_r = discord.Embed(title='第4回販売結果(続き)',
                                          description='以下の方々は取引を開始して下さい。',
                                          color=discord.Colour.red())
                sell4_3_r.add_field(name='-', value=str(sell4_3_list), inline=True)
                await sell_channel.send(embed=sell4_3_r)
        await sell_channel.send('finish')
        
                # *****************以下はじゃんけんBOT*******************
    global result, judge
    if message.content == '！じゃんけん':
        if message.author.id == 591281241798737938:
            saruji = random.choice(('？', '遊んどらんで金返せや', '最初はパー！私の勝ち！100dia払って＾＾'))
            await wai_channel.send(str(saruji))
            return

        else:
            await message.channel.send("最初はぐー、じゃんけん")

            jkbot = random.choice(("ぐー", "ちょき", "ぱー"))
            draw = str(jkbot) + "！引き分けだよ～"
            wn = str(jkbot) + "･･･君の勝ち！"
            lst = random.choice((str(jkbot) + 'だよ！私の勝ち！弱ｗｗｗｗｗｗｗｗｗｗｗｗやめたら？じゃんけん',
                                 str(jkbot) + 'だから私の勝ちだね(∩´∀｀)∩、また挑戦してね！'))

        def jankencheck(m):
            return (m.author == message.author) and (m.content in ['ぐー', 'ちょき', 'ぱー'])

        reply = await client.wait_for("message", check=jankencheck)
        if reply.content == jkbot:
            judge = draw
        else:
            if reply.content == "ぐー":
                if jkbot == "ちょき":
                    judge = wn
                else:
                    judge = lst

            elif reply.content == "ちょき":
                if jkbot == "ぱー":
                    judge = wn
                else:
                    judge = lst

            else:
                if jkbot == "ぐー":
                    judge = wn
                else:
                    judge = lst

        await message.channel.send(judge)

client.run(TOKEN)


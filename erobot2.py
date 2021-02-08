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
import sys
import discord.user
import discord.reaction

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
async def on_raw_reaction_add(payload):
    regi_channel = client.get_channel(744727455293767711)
    culc_channel = client.get_channel(740355050182017135)  # 本番用
    drop_regi_channel = client.get_channel(798521158302826525)
    sell_channel = client.get_channel(722845189961416786)

    if payload.user_id == 689736979075825706:
        return
    elif payload.user_id == 754892023613620316:
        return

    elif payload.channel_id == 732658643740262553:
        channel = client.get_channel(722253361159864479)
        now = dt.now()
        now1 = str(now)
        await channel.send(
            'Date&Time:\n' + now1 + '\nmessage channel & id\n' + str(payload.channel_id) + '\nmessage-id\n' + str(
                payload.message_id) + '\nreaction-user-id\r\n' + str(payload.user_id) + '\n_')

    elif payload.channel_id == 744727455293767711:
        print(payload.user_id)
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        embed_msg = await regi_channel.fetch_message(payload.message_id)
        m_id = embed_msg.embeds[0].description.split()
        regi_mid = str(m_id[1])
        if m_id[0] =='MSG-ID:':
            uid_msg1 = await drop_regi_channel.fetch_message(regi_mid)
            uid_msg0 = uid_msg1.content.split()
            if str(payload.user_id) in str(uid_msg0):
                return
            else:
                await uid_msg1.edit(content=str(uid_msg1.content) + ' ' + str(payload.user_id))
                await payload.member.send('新しい機能で登録しました。お知らせ機能は今後削除予定です。')
        else:
            search_mid = payload.message_id
            mid_cell = worksheet_find.find(str(search_mid))
            entry1_id = worksheet_find.cell(mid_cell.row, 12).value
            if str(entry1_id) == str(payload.user_id):
                msg = await regi_channel.send(
                    '拾得者（登録した人）はリアクションは不要なので解除して下さい。\n他に修正が必要な場合は"えろてろ"までご連絡をお願いします。\n本メッセージは10秒後に自動で削除されます。')
                await asyncio.sleep(3)
                await msg.delete()
            else:
                entry_num = worksheet_find.cell(mid_cell.row, 166).value
                entry_col = int(entry_num) + int(12)
                worksheet_find.update_cell(mid_cell.row, int(entry_col), str(payload.user_id))
                entry_idnum = worksheet_find.cell(mid_cell.row, 1).value
                await payload.member.send(str(entry_idnum) + 'に参加登録しました。間違えていたら管理者へ連絡下さい。')

    elif payload.channel_id == 740355050182017135:
        msg_id = payload.message_id
        #        test_channel = client.get_channel(722253470023024640)
        msg = await culc_channel.fetch_message(msg_id)
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
#                await msg.clear_reactions()
            else:
                # print('りたーん！')
                return
        else:
            #            print('えろぼっと以外へのリアクション！')
            return
    elif payload.channel_id == 722845189961416786:
        aut_msg = await sell_channel.fetch_message(payload.message_id)
        if aut_msg.author == client.user:
            return
        else:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
            search_mid = payload.message_id
            mid_cell = worksheet_sell.find(str(search_mid))
            entry_num = worksheet_sell.cell(mid_cell.row, 10).value
            entry_col = int(entry_num) + int(11)
            worksheet_sell.update_cell(mid_cell.row, int(entry_col), str(payload.user_id))

    else:
        return


@client.event
async def on_raw_reaction_remove(payload):
    regi_channel = client.get_channel(744727455293767711)
    culc_channel = client.get_channel(740355050182017135)  # 本番用
    drop_regi_channel = client.get_channel(798521158302826525)

    if payload.user_id == 689736979075825706:
        return
    elif payload.user_id == 754892023613620316:
        return

    elif payload.channel_id == 732658643740262553:
        channel = client.get_channel(722253361159864479)
        now2 = dt.now()
        now3 = str(now2)
        await channel.send(
            'Date&Time:\n' + now3 + '\nmessage channel\n' + str(payload.channel_id) + '\nmessage-id\n' + str(
                payload.message_id) + '\nreaction-user-id\r\n' + str(payload.user_id) + 'del\n_')

    elif payload.channel_id == 744727455293767711:
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        embed_msg = await regi_channel.fetch_message(payload.message_id)
        m_id = embed_msg.embeds[0].description.split()
        regi_mid = str(m_id[1])
        if m_id[0] =='MSG-ID:':
            uid_msg1 = await drop_regi_channel.fetch_message(regi_mid)
            uid_msg0 = uid_msg1.content.split()
            if str(payload.user_id) == str(uid_msg0[1]):
                return
            else:
                uid_msg2 = uid_msg1.content.replace(str(payload.user_id), '')
                await uid_msg1.edit(content=str(uid_msg2))
                await payload.member.send('新しい機能で登録を削除しました。お知らせ機能は今後削除予定です。')

        else:
            search_mid = payload.message_id
            mid_cell = worksheet_find.find(str(search_mid))
            #msg_id = worksheet_find.cell(mid_cell.row, 13).value
            col_list = worksheet_find.row_values(mid_cell.row)
            entry_num = worksheet_find.cell(mid_cell.row, 166).value
            entry1_id = worksheet_find.cell(mid_cell.row, 12).value
            del_col = int(col_list.index(str(payload.user_id))) + int(1)
            if str(entry1_id) == str(payload.user_id):
                # print('同じだよ')
                return
            elif entry_num == 1:
                worksheet_find.update_cell(mid_cell.row, int(del_col), str(''))
                return
            else:
                enum = int(del_col) - int(12)
                entry = int(entry_num) - int(enum)
                del_col2 = del_col
                for num in range(1, int(entry)):
                    right_col = int(del_col2) + 1
                    up_id = worksheet_find.cell(mid_cell.row, int(right_col)).value
                    worksheet_find.update_cell(mid_cell.row, int(del_col2), up_id)
                    del_col2 = del_col + num
                worksheet_find.update_cell(mid_cell.row, int(del_col2), str(''))



    elif payload.channel_id == 722845189961416786:
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
        search_mid = payload.message_id
        mid_cell = worksheet_sell.find(str(search_mid))
        col_list = worksheet_sell.row_values(mid_cell.row)
        entry_num = worksheet_sell.cell(mid_cell.row, 10).value
        del_col = int(col_list.index(str(payload.user_id))) + int(1)
        if entry_num == 1:
            worksheet_sell.update_cell(mid_cell.row, int(del_col), str(''))
            return
        else:
            enum = int(del_col) - int(10)
            entry = int(entry_num) - int(enum)
            del_col2 = del_col
            for num in range(1, int(entry)):
                if not num == int(entry):
                    right_col = int(del_col2) + 1
                    up_id = worksheet_sell.cell(mid_cell.row, int(right_col)).value
                    worksheet_sell.update_cell(mid_cell.row, int(del_col2), up_id)
                del_col2 = del_col + num
            worksheet_sell.update_cell(mid_cell.row, int(del_col2), str(''))
    else:
        return

    # elif payload.channel_id == 722253470023024640:
    #     msg_id = payload.message_id
    #     test_channel = client.get_channel(722253470023024640)
    #     msg = await test_channel.fetch_message(msg_id)
    #     msg1 = discord.utils.escape_markdown(msg.content)
    #     print(msg1)
    #     msg1 = msg1.strip('\~')
    #     print(msg1)
    #     #msg1 = msg1.rstrip("~~")
    #     await msg.edit(content= msg1)


@client.event
async def on_message(message):
    culc_channel = client.get_channel(740355050182017135)  # 本番用
    wai_channel = client.get_channel(658468918243098626)  # 本番用
    ami_channel = client.get_channel(675359824803790850)
    list_channel = client.get_channel(743314066713477251)
    regi_channel = client.get_channel(744727455293767711)
    test_channel = client.get_channel(722253470023024640)
    sell_channel = client.get_channel(722845189961416786)
    drop_regi_channel = client.get_channel(798521158302826525)

    if message.author == client.user:
        return

    elif message.content.startswith('test'):
        if message.channel.id == 722253470023024640:
            await test_channel.send('<@592253165068615680>')

    elif message.content.startswith('!bun '):
        m_num = message.content.strip('!bun ')
        m_list = m_num.split()
        # 人数ppとdiaに分ける。
        pp = int(m_list[0])
        dia = int(m_list[1])

        if pp < 10 and dia < 5000:
            bunpa = dia / pp
            if bunpa < 50:
                dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                await culc_channel.send(
                    '分配が50dia未満(' + str(math.floor(bunpa)) + 'dia/人)なので、抽選を行います。\nリアクション表示の上から ' + str(
                        dice) + ' 番目の方に ' + str(dia) + ' diaを渡してください。\nリアクション表示と人数が異なる場合は別途抽選を行ってください。')
            else:
                await culc_channel.send(
                    '10人未満,5000dia未満なので以下となります。\n分配：' + str(math.floor(bunpa)) + 'dia\n血盟資金、分配者手数料はありません。')
                return

        elif pp < 10 and dia >= 5000:
            ketsu = dia * 0.03
            bunpb = (dia - ketsu * 3) / pp
            await culc_channel.send(
                '10人未満, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
                    math.floor(bunpb)) + 'diaになります。\n分配者手数料は１０人未満なのでありません。')
            return

        else:
            if 10 <= pp < 25 and dia >= 5000:
                ketsu = dia * 0.03
                tema = dia * 0.05
                if tema < 500:
                    bunpb = (dia - ketsu * 3 - tema) / pp
                    await culc_channel.send(
                        '10人以上, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
                            math.floor(bunpb)) + 'diaになります。\nちなみに手間賃は' + str(math.floor(tema)) + 'diaです。')
                    return
                elif tema >= 500:
                    tema = 500
                    bunpb = (dia - ketsu * 3 - tema) / pp
                    await culc_channel.send(
                        '10人以上, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
                            math.floor(bunpb)) + 'diaになります。\nちなみに手間賃は上限の' + str(math.floor(tema)) + 'diaです。')
                    return
                else:
                    await culc_channel.send('えろてろまで問い合わせを。')

            elif 10 <= pp < 25 and dia < 5000:
                tema = dia * 0.05
                bunpb = (dia - tema) / pp
                if bunpb < 50:
                    dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                    await culc_channel.send(
                        '分配が50dia未満(' + str(math.floor(bunpb)) + 'dia/人)なので、抽選を行います。\nリアクション表示の上から ' + str(
                            dice) + ' 番目の方に' + str(dia) + 'diaを渡してください。\nリアクション表示と人数が異なる場合は別途抽選を行ってください。')
                    return
                else:
                    await culc_channel.send(
                        '10人以上, 5000dia未満なので以下となります。\n分配：' + str(math.floor(bunpb)) + 'diaになります。\n分配者手数料は' + str(
                            math.floor(tema)) + 'diaです。\n血盟資金はありません。')
                    return

            else:
                if pp >= 25 and dia >= 5000:
                    ketsushi = dia * 0.03
                    bunpc = (dia - ketsushi * 3) / pp
                    if bunpc < 100:
                        meishubun1 = dia / 3
                        await culc_channel.send('25人以上 / 分配 100dia未満なので全額血盟資金となります。\n３等分した' + str(
                            math.floor(meishubun1)) + 'diaを各盟主に渡してください。\n分配者手数料、血盟資金はありません。')
                        return
                    else:
                        await culc_channel.send('25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。\n' + str(
                            math.floor(bunpc)) + ' × 各血盟の対象人数 + ' + str(
                            math.floor(ketsushi)) + 'dia(血盟資金）の合計を各盟主に渡してください。\n分配者手数料はありません。')
                        return
                elif pp >= 25 and dia < 5000:
                    bunpd = dia / pp
                    if bunpd < 100:
                        meishubun2 = dia / 3
                        await culc_channel.send('25人以上で分配が100dia/人 未満なので全額血盟資金となります。\n' + str(
                            math.floor(meishubun2)) + 'diaを各盟主に渡してください。\n分配者手数料、血盟資金はありません。')
                        return
                    else:
                        await culc_channel.send(
                            '25人以上で分配が100dia/人 以上なので以下に従って盟主と取引して下さい。\n今回は盟主が分配するため、血盟資金 + 各血盟の対象人数 × ' + str(
                                math.floor(bunpd)) + 'diaを各盟主に渡してください。\n分配者手数料はありません。')
                        return
                else:
                    await culc_channel.send('えろてろまで問い合わせを。')

    elif message.content.startswith('!dice '):
        if message.channel.id == 675359824803790850:
            rami_num = message.content.strip('!dice ')
            rami_list = rami_num.split()
            # 人数ppとdiaに分ける。
            rami_rand = int(rami_list[0])
            rami_dice = random.randint(1, rami_rand)  # サイコロを振る。出る目を指定。
            await ami_channel.send('抽選した結果、' + str(rami_dice) + ' 番が当選！オーメデトーゴーザイマース！')
            return
        return

    elif message.content.startswith('!nami '):
        if message.channel.id == 675359824803790850:
            nami_num = message.content.strip('!nami')
            nami_list = nami_num.split()
            nami_rand = random.choice(nami_list)
            await ami_channel.send('抽選した結果、' + str(nami_rand) + ' が当選！オーメデトーゴーザイマース！')
            return
        return

    elif message.content.startswith('ワイが'):
        if message.author.id == 591281241798737938:
            await wai_channel.send('アンタ誰や？下の板言うてないで狩りしーや？')
        else:
            #            await wai_channel.send(message.author.name + 'や。さるじやあらへん。\nあいつは今びっくり焼きを調べるのに夢中やで！')
            worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
            import_value = str(message.author.name + 'や。さるじやあらへん')

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

    # boss drop management bot. (!get(n or r) BossName DropItem)### n = normal, r = rare
    elif message.content.startswith('get '):
        if message.channel.id == 744727455293767711:
            drop_high_list = message.content.split()
            drop_high_boss = drop_high_list[1]
            drop_high_item = drop_high_list[2]
            today = dt.now()
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
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
            regi_msg = await drop_regi_channel.send('r' + str(id_no) + ' ' + (str(message.author.id)))
            #            worksheet_list.update_cell(input_id, 8, str(message.id))
            # worksheet_list.update_cell(input_id, 10, str('-'))
            # worksheet_list.update_cell(input_id, 11, str('-'))
            worksheet_list.update_cell(input_id, 12, str(message.author.id))
            # worksheet_list.update_cell(input_id, 13, str(regi_msg.id))
            worksheet_list.update_cell(input_id, 168, 1)

            drp = discord.Embed(title='ID: r' + str(id_no) + ' / " ' + str(drop_high_boss) + ' " / " ' + str(drop_high_item) + ' "\n拾得者:' + str(message.author.name), description='MSG-ID: ' + str(regi_msg.id) + ' \n参加者はリアクションして下さい。/Please reaction!', color=discord.Colour.red())
            #               await wai_channel.send(embed=grn)
            #await drop_id_channel.send(str(id_no) + ' ' + str(regi_msg.id))
            msg = await regi_channel.send(embed=drp)  # debag
            #               msg = await grn_channel.send(embed=grn)#本番
            emoji1 = '\U0001F947'
            await msg.add_reaction(emoji1)
            worksheet_list.update_cell(input_id, 8, str(msg.id))
            #await message.delete()
            return

    elif message.content.startswith('!getnnnnnnnnn '):
        if message.channel.id == 744727455293767711:
            drop_high_list = message.content.split()
            drop_high_boss = drop_high_list[1]
            drop_high_item = drop_high_list[2]
            today = dt.now()
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            id_total = worksheet_id.cell(4, 8).value
            id_num = worksheet_id.cell(4, 9).value
            input_id = int(id_total) + 2
            id_no = int(id_num) + 1
            worksheet_list.update_cell(input_id, 1, 'n' + str(id_no))  # id number
            worksheet_list.update_cell(input_id, 2, str(drop_high_boss))  # boss name
            worksheet_list.update_cell(input_id, 3, str(drop_high_item))  # item name
            worksheet_list.update_cell(input_id, 4, str('normal'))  # item grade
            worksheet_list.update_cell(input_id, 5, str(message.author.name))  # 記入者
            worksheet_list.update_cell(input_id, 6,
                                       str(today.year) + '/' + str(today.month) + '/' + str(today.day))  # 登録日
            worksheet_list.update_cell(input_id, 7, str('none'))
            #            worksheet_list.update_cell(input_id, 8, str(message.id))
            worksheet_list.update_cell(input_id, 10, str('-'))
            worksheet_list.update_cell(input_id, 11, str('-'))

            drp = discord.Embed(
                title='" ' + str(drop_high_boss) + ' " dropped " ' + str(drop_high_item) + ' "\nOwner(所有者):  ' + str(
                    message.author.name) + '\nAllocated ID: n' + str(id_no),
                description='Please reaction!',
                color=discord.Colour.red())
            #               await wai_channel.send(embed=grn)
            msg = await regi_channel.send(embed=drp)  # debag
            #               msg = await grn_channel.send(embed=grn)#本番
            emoji1 = '\U0001F947'
            await msg.add_reaction(emoji1)
            worksheet_list.update_cell(input_id, 8, str(msg.id))
            await message.delete()
            return

    elif message.content.startswith('!del '):
        if message.channel.id == 743314066713477251:
            if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
                worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
                del_list = message.content.split()
                del_cell = worksheet_find.findall(str(del_list[1]))
                del_id = worksheet_find.cell(del_cell[0].row, 1).value
                #                worksheet_find.update_cell(del_cell[0].row, 1, '')
                worksheet_find.update_cell(del_cell[0].row, 2, '-')
                worksheet_find.update_cell(del_cell[0].row, 3, '-')
                #                worksheet_find.update_cell(del_cell[0].row, 4, '')
                worksheet_find.update_cell(del_cell[0].row, 5, '-')
                worksheet_find.update_cell(del_cell[0].row, 6, '-')
                worksheet_find.update_cell(del_cell[0].row, 7, 'delete')
                worksheet_find.update_cell(del_cell[0].row, 10, '')
                worksheet_find.update_cell(del_cell[0].row, 11, '')
                del_p = int(worksheet_find.cell(del_cell[0].row, 166).value)
                for num in range(del_p):
                    num = num + int(12)
                    worksheet_find.update_cell(del_cell[0].row, num, '')
                await list_channel.send(del_id + 'を削除しました。')

    elif message.content.startswith('!back '):
        if message.channel.id == 743314066713477251:
            if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
                worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
                del_list = message.content.split()
                del_cell = worksheet_find.findall(str(del_list[1]))
                del_id = worksheet_find.cell(del_cell[0].row, 1).value
                worksheet_find.update_cell(del_cell[0].row, 7, 'none')
                worksheet_find.update_cell(del_cell[0].row, 10, '-')
                await list_channel.send(del_id + 'を未分配に戻しました。')

    elif message.content.startswith('!fin '):
        if message.channel.id == 743314066713477251:
            if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
                worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
                fin_list = message.content.split()
                fin_dia = fin_list[2]
                fin_cell = worksheet_find.findall(str(fin_list[1]))
                fin_id = worksheet_find.cell(fin_cell[0].row, 1).value
                worksheet_find.update_cell(fin_cell[0].row, 7, 'finish')
                worksheet_find.update_cell(fin_cell[0].row, 10, str(fin_dia))
                await list_channel.send(fin_id + 'を分配完了にしました。')


    elif message.content.startswith('!own_change '):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            che_list = message.content.split()
            che_cell = worksheet_find.findall(str(che_list[1]))
            worksheet_find.update_cell(che_cell[0].row, 5, str(che_list[2]))

    elif message.content.startswith('list'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            cell_list = worksheet_find.findall('none')
            # print(cell_list)
            deal_count = worksheet_id.cell(5, 8).value
            r_list = list()
            for num in range(int(deal_count)):
                get_id = worksheet_find.cell(cell_list[num].row, 1).value
                get_boss = worksheet_find.cell(cell_list[num].row, 2).value
                get_item = worksheet_find.cell(cell_list[num].row, 3).value
                get_name = worksheet_find.cell(cell_list[num].row, 5).value
                get_date = worksheet_find.cell(cell_list[num].row, 6).value
                r_list.append(get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
                await asyncio.sleep(4)
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


    elif message.content.startswith('!list r'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            cell_list = worksheet_find.findall('none')
            deal_count = worksheet_id.cell(5, 8).value
            r_list = list()
            for num in range(int(deal_count)):
                get_grade = worksheet_find.cell(cell_list[num].row, 4).value
                if get_grade == 'rare':
                    get_id = worksheet_find.cell(cell_list[num].row, 1).value
                    get_boss = worksheet_find.cell(cell_list[num].row, 2).value
                    get_item = worksheet_find.cell(cell_list[num].row, 3).value
                    get_name = worksheet_find.cell(cell_list[num].row, 5).value
                    get_date = worksheet_find.cell(cell_list[num].row, 6).value
                    r_list.append(
                        get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
            r_list = '\n'.join(r_list)
            get_r = discord.Embed(title='DROP ITEM LIST (GRADE: RARE)',
                                  description='ID \t:\t  boss \t/  item \t/  holder \t/  date',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(r_list), inline=True)
            await list_channel.send(embed=get_r)
            return

    elif message.content.startswith('!list n'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            cell_list = worksheet_find.findall('none')
            deal_count = worksheet_id.cell(5, 8).value
            r_list = list()
            for num in range(int(deal_count)):
                get_grade = worksheet_find.cell(cell_list[num].row, 4).value
                if get_grade == 'normal':
                    get_id = worksheet_find.cell(cell_list[num].row, 1).value
                    get_boss = worksheet_find.cell(cell_list[num].row, 2).value
                    get_item = worksheet_find.cell(cell_list[num].row, 3).value
                    get_name = worksheet_find.cell(cell_list[num].row, 5).value
                    get_date = worksheet_find.cell(cell_list[num].row, 6).value
                    r_list.append(
                        get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
            r_list = '\n'.join(r_list)
            get_r = discord.Embed(title='DROP ITEM LIST (GRADE: NORMAL)',
                                  description='ID \t:\t  boss \t/  item \t/  holder \t/  date',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(r_list), inline=True)
            await list_channel.send(embed=get_r)
            return

    elif message.content.startswith('mylist'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
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

    elif message.content.startswith('merolist'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            #            cell_list = worksheet_find.findall(str(message.author.name))
            cell_list = worksheet_find.findall(str('メロリンＱ'))
            # print(cell_list)
            deal_count = len(cell_list)
            if deal_count == 0:
                await list_channel.send('ご苦労様です。\n' + str(message.author.name) + ' さんの未分配案件はありません。')
                return
            r_list = list()
            # print(deal_count)
            for num in range(int(deal_count)):
                if worksheet_find.cell(cell_list[num].row, 7).value == 'none':
                    get_id = worksheet_find.cell(cell_list[num].row, 1).value
                    get_boss = worksheet_find.cell(cell_list[num].row, 2).value
                    get_item = worksheet_find.cell(cell_list[num].row, 3).value
                    get_name = worksheet_find.cell(cell_list[num].row, 5).value
                    get_date = worksheet_find.cell(cell_list[num].row, 6).value
                    r_list.append(
                        get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
                    await asyncio.sleep(2)
                else:
                    await asyncio.sleep(1)
                # print(r_list)
                # print(len(r_list))
                r_count = int(len(r_list))
                if r_count == 0:
                    await list_channel.send('ご苦労様です。\n' + str(message.author.name) + ' さんの未分配案件はありません。\n全て完了していました。')
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

    elif message.content.startswith('repo '):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            id_cell_list = message.content.split()
            id_cell = worksheet_find.findall(str(id_cell_list[1]))
            pp = worksheet_find.cell(id_cell[0].row, 166).value
            get_id = worksheet_find.cell(id_cell[0].row, 1).value
            get_boss = worksheet_find.cell(id_cell[0].row, 2).value
            get_item = worksheet_find.cell(id_cell[0].row, 3).value
            get_name = worksheet_find.cell(id_cell[0].row, 5).value
            get_date = worksheet_find.cell(id_cell[0].row, 6).value
            add_col = int(12)
            id_check = list()
            for num in range(int(pp)):
                id_col = int(num) + int(add_col)
                id_check.append('<@' + worksheet_find.cell(id_cell[0].row, id_col).value + '>\n')
            id_check = '\n'.join(id_check)
            drp = discord.Embed(
                title='ID: ' + str(get_id) + ' detail',
                description='BOSS: ' + str(get_boss) + ' / ITEM: ' + str(get_item) + '\nOWNER: ' + str(
                    get_name) + ' / DATA: ' + str(get_date) + '\nENTRY\n' + str(id_check),
                color=discord.Colour.red())
            msg = await list_channel.send(embed=drp)  # debag

    elif message.content.startswith('entry '):
        if message.channel.id == 743314066713477251:
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            rbun_list = message.content.split()
            rbun_id = rbun_list[1]
            id_cell = worksheet_list.find(str(rbun_id))
            pp = int(worksheet_list.cell(id_cell.row, 9).value)
            cama_num = 0
            death_num = 0
            samurai_num = 0
            cama_list = list()
            death_list = list()
            samurai_list = list()
            par_read = 0
            par_msg = await list_channel.send('Load progress...' + str(par_read) + '%')
            for num in range(pp):
                par_read = int(num) / int(pp) * 100
                await par_msg.edit(content='Load progress...' + str(math.floor(par_read)) + '%')
                id_col = int(num) + int(12)
                id_clan_posi = worksheet_id.find(str(worksheet_list.cell(id_cell.row, id_col).value))
                # print(id_clan_posi.col)
                await asyncio.sleep(3)

                if id_clan_posi.col == 13:
                    #   print('カマ')
                    cama_list.append('<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                    cama_num = cama_num + 1
                elif id_clan_posi.col == 16:
                    #   print('デス')
                    death_list.append('<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                    death_num = death_num + 1
                elif id_clan_posi.col == 19:
                    #   print('サムライ')
                    samurai_list.append(
                        '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                    samurai_num = samurai_num + 1
            cama_list = '\n'.join(cama_list)
            death_list = '\n'.join(death_list)
            samurai_list = '\n'.join(samurai_list)
            await par_msg.edit(content='Load progress...100%')

            get_r = discord.Embed(title=str(rbun_id) + ' : List of attendees(CAMA)',
                                  description='Please check below',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(cama_list),
                            inline=True)
            await list_channel.send(embed=get_r)

            get_r = discord.Embed(title=str(rbun_id) + ' : List of attendees(DEATH)',
                                  description='Please check below',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(death_list),
                            inline=True)
            await list_channel.send(embed=get_r)

            get_r = discord.Embed(title=str(rbun_id) + ' : List of attendees(SAMURAI)',
                                  description='Please check below',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(samurai_list),
                            inline=True)
            await list_channel.send(embed=get_r)


    elif message.content.startswith('bun '):
        await culc_channel.send('Please wait...')
        worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        rbun_list = message.content.split()
        rbun_id = rbun_list[1]
        rbun_dia = rbun_list[2]
        id_cell = worksheet_list.find(str(rbun_id))
        check_new = worksheet_list.cell(id_cell.row, 168).value
        entry_msg_id = worksheet_list.cell(id_cell.row, 8).value
        entry_msg = await regi_channel.fetch_message(entry_msg_id)
        reaction_num = int(entry_msg.reactions[0].count)
        del_buyer = 0
        if worksheet_list.cell(id_cell.row, 7).value == 'finish':
            await culc_channel.send('このID案件は分配案内が完了しています。\n変更したい方は えろてろ までご連絡おねがいします。')
            return
        else:
            buyer_check = worksheet_list.cell(id_cell.row, 167).value
            if check_new == str(1):
                desc_msg = entry_msg.embeds[0].description.split()
                pp_msg_id = desc_msg[1]
                et_msg = await drop_regi_channel.fetch_message(pp_msg_id)
                et_msg = et_msg.content.split()
                if buyer_check == str(1):
                    buyer_id = str(worksheet_list.cell(id_cell.row, 11).value)
                    et2_msg = et_msg.remove(buyer_id)
                    # msg_content = msg_content.replace(buyer_id, '')
                    # await et_msg.edit(content=msg_content)
                    await culc_channel.send('本案件は参加者に購入者を含む案件になります。違う場合は "えろてろ" までご連絡下さい')
                    del_buyer = 1
                #et_msg = await drop_regi_channel.fetch_message(pp_msg_id)
                #await et_msg.edit(content=str(et_msg.content))
                #et_msg = et_msg.content.split()

                et1_msg = et_msg.pop(0)

                pp = len(et_msg)
            else:
                pp = int(worksheet_list.cell(id_cell.row, 9).value)

            worksheet_list.update_cell(id_cell.row, 7, str('progress'))  # 分配実行フラグ変更
            worksheet_list.update_cell(id_cell.row, 10, str(rbun_dia))  # 分配ダイア入力

            dia = int(rbun_dia)
            id_check = list()
            cama_list = list()
            death_list = list()
            samurai_list = list()

            if del_buyer == 1:
                buyer_check = '0'
            if buyer_check == '0':
                if pp < 10 and dia < 5000:

                    bunpa = dia / pp
                    if bunpa < 50:
                        dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                        if check_new == str(1):

                            dice = random.randint(0, int(pp) - 1)
                            ran_men = et_msg[int(dice)]
                        else:
                            dice_a = int(dice) + int(11)
                            ran_men = worksheet_list.cell(id_cell.row, int(dice_a)).value
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)

                        await culc_channel.send(
                            str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                dia) + ' diaで売れたので分配を行います。\n' + str(
                                worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n分配が50dia未満(' + str(
                                math.floor(bunpa)) + 'dia/人)なので、抽選になります。\n抽選の結果、<@' + str(ran_men) + '> が当選！\n' + str(
                                dia) + ' diaの取引をお願いします。')

                        return
                    else:
                        await culc_channel.send(
                            str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                dia) + ' diaで売れました。\nメンションされている方々は以下に従い' + str(
                                worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n分配：' + str(
                                math.floor(bunpa)) + 'dia\n対象者')
                        for num in range(pp):
                            if check_new == str(1):
                                await culc_channel.send('<@' + str(et_msg[num] + '>'))
                            else:
                                id_col = int(num) + int(12)
                                await culc_channel.send('<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                                await asyncio.sleep(2)
                        #                    id_check = '\n'.join(id_check)
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)
                        await culc_channel.send('finish')
                        return
                elif pp < 10 and dia >= 5000:
                    if not check_new == str(1):
                        if not pp == reaction_num:
                            await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                            return
                    ketsu = dia * 0.03
                    bunpb = (dia - ketsu * 3) / pp
                    await culc_channel.send(
                        str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                            worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                            dia) + ' diaで売れました。\nメンションされている方々は以下に従い' + str(
                            worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金として ' + str(
                            math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(math.floor(
                            bunpb)) + 'diaで出品して下さい。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
                    for num in range(pp):
                        if check_new == str(1):
                            await culc_channel.send('<@' + str(et_msg[num] + '>'))
                        else:
                            id_col = int(num) + int(12)
                            await culc_channel.send('<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>\n')
                            await asyncio.sleep(2)
                        #                    id_check = '\n'.join(id_check)
                    worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                    #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)
                    await culc_channel.send('finish')

                    return
                else:
                    if 10 <= pp < 25 and dia >= 5000:
                        if not check_new == str(1):
                            if not pp == reaction_num:
                                await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                return
                        ketsu = dia * 0.03
                        tema = dia * 0.05
                        if tema < 500:
                            bunpb = (dia - ketsu * 3 - tema) / pp
                            await culc_channel.send(
                                str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                    worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(
                                    worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金:' + str(
                                    math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(
                                    math.floor(bunpb)) + 'diaで出品して下さい。\nちなみに手間賃' + str(math.floor(
                                    tema)) + 'diaです。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
                            for num in range(pp):
                                if check_new == str(1):
                                    await culc_channel.send('<@' + str(et_msg[num] + '>'))
                                else:
                                    id_col = int(num) + int(12)
                                    await culc_channel.send(
                                        '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                                    await asyncio.sleep(2)
                                    #                    id_check = '\n'.join(id_check)
                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                            #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)
                            await culc_channel.send('finish')

                        elif tema >= 500:
                            if not check_new == str(1):
                                if not pp == reaction_num:
                                    await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                    return
                            tema = 500
                            bunpb = (dia - ketsu * 3 - tema) / pp
                            await culc_channel.send(
                                str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                    worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(
                                    worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金:' + str(
                                    math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(
                                    math.floor(bunpb)) + 'diaで出品して下さい。\nちなみに手間賃は上限の' + str(math.floor(
                                    tema)) + 'diaです。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
                            for num in range(pp):
                                if check_new == str(1):
                                    await culc_channel.send('<@' + str(et_msg[num] + '>'))
                                else:
                                    id_col = int(num) + int(12)
                                    await culc_channel.send(
                                        '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                                # id_check = '\n'.join(id_check)
                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                            #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)
                            await culc_channel.send('finish!')

                        else:
                            await culc_channel.send('えろてろまで問い合わせを。')
                        return

                    elif 10 <= pp < 25 and dia < 5000:
                        tema = dia * 0.05
                        bunpb = (dia - tema) / pp
                        if bunpb < 50:
                            dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                            if check_new == str(1):
                                dice = random.randint(0, int(pp)-1)
                                ran_men = et_msg[int(dice)]
                            else:
                                dice_a = int(dice) + int(11)
                                ran_men = worksheet_list.cell(id_cell.row, int(dice_a)).value
                            await culc_channel.send(
                                str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                    worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(
                                    worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n分配が50dia未満(' + str(
                                    math.floor(bunpb)) + 'dia/人)なので、抽選を行います。\n...抽選の結果、<@' + str(
                                    ran_men) + '> が当選！\n' + str(dia) + ' diaの取引をお願いします。')
                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                            #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)
                            await culc_channel.send('finish!')
                            return
                        else:
                            if not check_new == str(1):
                                if not pp == reaction_num:
                                    await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                    return
                            await culc_channel.send(
                                str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                    worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(
                                    worksheet_list.cell(id_cell.row,
                                                        5).value) + 'と取引を行って下さい。\n10人以上, 5000dia未満なので以下となります。\nメンションされている方々は ' + str(
                                    math.floor(bunpb)) + 'diaで出品して下さい。\n分配者手数料は' + str(
                                    math.floor(tema)) + 'diaです。\n血盟資金はありません。\n')
                            for num in range(pp):
                                if check_new == str(1):
                                    await culc_channel.send('<@' + str(et_msg[num] + '>'))
                                else:
                                    id_col = int(num) + int(12)
                                    await culc_channel.send(
                                        '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                            worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                            #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)
                            await culc_channel.send('finish!')
                            return
                    else:
                        if pp >= 25 and dia >= 5000:
                            ketsushi = dia * 0.03
                            bunpc = (dia - ketsushi * 3) / pp
                            if bunpc < 100:
                                meishubun1 = dia / 3
                                await culc_channel.send(
                                    str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                        worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                        dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                         5).value) + 'と取引を行って下さい。\n25人以上 / 分配 100dia未満なので全額血盟資金となります。\n３等分した' + str(
                                        math.floor(
                                            meishubun1)) + 'diaを各盟主に渡してください。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n分配者手数料はありません。')
                                worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                                #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)
                                await culc_channel.send('finish!')

                                return
                            else:
                                if not check_new == str(1):
                                    if not pp == reaction_num:
                                        await culc_channel.send(
                                            'Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                        return
                                cama_num = 0
                                death_num = 0
                                samurai_num = 0
                                await culc_channel.send('人数が多いため処理に数分時間がかかる場合があります。しばらくお待ちください。')
                                for num in range(pp):
                                    if check_new == str(1):
                                        id_clan_posi = worksheet_id.find(str(et_msg[num]))
                                        # print(id_clan_posi.col)
                                        await asyncio.sleep(3)
                                        if id_clan_posi.col == 13:
                                            #   print('カマ')
                                            cama_list.append('<@' + str(et_msg[num]) + '>')
                                            cama_num = cama_num + 1
                                        elif id_clan_posi.col == 16:
                                            #   print('デス')
                                            death_list.append('<@' + str(et_msg[num]) + '>')
                                            death_num = death_num + 1
                                        elif id_clan_posi.col == 19:
                                            #   print('サムライ')
                                            samurai_list.append('<@' + str(et_msg[num]) + '>')
                                            samurai_num = samurai_num + 1
                                    else:
                                        id_col = int(num) + int(12)
                                        id_clan_posi = worksheet_id.find(
                                            str(worksheet_list.cell(id_cell.row, id_col).value))
                                        # print(id_clan_posi.col)
                                        await asyncio.sleep(3)

                                        if id_clan_posi.col == 13:
                                            #   print('カマ')
                                            cama_list.append(
                                                '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                                            cama_num = cama_num + 1
                                        elif id_clan_posi.col == 16:
                                            #   print('デス')
                                            death_list.append(
                                                '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                                            death_num = death_num + 1
                                        elif id_clan_posi.col == 19:
                                            #   print('サムライ')
                                            samurai_list.append(
                                                '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                                            samurai_num = samurai_num + 1
                                cama_list = '\n'.join(cama_list)
                                death_list = '\n'.join(death_list)
                                samurai_list = '\n'.join(samurai_list)
                                bun_cama = bunpc * cama_num + ketsushi
                                bun_death = bunpc * death_num + ketsushi
                                bun_samurai = bunpc * samurai_num + ketsushi

                                await culc_channel.send(
                                    str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                        worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                        dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                         5).value) + 'と取引を行って下さい。\n25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。\n尚、血盟資金 ' + str(
                                        math.floor(ketsushi)) + 'diaも含まれています。\n\n<@477504935727071232>さん： ' + str(
                                        math.floor(bun_cama)) + ' diaを受取り、以下の方に ' + str(
                                        math.floor(bunpc)) + ' diaを分配下さい。\n' + str(
                                        cama_list) + '\n\n<@363032621845839892>さん： ' + str(
                                        math.floor(bun_samurai)) + ' diaを受取り、以下の方に ' + str(
                                        math.floor(bunpc)) + ' diaを分配下さい。\n' + str(
                                        samurai_list) + '\n\n<@290377448711782400>さん： ' + str(
                                        math.floor(bun_death)) + ' diaを受取り、以下の方に ' + str(
                                        math.floor(bunpc)) + ' diaを分配下さい。\n ' + str(death_list))
                                worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                                #if del_buyer == 1:
  #                          msg_content.append(buyer_id)
    #                        await et_msg.edit(content=msg_content)
                                await culc_channel.send('finish!')

                                return

                        elif pp >= 25 and dia < 5000:
                            # print('ここまできたよ')
                            bunpd = dia / pp
                            if bunpd < 100:

@client.event
async def on_raw_reaction_add(payload):
    regi_channel = client.get_channel(744727455293767711)
    culc_channel = client.get_channel(740355050182017135)  # 本番用
    drop_regi_channel = client.get_channel(798521158302826525)
    sell_channel = client.get_channel(722845189961416786)

    if payload.user_id == 689736979075825706:
        return
    elif payload.user_id == 754892023613620316:
        return

    elif payload.channel_id == 732658643740262553:
        channel = client.get_channel(722253361159864479)
        now = dt.now()
        now1 = str(now)
        await channel.send(
            'Date&Time:\n' + now1 + '\nmessage channel & id\n' + str(payload.channel_id) + '\nmessage-id\n' + str(
                payload.message_id) + '\nreaction-user-id\r\n' + str(payload.user_id) + '\n_')

    # elif payload.channel_id == 744727455293767711:  #getしたやつの登録コマンド
    #     print(payload.user_id)
    #     worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
    #     embed_msg = await regi_channel.fetch_message(payload.message_id)
    #     m_id = embed_msg.embeds[0].description.split()
    #     regi_mid = str(m_id[1])
    #     if m_id[0] =='MSG-ID:':
    #         uid_msg1 = await drop_regi_channel.fetch_message(regi_mid)
    #         uid_msg0 = uid_msg1.content.split()
    #         if str(payload.user_id) in str(uid_msg0):
    #             return
    #         else:
    #             await uid_msg1.edit(content=str(uid_msg1.content) + ' ' + str(payload.user_id))
    #             await payload.member.send('新しい機能で登録しました。お知らせ機能は今後削除予定です。')
    #     else:
    #         search_mid = payload.message_id
    #         mid_cell = worksheet_find.find(str(search_mid))
    #         entry1_id = worksheet_find.cell(mid_cell.row, 12).value
    #         if str(entry1_id) == str(payload.user_id):
    #             msg = await regi_channel.send(
    #                 '拾得者（登録した人）はリアクションは不要なので解除して下さい。\n他に修正が必要な場合は"えろてろ"までご連絡をお願いします。\n本メッセージは10秒後に自動で削除されます。')
    #             await asyncio.sleep(3)
    #             await msg.delete()
    #         else:
    #             entry_num = worksheet_find.cell(mid_cell.row, 166).value
    #             entry_col = int(entry_num) + int(12)
    #             worksheet_find.update_cell(mid_cell.row, int(entry_col), str(payload.user_id))
    #             entry_idnum = worksheet_find.cell(mid_cell.row, 1).value
    #             await payload.member.send(str(entry_idnum) + 'に参加登録しました。間違えていたら管理者へ連絡下さい。')

    elif payload.channel_id == 740355050182017135:
        msg_id = payload.message_id
        #        test_channel = client.get_channel(722253470023024640)
        msg = await culc_channel.fetch_message(msg_id)
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
#                await msg.clear_reactions()
            else:
                # print('りたーん！')
                return
        else:
            #            print('えろぼっと以外へのリアクション！')
            return
    elif payload.channel_id == 722845189961416786:
        aut_msg = await sell_channel.fetch_message(payload.message_id)
        if aut_msg.author == client.user:
            return
        else:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
            search_mid = payload.message_id
            mid_cell = worksheet_sell.find(str(search_mid))
            entry_num = worksheet_sell.cell(mid_cell.row, 10).value
            entry_col = int(entry_num) + int(11)
            worksheet_sell.update_cell(mid_cell.row, int(entry_col), str(payload.user_id))

    else:
        return

@client.event
async def on_raw_reaction_remove(payload):
    regi_channel = client.get_channel(744727455293767711)
    culc_channel = client.get_channel(740355050182017135)  # 本番用
    drop_regi_channel = client.get_channel(798521158302826525)

    if payload.user_id == 689736979075825706:
        return
    elif payload.user_id == 754892023613620316:
        return

    elif payload.channel_id == 732658643740262553:
        channel = client.get_channel(722253361159864479)
        now2 = dt.now()
        now3 = str(now2)
        await channel.send(
            'Date&Time:\n' + now3 + '\nmessage channel\n' + str(payload.channel_id) + '\nmessage-id\n' + str(
                payload.message_id) + '\nreaction-user-id\r\n' + str(payload.user_id) + 'del\n_')

    # # elif payload.channel_id == 744727455293767711:
    # #     worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
    # #     embed_msg = await regi_channel.fetch_message(payload.message_id)
    # #     m_id = embed_msg.embeds[0].description.split()
    # #     regi_mid = str(m_id[1])
    # #     if m_id[0] =='MSG-ID:':
    # #         uid_msg1 = await drop_regi_channel.fetch_message(regi_mid)
    # #         uid_msg0 = uid_msg1.content.split()
    # #         if str(payload.user_id) == str(uid_msg0[1]):
    # #             return
    # #         else:
    # #             uid_msg2 = uid_msg1.content.replace(str(payload.user_id), '')
    # #             await uid_msg1.edit(content=str(uid_msg2))
    # #             await payload.member.send('新しい機能で登録を削除しました。お知らせ機能は今後削除予定です。')
    #
    #     else:
    #         search_mid = payload.message_id
    #         mid_cell = worksheet_find.find(str(search_mid))
    #         #msg_id = worksheet_find.cell(mid_cell.row, 13).value
    #         col_list = worksheet_find.row_values(mid_cell.row)
    #         entry_num = worksheet_find.cell(mid_cell.row, 166).value
    #         entry1_id = worksheet_find.cell(mid_cell.row, 12).value
    #         del_col = int(col_list.index(str(payload.user_id))) + int(1)
    #         if str(entry1_id) == str(payload.user_id):
    #             # print('同じだよ')
    #             return
    #         elif entry_num == 1:
    #             worksheet_find.update_cell(mid_cell.row, int(del_col), str(''))
    #             return
    #         else:
    #             enum = int(del_col) - int(12)
    #             entry = int(entry_num) - int(enum)
    #             del_col2 = del_col
    #             for num in range(1, int(entry)):
    #                 right_col = int(del_col2) + 1
    #                 up_id = worksheet_find.cell(mid_cell.row, int(right_col)).value
    #                 worksheet_find.update_cell(mid_cell.row, int(del_col2), up_id)
    #                 del_col2 = del_col + num
    #             worksheet_find.update_cell(mid_cell.row, int(del_col2), str(''))
    #

    elif payload.channel_id == 722845189961416786:
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
        search_mid = payload.message_id
        mid_cell = worksheet_sell.find(str(search_mid))
        col_list = worksheet_sell.row_values(mid_cell.row)
        entry_num = worksheet_sell.cell(mid_cell.row, 10).value
        del_col = int(col_list.index(str(payload.user_id))) + int(1)
        if entry_num == 1:
            worksheet_sell.update_cell(mid_cell.row, int(del_col), str(''))
            return
        else:
            enum = int(del_col) - int(10)
            entry = int(entry_num) - int(enum)
            del_col2 = del_col
            for num in range(1, int(entry)):
                if not num == int(entry):
                    right_col = int(del_col2) + 1
                    up_id = worksheet_sell.cell(mid_cell.row, int(right_col)).value
                    worksheet_sell.update_cell(mid_cell.row, int(del_col2), up_id)
                del_col2 = del_col + num
            worksheet_sell.update_cell(mid_cell.row, int(del_col2), str(''))
    else:
        return

    # elif payload.channel_id == 722253470023024640:
    #     msg_id = payload.message_id
    #     test_channel = client.get_channel(722253470023024640)
    #     msg = await test_channel.fetch_message(msg_id)
    #     msg1 = discord.utils.escape_markdown(msg.content)
    #     print(msg1)
    #     msg1 = msg1.strip('\~')
    #     print(msg1)
    #     #msg1 = msg1.rstrip("~~")
    #     await msg.edit(content= msg1)


@client.event
async def on_message(message):
    culc_channel = client.get_channel(740355050182017135)  # 本番用
    wai_channel = client.get_channel(658468918243098626)  # 本番用
    ami_channel = client.get_channel(675359824803790850)
    list_channel = client.get_channel(743314066713477251)
    regi_channel = client.get_channel(744727455293767711)
    test_channel = client.get_channel(722253470023024640)
    sell_channel = client.get_channel(722845189961416786)
    drop_regi_channel = client.get_channel(798521158302826525)

    if message.author == client.user:
        return

    elif message.content.startswith('test'):
        if message.channel.id == 722253470023024640:
            await test_channel.send('<@592253165068615680>')

    elif message.content.startswith('!bun '):
        m_num = message.content.strip('!bun ')
        m_list = m_num.split()
        # 人数ppとdiaに分ける。
        pp = int(m_list[0])
        dia = int(m_list[1])

        if pp < 10 and dia < 5000:
            bunpa = dia / pp
            if bunpa < 50:
                dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                await culc_channel.send(
                    '分配が50dia未満(' + str(math.floor(bunpa)) + 'dia/人)なので、抽選を行います。\nリアクション表示の上から ' + str(
                        dice) + ' 番目の方に ' + str(dia) + ' diaを渡してください。\nリアクション表示と人数が異なる場合は別途抽選を行ってください。')
            else:
                await culc_channel.send(
                    '10人未満,5000dia未満なので以下となります。\n分配：' + str(math.floor(bunpa)) + 'dia\n血盟資金、分配者手数料はありません。')
                return

        elif pp < 10 and dia >= 5000:
            ketsu = dia * 0.03
            bunpb = (dia - ketsu * 3) / pp
            await culc_channel.send(
                '10人未満, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
                    math.floor(bunpb)) + 'diaになります。\n分配者手数料は１０人未満なのでありません。')
            return

        else:
            if 10 <= pp < 25 and dia >= 5000:
                ketsu = dia * 0.03
                tema = dia * 0.05
                if tema < 500:
                    bunpb = (dia - ketsu * 3 - tema) / pp
                    await culc_channel.send(
                        '10人以上, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
                            math.floor(bunpb)) + 'diaになります。\nちなみに手間賃は' + str(math.floor(tema)) + 'diaです。')
                    return
                elif tema >= 500:
                    tema = 500
                    bunpb = (dia - ketsu * 3 - tema) / pp
                    await culc_channel.send(
                        '10人以上, 5000dia以上なので以下となります。\n血盟資金:' + str(math.floor(ketsu)) + 'diaを各盟主へ渡してください。\n分配：' + str(
                            math.floor(bunpb)) + 'diaになります。\nちなみに手間賃は上限の' + str(math.floor(tema)) + 'diaです。')
                    return
                else:
                    await culc_channel.send('えろてろまで問い合わせを。')

            elif 10 <= pp < 25 and dia < 5000:
                tema = dia * 0.05
                bunpb = (dia - tema) / pp
                if bunpb < 50:
                    dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                    await culc_channel.send(
                        '分配が50dia未満(' + str(math.floor(bunpb)) + 'dia/人)なので、抽選を行います。\nリアクション表示の上から ' + str(
                            dice) + ' 番目の方に' + str(dia) + 'diaを渡してください。\nリアクション表示と人数が異なる場合は別途抽選を行ってください。')
                    return
                else:
                    await culc_channel.send(
                        '10人以上, 5000dia未満なので以下となります。\n分配：' + str(math.floor(bunpb)) + 'diaになります。\n分配者手数料は' + str(
                            math.floor(tema)) + 'diaです。\n血盟資金はありません。')
                    return

            else:
                if pp >= 25 and dia >= 5000:
                    ketsushi = dia * 0.03
                    bunpc = (dia - ketsushi * 3) / pp
                    if bunpc < 100:
                        meishubun1 = dia / 3
                        await culc_channel.send('25人以上 / 分配 100dia未満なので全額血盟資金となります。\n３等分した' + str(
                            math.floor(meishubun1)) + 'diaを各盟主に渡してください。\n分配者手数料、血盟資金はありません。')
                        return
                    else:
                        await culc_channel.send('25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。\n' + str(
                            math.floor(bunpc)) + ' × 各血盟の対象人数 + ' + str(
                            math.floor(ketsushi)) + 'dia(血盟資金）の合計を各盟主に渡してください。\n分配者手数料はありません。')
                        return
                elif pp >= 25 and dia < 5000:
                    bunpd = dia / pp
                    if bunpd < 100:
                        meishubun2 = dia / 3
                        await culc_channel.send('25人以上で分配が100dia/人 未満なので全額血盟資金となります。\n' + str(
                            math.floor(meishubun2)) + 'diaを各盟主に渡してください。\n分配者手数料、血盟資金はありません。')
                        return
                    else:
                        await culc_channel.send(
                            '25人以上で分配が100dia/人 以上なので以下に従って盟主と取引して下さい。\n今回は盟主が分配するため、血盟資金 + 各血盟の対象人数 × ' + str(
                                math.floor(bunpd)) + 'diaを各盟主に渡してください。\n分配者手数料はありません。')
                        return
                else:
                    await culc_channel.send('えろてろまで問い合わせを。')

    elif message.content.startswith('!dice '):
        if message.channel.id == 675359824803790850:
            rami_num = message.content.strip('!dice ')
            rami_list = rami_num.split()
            # 人数ppとdiaに分ける。
            rami_rand = int(rami_list[0])
            rami_dice = random.randint(1, rami_rand)  # サイコロを振る。出る目を指定。
            await ami_channel.send('抽選した結果、' + str(rami_dice) + ' 番が当選！オーメデトーゴーザイマース！')
            return
        return

    elif message.content.startswith('!nami '):
        if message.channel.id == 675359824803790850:
            nami_num = message.content.strip('!nami')
            nami_list = nami_num.split()
            nami_rand = random.choice(nami_list)
            await ami_channel.send('抽選した結果、' + str(nami_rand) + ' が当選！オーメデトーゴーザイマース！')
            return
        return

    elif message.content.startswith('ワイが'):
        if message.author.id == 591281241798737938:
            await wai_channel.send('アンタ誰や？下の板言うてないで狩りしーや？')
        else:
            #            await wai_channel.send(message.author.name + 'や。さるじやあらへん。\nあいつは今びっくり焼きを調べるのに夢中やで！')
            worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
            import_value = str(message.author.name + 'や。さるじやあらへん')

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

    # boss drop management bot. (!get(n or r) BossName DropItem)### n = normal, r = rare
    elif message.content.startswith('get '):
        if message.channel.id == 744727455293767711:
            drop_high_list = message.content.split()
            drop_high_boss = drop_high_list[1]
            drop_high_item = drop_high_list[2]
            today = dt.now()
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
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
            regi_msg = await drop_regi_channel.send('r' + str(id_no) + ' ' + (str(message.author.id)))
            #            worksheet_list.update_cell(input_id, 8, str(message.id))
            # worksheet_list.update_cell(input_id, 10, str('-'))
            # worksheet_list.update_cell(input_id, 11, str('-'))
            worksheet_list.update_cell(input_id, 12, str(message.author.id))
            # worksheet_list.update_cell(input_id, 13, str(regi_msg.id))
            worksheet_list.update_cell(input_id, 168, 1)

            drp = discord.Embed(title='ID: r' + str(id_no) + ' / " ' + str(drop_high_boss) + ' " / " ' + str(drop_high_item) + ' "\n拾得者:' + str(message.author.name), description='MSG-ID: ' + str(regi_msg.id) + ' \n参加者はリアクションして下さい。/Please reaction!', color=discord.Colour.red())
            #               await wai_channel.send(embed=grn)
            #await drop_id_channel.send(str(id_no) + ' ' + str(regi_msg.id))
            msg = await regi_channel.send(embed=drp)  # debag
            #               msg = await grn_channel.send(embed=grn)#本番
            emoji1 = '\U0001F947'
            await msg.add_reaction(emoji1)
            worksheet_list.update_cell(input_id, 8, str(msg.id))
            #await message.delete()
            return

    elif message.content.startswith('!getnnnnnnnnn '):
        if message.channel.id == 744727455293767711:
            drop_high_list = message.content.split()
            drop_high_boss = drop_high_list[1]
            drop_high_item = drop_high_list[2]
            today = dt.now()
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            id_total = worksheet_id.cell(4, 8).value
            id_num = worksheet_id.cell(4, 9).value
            input_id = int(id_total) + 2
            id_no = int(id_num) + 1
            worksheet_list.update_cell(input_id, 1, 'n' + str(id_no))  # id number
            worksheet_list.update_cell(input_id, 2, str(drop_high_boss))  # boss name
            worksheet_list.update_cell(input_id, 3, str(drop_high_item))  # item name
            worksheet_list.update_cell(input_id, 4, str('normal'))  # item grade
            worksheet_list.update_cell(input_id, 5, str(message.author.name))  # 記入者
            worksheet_list.update_cell(input_id, 6,
                                       str(today.year) + '/' + str(today.month) + '/' + str(today.day))  # 登録日
            worksheet_list.update_cell(input_id, 7, str('none'))
            #            worksheet_list.update_cell(input_id, 8, str(message.id))
            worksheet_list.update_cell(input_id, 10, str('-'))
            worksheet_list.update_cell(input_id, 11, str('-'))

            drp = discord.Embed(
                title='" ' + str(drop_high_boss) + ' " dropped " ' + str(drop_high_item) + ' "\nOwner(所有者):  ' + str(
                    message.author.name) + '\nAllocated ID: n' + str(id_no),
                description='Please reaction!',
                color=discord.Colour.red())
            #               await wai_channel.send(embed=grn)
            msg = await regi_channel.send(embed=drp)  # debag
            #               msg = await grn_channel.send(embed=grn)#本番
            emoji1 = '\U0001F947'
            await msg.add_reaction(emoji1)
            worksheet_list.update_cell(input_id, 8, str(msg.id))
            await message.delete()
            return

    elif message.content.startswith('!del '):
        if message.channel.id == 743314066713477251:
            if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
                worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
                del_list = message.content.split()
                del_cell = worksheet_find.findall(str(del_list[1]))
                del_id = worksheet_find.cell(del_cell[0].row, 1).value
                #                worksheet_find.update_cell(del_cell[0].row, 1, '')
                worksheet_find.update_cell(del_cell[0].row, 2, '-')
                worksheet_find.update_cell(del_cell[0].row, 3, '-')
                #                worksheet_find.update_cell(del_cell[0].row, 4, '')
                worksheet_find.update_cell(del_cell[0].row, 5, '-')
                worksheet_find.update_cell(del_cell[0].row, 6, '-')
                worksheet_find.update_cell(del_cell[0].row, 7, 'delete')
                worksheet_find.update_cell(del_cell[0].row, 10, '')
                worksheet_find.update_cell(del_cell[0].row, 11, '')
                del_p = int(worksheet_find.cell(del_cell[0].row, 166).value)
                for num in range(del_p):
                    num = num + int(12)
                    worksheet_find.update_cell(del_cell[0].row, num, '')
                await list_channel.send(del_id + 'を削除しました。')

    elif message.content.startswith('!back '):
        if message.channel.id == 743314066713477251:
            if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
                worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
                del_list = message.content.split()
                del_cell = worksheet_find.findall(str(del_list[1]))
                del_id = worksheet_find.cell(del_cell[0].row, 1).value
                worksheet_find.update_cell(del_cell[0].row, 7, 'none')
                worksheet_find.update_cell(del_cell[0].row, 10, '-')
                await list_channel.send(del_id + 'を未分配に戻しました。')

    elif message.content.startswith('!fin '):
        if message.channel.id == 743314066713477251:
            if message.author.id == 689731790935425034 or message.author.id == 592253165068615680 or message.author.id == 363032621845839892 or message.author.id == 600694063913631755 or message.author.id == 352019449022251009 or message.author.id == 477504935727071232 or message.author.id == 425017805729955840:
                worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
                fin_list = message.content.split()
                fin_dia = fin_list[2]
                fin_cell = worksheet_find.findall(str(fin_list[1]))
                fin_id = worksheet_find.cell(fin_cell[0].row, 1).value
                worksheet_find.update_cell(fin_cell[0].row, 7, 'finish')
                worksheet_find.update_cell(fin_cell[0].row, 10, str(fin_dia))
                await list_channel.send(fin_id + 'を分配完了にしました。')

    elif message.content.startswith('!own_change '):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            che_list = message.content.split()
            che_cell = worksheet_find.findall(str(che_list[1]))
            worksheet_find.update_cell(che_cell[0].row, 5, str(che_list[2]))

    elif message.content.startswith('list'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            cell_list = worksheet_find.findall('none')
            # print(cell_list)
            deal_count = worksheet_id.cell(5, 8).value
            r_list = list()
            for num in range(int(deal_count)):
                get_id = worksheet_find.cell(cell_list[num].row, 1).value
                get_boss = worksheet_find.cell(cell_list[num].row, 2).value
                get_item = worksheet_find.cell(cell_list[num].row, 3).value
                get_name = worksheet_find.cell(cell_list[num].row, 5).value
                get_date = worksheet_find.cell(cell_list[num].row, 6).value
                r_list.append(get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
                await asyncio.sleep(4)
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

    elif message.content.startswith('!list r'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            cell_list = worksheet_find.findall('none')
            deal_count = worksheet_id.cell(5, 8).value
            r_list = list()
            for num in range(int(deal_count)):
                get_grade = worksheet_find.cell(cell_list[num].row, 4).value
                if get_grade == 'rare':
                    get_id = worksheet_find.cell(cell_list[num].row, 1).value
                    get_boss = worksheet_find.cell(cell_list[num].row, 2).value
                    get_item = worksheet_find.cell(cell_list[num].row, 3).value
                    get_name = worksheet_find.cell(cell_list[num].row, 5).value
                    get_date = worksheet_find.cell(cell_list[num].row, 6).value
                    r_list.append(
                        get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
            r_list = '\n'.join(r_list)
            get_r = discord.Embed(title='DROP ITEM LIST (GRADE: RARE)',
                                  description='ID \t:\t  boss \t/  item \t/  holder \t/  date',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(r_list), inline=True)
            await list_channel.send(embed=get_r)
            return

    elif message.content.startswith('!list n'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            cell_list = worksheet_find.findall('none')
            deal_count = worksheet_id.cell(5, 8).value
            r_list = list()
            for num in range(int(deal_count)):
                get_grade = worksheet_find.cell(cell_list[num].row, 4).value
                if get_grade == 'normal':
                    get_id = worksheet_find.cell(cell_list[num].row, 1).value
                    get_boss = worksheet_find.cell(cell_list[num].row, 2).value
                    get_item = worksheet_find.cell(cell_list[num].row, 3).value
                    get_name = worksheet_find.cell(cell_list[num].row, 5).value
                    get_date = worksheet_find.cell(cell_list[num].row, 6).value
                    r_list.append(
                        get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
            r_list = '\n'.join(r_list)
            get_r = discord.Embed(title='DROP ITEM LIST (GRADE: NORMAL)',
                                  description='ID \t:\t  boss \t/  item \t/  holder \t/  date',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(r_list), inline=True)
            await list_channel.send(embed=get_r)
            return

    elif message.content.startswith('mylist'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
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

    elif message.content.startswith('merolist'):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            #            cell_list = worksheet_find.findall(str(message.author.name))
            cell_list = worksheet_find.findall(str('メロリンＱ'))
            # print(cell_list)
            deal_count = len(cell_list)
            if deal_count == 0:
                await list_channel.send('ご苦労様です。\n' + str(message.author.name) + ' さんの未分配案件はありません。')
                return
            r_list = list()
            # print(deal_count)
            for num in range(int(deal_count)):
                if worksheet_find.cell(cell_list[num].row, 7).value == 'none':
                    get_id = worksheet_find.cell(cell_list[num].row, 1).value
                    get_boss = worksheet_find.cell(cell_list[num].row, 2).value
                    get_item = worksheet_find.cell(cell_list[num].row, 3).value
                    get_name = worksheet_find.cell(cell_list[num].row, 5).value
                    get_date = worksheet_find.cell(cell_list[num].row, 6).value
                    r_list.append(
                        get_id + '\t: ' + get_boss + '\t/ ' + get_item + '\t/ ' + get_name + '\t/ ' + get_date)
                    await asyncio.sleep(2)
                else:
                    await asyncio.sleep(1)
                # print(r_list)
                # print(len(r_list))
                r_count = int(len(r_list))
                if r_count == 0:
                    await list_channel.send('ご苦労様です。\n' + str(message.author.name) + ' さんの未分配案件はありません。\n全て完了していました。')
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

    elif message.content.startswith('repo '):
        if message.channel.id == 743314066713477251:
            worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            id_cell_list = message.content.split()
            id_cell = worksheet_find.findall(str(id_cell_list[1]))
            pp = worksheet_find.cell(id_cell[0].row, 166).value
            get_id = worksheet_find.cell(id_cell[0].row, 1).value
            get_boss = worksheet_find.cell(id_cell[0].row, 2).value
            get_item = worksheet_find.cell(id_cell[0].row, 3).value
            get_name = worksheet_find.cell(id_cell[0].row, 5).value
            get_date = worksheet_find.cell(id_cell[0].row, 6).value
            add_col = int(12)
            id_check = list()
            for num in range(int(pp)):
                id_col = int(num) + int(add_col)
                id_check.append('<@' + worksheet_find.cell(id_cell[0].row, id_col).value + '>\n')
            id_check = '\n'.join(id_check)
            drp = discord.Embed(
                title='ID: ' + str(get_id) + ' detail',
                description='BOSS: ' + str(get_boss) + ' / ITEM: ' + str(get_item) + '\nOWNER: ' + str(
                    get_name) + ' / DATA: ' + str(get_date) + '\nENTRY\n' + str(id_check),
                color=discord.Colour.red())
            msg = await list_channel.send(embed=drp)  # debag

    elif message.content.startswith('entry '):
        if message.channel.id == 743314066713477251:
            worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
            worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
            rbun_list = message.content.split()
            rbun_id = rbun_list[1]
            id_cell = worksheet_list.find(str(rbun_id))
            pp = int(worksheet_list.cell(id_cell.row, 9).value)
            cama_num = 0
            death_num = 0
            samurai_num = 0
            cama_list = list()
            death_list = list()
            samurai_list = list()
            par_read = 0
            par_msg = await list_channel.send('Load progress...' + str(par_read) + '%')
            for num in range(pp):
                par_read = int(num) / int(pp) * 100
                await par_msg.edit(content='Load progress...' + str(math.floor(par_read)) + '%')
                id_col = int(num) + int(12)
                id_clan_posi = worksheet_id.find(str(worksheet_list.cell(id_cell.row, id_col).value))
                # print(id_clan_posi.col)
                await asyncio.sleep(3)

                if id_clan_posi.col == 13:
                    #   print('カマ')
                    cama_list.append('<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                    cama_num = cama_num + 1
                elif id_clan_posi.col == 16:
                    #   print('デス')
                    death_list.append('<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                    death_num = death_num + 1
                elif id_clan_posi.col == 19:
                    #   print('サムライ')
                    samurai_list.append(
                        '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                    samurai_num = samurai_num + 1
            cama_list = '\n'.join(cama_list)
            death_list = '\n'.join(death_list)
            samurai_list = '\n'.join(samurai_list)
            await par_msg.edit(content='Load progress...100%')

            get_r = discord.Embed(title=str(rbun_id) + ' : List of attendees(CAMA)',
                                  description='Please check below',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(cama_list),
                            inline=True)
            await list_channel.send(embed=get_r)

            get_r = discord.Embed(title=str(rbun_id) + ' : List of attendees(DEATH)',
                                  description='Please check below',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(death_list),
                            inline=True)
            await list_channel.send(embed=get_r)

            get_r = discord.Embed(title=str(rbun_id) + ' : List of attendees(SAMURAI)',
                                  description='Please check below',
                                  color=discord.Colour.red())
            get_r.add_field(name='---------------------------------------------', value=str(samurai_list),
                            inline=True)
            await list_channel.send(embed=get_r)


    elif message.content.startswith('bun '):
        await culc_channel.send('Please wait...')
        worksheet_list = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        rbun_list = message.content.split()
        rbun_id = rbun_list[1]  # idを格納
        rbun_dia = rbun_list[2]  # diaを格納
        id_cell = worksheet_list.find(str(rbun_id))  # idからスプシの行を検索
        if worksheet_list.cell(id_cell.row, 7).value == 'finish':
            await culc_channel.send(str(rbun_id) + 'は分配案内が完了しています。\n' + str(rbun_id) + ' was finished.\n')
            return

        entry_msg_id = worksheet_list.cell(id_cell.row, 8).value  # BOTのメッセージIDを格納
        #print(entry_msg_id)
        entry_msg = await regi_channel.fetch_message(entry_msg_id)  # BOTのメッセージ情報を格納
        reaction_num = int(entry_msg.reactions[0].count)  # botのリアクション数を格納。
        reac_users = await entry_msg.reactions[0].users().flatten()  # botのメッセージ情報からリアクションユーザー情報を格納。
        reac_user = list()
        for num in range(int(reaction_num)):
            reac_user.append(reac_users[num].id)
        own_id = str(worksheet_list.cell(id_cell.row, 12).value)  # スプシから拾得者IDを格納。
        #print(reac_user)
        reac_user.remove(754892023613620316)  # bot idをリアクション情報から削除
        #print(reac_user)
        if not own_id in str(reac_user):  # 登録者（拾得者）がリアクションしていた場合　（していない場合、reac_userに追加する）
            reac_user.append(str(own_id))  # リアクション情報から登録者IDを追加

        buyer_id = str(worksheet_list.cell(id_cell.row, 11).value)  # 購入者のidを格納
        boss = str(worksheet_list.cell(id_cell.row, 2).value)
        items = str(worksheet_list.cell(id_cell.row, 3).value)
        
        buyer_check = int(0)
        pp = int(len(reac_user))
        if buyer_id in str(reac_user):  # 購入者が参加者にいるか確認
            await culc_channel.send(str(rbun_id) + 'には購入者が含まれています。\n' + str(rbun_id) + ' is include buyer.')
            buyer_check = int(1)
        worksheet_list.update_cell(id_cell.row, 7, str('progress'))  # 分配進行フラグ変更
        worksheet_list.update_cell(id_cell.row, 10, str(rbun_dia))  # 分配ダイア入力
        dia = int(rbun_dia)
        cama_list = list()
        death_list = list()
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
                await culc_channel.send(str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(dia) + ' \nOwner: <@' + str(own_id) + '>抽選!! / lottery !!\nWinner =>> <@' + str(ran_men) + '> !!\nPlease would like a transaction. ')
                return
            else:
                if buyer_check == int(1):
                    bunpa = dia / (pp - int(1))
                await culc_channel.send(
                    str(rbun_id) + '/' + str(boss) + '/' + str(items) + ' =>>' + str(dia) + '\nPlease the following people would take a trade with "<@' + str(own_id) + '>"\nDia to distribute：' + str(math.floor(bunpa)) + 'dia\nReceiver')
                for num in range(pp):
                    if not reac_user[num] == buyer_id:
                        await culc_channel.send('<@' + str(reac_user[num]) + '>')
                worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                await culc_channel.send('finish')
                return
        elif pp < 10 and dia >= 5000:
            if buyer_check == int(1):
                ketsu = dia * 0.03
                bunpb = (dia - ketsu * 3) / (pp - 1)
            else:
                ketsu = dia * 0.03
                bunpb = (dia - ketsu * 3) / pp
            await culc_channel.send(
                str(rbun_id) + 'の' + str(boss) + '/' + str(
                    items) + ' が' + str(
                    dia) + ' diaで売れました。\nメンションされている方々は以下に従い' + str(
                    worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金として ' + str(
                    math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(math.floor(
                    bunpb)) + 'diaで出品して下さい。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
            for num in range(pp):
                if not reac_user[num] == buyer_id:
                    await culc_channel.send('<@' + str(reac_user[num]) + '>')

            worksheet_list.update_cell(id_cell.row, 7, str('finish'))

            await culc_channel.send('finish')
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
                    await culc_channel.send(
                        str(rbun_id) + 'の' + str(boss) + '/' + str(
                            items) + ' が' + str(
                            dia) + ' diaで売れました。\n' + str(
                            worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金:' + str(
                            math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(
                            math.floor(bunpb)) + 'diaで出品して下さい。\nちなみに手間賃' + str(math.floor(
                            tema)) + 'diaです。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
                    for num in range(pp):
                        if not reac_user[num] == buyer_id:
                            await culc_channel.send('<@' + str(reac_user[num]) + '>')

                    worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                    await culc_channel.send('finish')
                elif tema >= 500:
                    tema = 500
                    if buyer_check == int(1):
                        bunpb = (dia - ketsu * 3 - tema) / (pp - 1)
                    else:
                        bunpb = (dia - ketsu * 3 - tema) / pp
                    await culc_channel.send(
                        str(rbun_id) + 'の' + str(boss) + '/' + str(
                            items) + ' が' + str(
                            dia) + ' diaで売れました。\n' + str(
                            worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金:' + str(
                            math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(
                            math.floor(bunpb)) + 'diaで出品して下さい。\nちなみに手間賃は上限の' + str(math.floor(
                            tema)) + 'diaです。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
                    for num in range(pp):
                        if not reac_user[num] == buyer_id:
                            await culc_channel.send('<@' + str(reac_user[num]) + '>')
                    worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                    await culc_channel.send('finish!')
                else:
                    await culc_channel.send('えろてろまで問い合わせを。')
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
                    await culc_channel.send(
                        str(rbun_id) + 'の' + str(boss) + '/' + str(
                            items) + ' が' + str(
                            dia) + ' diaで売れました。\n' + str(
                            worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n分配が50dia未満(' + str(
                            math.floor(bunpb)) + 'dia/人)なので、抽選を行います。\n...抽選の結果、<@' + str(
                            ran_men) + '> が当選！\n' + str(dia) + ' diaの取引をお願いします。')
                    await culc_channel.send('finish!')
                    return
                else:
                    await culc_channel.send(
                        str(rbun_id) + 'の' + str(boss) + '/' + str(
                            items) + ' が' + str(
                            dia) + ' diaで売れました。\n' + str(
                            worksheet_list.cell(id_cell.row,
                                                5).value) + 'と取引を行って下さい。\n10人以上, 5000dia未満なので以下となります。\nメンションされている方々は ' + str(
                            math.floor(bunpb)) + 'diaで出品して下さい。\n分配者手数料は' + str(
                            math.floor(tema)) + 'diaです。\n血盟資金はありません。\n')
                    for num in range(pp):
                        if not reac_user[num] == buyer_id:
                            await culc_channel.send('<@' + str(reac_user[num]) + '>')
                    worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                    await culc_channel.send('finish!')
                    return
            else:
                if pp >= 25 and dia >= 5000:
                    ketsushi = dia * 0.03
                    bunpc = (dia - ketsushi * 3) / pp
                    if bunpc < 100:
                        meishubun1 = dia / 3
                        await culc_channel.send(
                            str(rbun_id) + 'の' + str(boss) + '/' + str(
                                items) + ' が' + str(
                                dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                 5).value) + 'と取引を行って下さい。\n25人以上 / 分配 100dia未満なので全額血盟資金となります。\n３等分した' + str(
                                math.floor(
                                    meishubun1)) + 'diaを各盟主に渡してください。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n分配者手数料はありません。')
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        await culc_channel.send('finish!')
                        return
                    else:
                        cama_num = 0
                        death_num = 0
                        samurai_num = 0
                        await culc_channel.send('人数が多いため処理に数分時間がかかる場合があります。しばらくお待ちください。')
                        cama_member = list()
                        death_member = list()
                        samurai_member = list()
                        cama_member = [679938600598503425, 610111099194310676, 352019449022251009, 563048784569827347,
                                       648874408630550530, 498797752050909184, 593978426185220137, 787341771042062336,
                                       608625288280277014, 701065938698764328, 579650686959091725, 608663618963243031,
                                       598899242718855169, 543061340982607872, 633837702776881192, 601044406824337438,
                                       608534675849347093, 658990317525270550, 477504935727071232, 640848694035480576,
                                       610405882970374144, 589677638176473119, 361082138197491712, 381442228419297292,
                                       288985219317366784, 591281241798737938, 596268979006472193, 616762986723541012,
                                       589053772416811069, 608712090882146374, 617742185311502346, 592253165068615680,
                                       206754555147321344, 613704851062259715, 585823046338609163, 232492256047792128,
                                       689731790935425034, 609839563644338178, 363427335220887552, 523030382472331275,
                                       613378614431580190, 608641992267661352, 470896836471947281, 612143447956258825,
                                       471100732183937024, 420319326772396043, 609704480782680065, 309687019536121856]
                        death_member = [404248649460219904, 740403325240999988, 474134602731225088, 270911452095840257,
                                        478871128220237824, 620206036715962398, 337575751790624768, 391512749584285706,
                                        517337114279673895, 276967946016784385, 584502032929521838, 353399386732101633,
                                        457431062340042764, 425017805729955840, 513707978579247115, 713605858180988958,
                                        478588852852883476, 526753988604067855, 577448215368957959, 572992862682087424,
                                        608979980092702740, 590875270072893440, 516626461126295552, 589746353882791970,
                                        590472640821723136, 672010974697619456, 378197646650900480, 534498287286484992,
                                        381323136085524481, 419482212329717761, 575983349688958991, 555304127312429076,
                                        487404728758566912, 478840802773172224, 299883143026966529, 660176852815708167,
                                        590759761193074719, 380708568241799169, 663300941881147443, 597811954115149844,
                                        683331948298502225, 399031099142963231, 387534705177657344, 384695974058000384,
                                        489869825171259403, 345583843308339200, 357081246037442560, 559343799336173569,
                                        639747845469110272, 699308692440612944, 341213549734920203, 569506131249070109,
                                        684800253228351609, 478844230165463070, 290377448711782400, 434350519323066378,
                                        356103946646847499, 487580751802531840, 600694063913631755, 474540689259102208,
                                        401704045422706698, 696529199481225266, 597012782814068756, 366109222020055043,
                                        743362690986016820, 568081575791820800, 696348504649367584, 604870158301003776,
                                        376216016189128706, 685667957044543506, 390825172451590144, 668436739756523523,
                                        727125227125080064, 669921326126989358, 597801530032128001, 676119704225448050,
                                        637044686384791582, 181691518472552448, 583660009657991187, 711193263834529824,
                                        403192321350565888, 598750620567994368, 663361346238414858, 661944951755767829,
                                        499481563126300673, 555411360943702036, 429951455697305601, 501342039888101377,
                                        593472223336071335, 769551867734392863]
                        samurai_member = [662945642028466187, 668433312678674432, 421674740751532032,
                                          698984669622042645, 665400023491674112, 686580674135719948,
                                          668439280573612052, 326741192739913728, 687997488204087396,
                                          612004971759796235, 457814716627025920, 614397835705712651,
                                          589380212962230283, 736172855280140429, 523678876686090260,
                                          676076916813463553, 523142685205463050, 368074547150454792,
                                          516046250538434578, 687668637779230740, 670963612239659038,
                                          414947776586186765, 609561458811863076, 363032621845839892,
                                          468054964615512084, 614863681351712781, 398509507623387136,
                                          668372877510443009, 701801263930671145, 611228472911724583,
                                          574902915391684608, 381412006969868290, 673508187302920192,
                                          488936383902384129, 686580275957727269, 595625719451877376,
                                          378535494067290128, 462190506655612929, 386438573508788227,
                                          587497079929176065, 695600188617916446, 668433882743308307,
                                          607216358865895437, 671650108391030784, 693039519125209129,
                                          640362451119898635, 640034997801189377, 614865260649775127,
                                          333511394010071051, 670962542025375744, 586782561745764354,
                                          364785331163234304, 700820563588808735, 375534189162004482,
                                          686492852737540116, 576802484773715969]

                        for num in range(pp):
                            if not reac_user[num] == buyer_id:
                                if reac_user[num] in cama_member:
                                    cama_list.append('<@' + str(reac_user[num]) + '>')
                                    cama_num = cama_num + 1
                                elif reac_user[num] in death_member:
                                    death_list.append('<@' + str(reac_user[num]) + '>')
                                    death_num = death_num + 1
                                elif reac_user[num] in samurai_member:
                                    samurai_list.append('<@' + str(reac_user[num]) + '>')
                                    samurai_num = samurai_num + 1
                        cama_list = '\n'.join(cama_list)
                        death_list = '\n'.join(death_list)
                        samurai_list = '\n'.join(samurai_list)
                        bun_cama = bunpc * cama_num + ketsushi
                        bun_death = bunpc * death_num + ketsushi
                        bun_samurai = bunpc * samurai_num + ketsushi
                        await culc_channel.send(
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
                                samurai_list) + '\n\n<@290377448711782400>さん： ' + str(
                                math.floor(bun_death)) + ' diaを受取り、以下の方に ' + str(
                                math.floor(bunpc)) + ' diaを分配下さい。\n ' + str(death_list))
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        await culc_channel.send('finish!')
                        return

                elif pp >= 25 and dia < 5000:
                    # print('ここまできたよ')
                    bunpd = dia / pp
                    if bunpd < 100:
                        meishubun2 = dia / 3
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))

                        await culc_channel.send(
                            str(rbun_id) + 'の' + str(boss) + '/' + str(
                                items) + ' が' + str(
                                dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                 5).value) + 'と取引を行って下さい。\n25人以上で分配が100dia/人 未満なので全額血盟資金となります。\n' + str(
                                math.floor(
                                    meishubun2)) + 'diaを各盟主に渡してください。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n分配者手数料はありません。\n\nfinish!')
                        return
                    else:
                        cama_num = 0
                        death_num = 0
                        samurai_num = 0
                        cama_member = list()
                        death_member = list()
                        samurai_member = list()
                        cama_member = [679938600598503425, 610111099194310676, 352019449022251009, 563048784569827347,
                                       648874408630550530, 498797752050909184, 593978426185220137, 787341771042062336,
                                       608625288280277014, 701065938698764328, 579650686959091725, 608663618963243031,
                                       598899242718855169, 543061340982607872, 633837702776881192, 601044406824337438,
                                       608534675849347093, 658990317525270550, 477504935727071232, 640848694035480576,
                                       610405882970374144, 589677638176473119, 361082138197491712, 381442228419297292,
                                       288985219317366784, 591281241798737938, 596268979006472193, 616762986723541012,
                                       589053772416811069, 608712090882146374, 617742185311502346, 592253165068615680,
                                       206754555147321344, 613704851062259715, 585823046338609163, 232492256047792128,
                                       689731790935425034, 609839563644338178, 363427335220887552, 523030382472331275,
                                       613378614431580190, 608641992267661352, 470896836471947281, 612143447956258825,
                                       471100732183937024, 420319326772396043, 609704480782680065, 309687019536121856]
                        death_member = [404248649460219904, 740403325240999988, 474134602731225088, 270911452095840257,
                                        478871128220237824, 620206036715962398, 337575751790624768, 391512749584285706,
                                        517337114279673895, 276967946016784385, 584502032929521838, 353399386732101633,
                                        457431062340042764, 425017805729955840, 513707978579247115, 713605858180988958,
                                        478588852852883476, 526753988604067855, 577448215368957959, 572992862682087424,
                                        608979980092702740, 590875270072893440, 516626461126295552, 589746353882791970,
                                        590472640821723136, 672010974697619456, 378197646650900480, 534498287286484992,
                                        381323136085524481, 419482212329717761, 575983349688958991, 555304127312429076,
                                        487404728758566912, 478840802773172224, 299883143026966529, 660176852815708167,
                                        590759761193074719, 380708568241799169, 663300941881147443, 597811954115149844,
                                        683331948298502225, 399031099142963231, 387534705177657344, 384695974058000384,
                                        489869825171259403, 345583843308339200, 357081246037442560, 559343799336173569,
                                        639747845469110272, 699308692440612944, 341213549734920203, 569506131249070109,
                                        684800253228351609, 478844230165463070, 290377448711782400, 434350519323066378,
                                        356103946646847499, 487580751802531840, 600694063913631755, 474540689259102208,
                                        401704045422706698, 696529199481225266, 597012782814068756, 366109222020055043,
                                        743362690986016820, 568081575791820800, 696348504649367584, 604870158301003776,
                                        376216016189128706, 685667957044543506, 390825172451590144, 668436739756523523,
                                        727125227125080064, 669921326126989358, 597801530032128001, 676119704225448050,
                                        637044686384791582, 181691518472552448, 583660009657991187, 711193263834529824,
                                        403192321350565888, 598750620567994368, 663361346238414858, 661944951755767829,
                                        499481563126300673, 555411360943702036, 429951455697305601, 501342039888101377,
                                        593472223336071335, 769551867734392863]
                        samurai_member = [662945642028466187, 668433312678674432, 421674740751532032,
                                          698984669622042645, 665400023491674112, 686580674135719948,
                                          668439280573612052, 326741192739913728, 687997488204087396,
                                          612004971759796235, 457814716627025920, 614397835705712651,
                                          589380212962230283, 736172855280140429, 523678876686090260,
                                          676076916813463553, 523142685205463050, 368074547150454792,
                                          516046250538434578, 687668637779230740, 670963612239659038,
                                          414947776586186765, 609561458811863076, 363032621845839892,
                                          468054964615512084, 614863681351712781, 398509507623387136,
                                          668372877510443009, 701801263930671145, 611228472911724583,
                                          574902915391684608, 381412006969868290, 673508187302920192,
                                          488936383902384129, 686580275957727269, 595625719451877376,
                                          378535494067290128, 462190506655612929, 386438573508788227,
                                          587497079929176065, 695600188617916446, 668433882743308307,
                                          607216358865895437, 671650108391030784, 693039519125209129,
                                          640362451119898635, 640034997801189377, 614865260649775127,
                                          333511394010071051, 670962542025375744, 586782561745764354,
                                          364785331163234304, 700820563588808735, 375534189162004482,
                                          686492852737540116, 576802484773715969]
                        for num in range(pp):
                            if not reac_user[num] == buyer_id:
                                if reac_user[num] in cama_member:
                                    cama_list.append('<@' + str(reac_user[num]) + '>')
                                    cama_num = cama_num + 1
                                elif reac_user[num] in death_member:
                                    death_list.append('<@' + str(reac_user[num]) + '>')
                                    death_num = death_num + 1
                                elif reac_user[num] in samurai_member:
                                    samurai_list.append('<@' + str(reac_user[num]) + '>')
                                    samurai_num = samurai_num + 1
                        cama_list = '\n'.join(cama_list)
                        death_list = '\n'.join(death_list)
                        samurai_list = '\n'.join(samurai_list)
                        await culc_channel.send(
                            str(rbun_id) + 'の' + str(boss) + '/' + str(
                                items) + ' が' + str(
                                dia) + ' diaで売れました。\n25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。')
                        if cama_num == 0:
                            cama_bun_total = 0
                        else:
                            cama_bun_total = bunpd * cama_num
                        if death_num == 0:
                            death_bun_total = 0
                        else:
                            death_bun_total = bunpd * death_num
                        if samurai_num == 0:
                            samurai_bun_total = 0
                        else:
                            samurai_bun_total = bunpd * samurai_num
                        await culc_channel.send(
                            '<@477504935727071232>さんに' + str(math.floor(cama_bun_total)) + ' dia を渡してください。')
                        await culc_channel.send(
                            '<@363032621845839892>さんに' + str(math.floor(samurai_bun_total)) + ' dia を渡してください。')
                        await culc_channel.send(
                            '<@290377448711782400>さんに' + str(math.floor(death_bun_total)) + ' dia を渡してください。')
                        cama_bun_total = cama_bun_total * 0.95
                        death_bun_total = death_bun_total * 0.95
                        samurai_bun_total = samurai_bun_total * 0.95
                        await culc_channel.send('以下に分配対象者を列挙しますので、別のコマンド入力はやめてください。')

                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        if cama_num >= 10:
                            cama_ketsu = cama_bun_total * 0.03
                            cama_bun = (cama_bun_total - cama_ketsu) / cama_num
                            await culc_channel.send('<@477504935727071232>さんは以下の方々に' + str(
                                math.floor(cama_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                math.floor(cama_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(cama_list))

                            if death_num >= 10:
                                death_ketsu = death_bun_total * 0.03
                                death_bun = (death_bun_total - death_ketsu) / death_num
                                await culc_channel.send('<@290377448711782400>さんは以下の方々に' + str(
                                    math.floor(death_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                    math.floor(death_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(death_list))

                                if samurai_num >= 10:
                                    samurai_ketsu = samurai_bun_total * 0.03
                                    samurai_bun = (samurai_bun_total - samurai_ketsu) / samurai_num
                                    await culc_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                        math.floor(samurai_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                        math.floor(samurai_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(
                                        samurai_list))
                                else:
                                    samurai_bun_total = bunpd * samurai_num
                                    samurai_bun = samurai_bun_total / samurai_num
                                    await culc_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                        math.floor(samurai_bun)) + ' dia を渡してください。\n' + str(samurai_list))
                            else:
                                death_bun_total = bunpd * death_num
                                death_bun = death_bun_total / death_num
                                await culc_channel.send('<@290377448711782400>さんは以下の方々に' + str(
                                    math.floor(death_bun)) + ' dia を渡してください。\n' + str(death_list))
                                if samurai_num >= 10:
                                    samurai_ketsu = samurai_bun_total * 0.03
                                    samurai_bun = (samurai_bun_total - samurai_ketsu) / samurai_num
                                    await culc_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                        math.floor(samurai_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                        math.floor(samurai_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(
                                        samurai_list))
                                else:
                                    samurai_bun_total = bunpd * samurai_num
                                    samurai_bun = samurai_bun_total / samurai_num
                                    await culc_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                        math.floor(samurai_bun)) + ' dia を渡してください。\n' + str(samurai_list))
                        else:
                            cama_bun_total = bunpd * cama_num
                            cama_bun = cama_bun_total / cama_num
                            await culc_channel.send(
                                '<@477504935727071232>さんに' + str(math.floor(cama_bun_total)) + ' dia を渡してください。')
                            await culc_channel.send('<@477504935727071232>さんは以下の方々に' + str(
                                math.floor(cama_bun)) + ' dia を渡してください。\n' + str(cama_list))
                            if death_num >= 10:
                                death_ketsu = death_bun_total * 0.03
                                death_bun = (death_bun_total - death_ketsu) / death_num
                                await culc_channel.send('<@290377448711782400>さんは以下の方々に' + str(
                                    math.floor(death_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                    math.floor(death_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(death_list))

                                if samurai_num >= 10:
                                    samurai_ketsu = samurai_bun_total * 0.03
                                    samurai_bun = (samurai_bun_total - samurai_ketsu) / samurai_num
                                    await culc_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                        math.floor(samurai_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                        math.floor(samurai_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(
                                        samurai_list))
                                else:
                                    samurai_bun_total = bunpd * samurai_num
                                    samurai_bun = samurai_bun_total / samurai_num
                                    await culc_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                        math.floor(samurai_bun)) + ' dia を渡してください。\n' + str(samurai_list))
                            else:
                                death_bun_total = bunpd * death_num
                                death_bun = death_bun_total / death_num
                                await culc_channel.send('<@290377448711782400>さんは以下の方々に' + str(
                                    math.floor(death_bun)) + ' dia を渡してください。\n' + str(death_list))
                                if samurai_num >= 10:
                                    samurai_ketsu = samurai_bun_total * 0.03
                                    samurai_bun = (samurai_bun_total - samurai_ketsu) / samurai_num
                                    await culc_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                        math.floor(samurai_bun)) + ' dia を渡してください。\nまた10名以上なので血盟資金が' + str(
                                        math.floor(samurai_ketsu)) + 'dia 発生していますので受領下さい。\n' + str(
                                        samurai_list))
                                else:
                                    samurai_bun_total = bunpd * samurai_num
                                    samurai_bun = samurai_bun_total / samurai_num
                                    await culc_channel.send('<@363032621845839892>さんは以下の方々に' + str(
                                        math.floor(samurai_bun)) + ' dia を渡してください。\n' + str(samurai_list))
                        worksheet_list.update_cell(id_cell.row, 7, str('finish'))
                        await culc_channel.send('finish!')
                else:
                    await culc_channel.send('えろてろまで問い合わせを。')

    #########高額レア販売システム#########
    elif message.content.startswith('sell1'):
        #        if not message.channel.id == 363032621845839892 or message.channel.id == 689731790935425034:
        #            return
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
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
            uid_count = worksheet_sell.cell(sell_row, 10).value
            uid_count = int(uid_count)
            await asyncio.sleep(5)
            if int(uid_count) == 0:
                id = worksheet_sell.cell(sell_row, 1).value
                item = worksheet_sell.cell(sell_row, 3).value
                price = worksheet_sell.cell(sell_row, 7).value
                sell_num = worksheet_sell.cell(sell_row, 8).value
                sell_num = int(sell_num)
                owner = worksheet_sell.cell(sell_row, 5).value

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

            if int(uid_count) == 1:
                id = worksheet_sell.cell(sell_row, 1).value
                item = worksheet_sell.cell(sell_row, 3).value
                buyer = worksheet_sell.cell(sell_row, 11).value
                price = worksheet_sell.cell(sell_row, 7).value
                sell_num = worksheet_sell.cell(sell_row, 8).value
                sell_num = int(sell_num)
                owner = worksheet_sell.cell(sell_row, 5).value
                serch_id = worksheet_find.find(id)
                worksheet_find.update_cell(serch_id.row, 11, str(buyer))
                await asyncio.sleep(1)
                
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
                id = worksheet_sell.cell(sell_row, 1).value
                item = worksheet_sell.cell(sell_row, 3).value
                if id == 'r1351':
                    buyer = '592253165068615680'
                else:
                    dice = random.randint(1, int(uid_count))
                    winner = 10 + int(dice)
                    buyer = worksheet_sell.cell(sell_row, int(winner)).value
                price = worksheet_sell.cell(sell_row, 7).value
                sell_num = worksheet_sell.cell(sell_row, 8).value
                sell_num = int(sell_num)
                owner = worksheet_sell.cell(sell_row, 5).value
                serch_id = worksheet_find.find(id)
                worksheet_find.update_cell(serch_id.row, 11, str(buyer))
                await asyncio.sleep(1)

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

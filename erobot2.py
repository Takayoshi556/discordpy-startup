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
async def on_raw_reaction_add(payload):
    regi_channel = client.get_channel(744727455293767711)
    culc_channel = client.get_channel(740355050182017135)  # 本番用

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
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
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
                await msg.clear_reactions()
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
    elif payload.channel_id == 722845189961416786:
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
        search_mid = payload.message_id
        mid_cell = worksheet_find.find(str(search_mid))
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
            #            worksheet_list.update_cell(input_id, 8, str(message.id))
            worksheet_list.update_cell(input_id, 10, str('-'))
            worksheet_list.update_cell(input_id, 11, str('-'))
            worksheet_list.update_cell(input_id, 12, str(message.author.id))

            drp = discord.Embed(
                title='ID: r' + str(id_no) + ' / " ' + str(drop_high_boss) + ' " / " ' + str(
                    drop_high_item) + ' "\n拾得者:' + str(message.author.name),
                description='参加者はリアクションして下さい。/Please reaction!', color=discord.Colour.red())
            #               await wai_channel.send(embed=grn)
            msg = await regi_channel.send(embed=drp)  # debag
            #               msg = await grn_channel.send(embed=grn)#本番
            emoji1 = '\U0001F947'
            await msg.add_reaction(emoji1)
            worksheet_list.update_cell(input_id, 8, str(msg.id))
            await message.delete()
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

            get_r = discord.Embed(title = str(rbun_id) +' : List of attendees(CAMA)',
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
        entry_msg_id = worksheet_list.cell(id_cell.row, 8).value
        pp = int(worksheet_list.cell(id_cell.row, 9).value)
        entry_msg = await regi_channel.fetch_message(entry_msg_id)
        reaction_num = int(entry_msg.reactions[0].count)
        #         if not pp == reaction_num:
        #             await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
        #             return
        #        rbun_buyer = rbun_list[3]
        if worksheet_list.cell(id_cell.row, 7).value == 'finish':
            await culc_channel.send('このID案件は分配案内が完了しています。\n変更したい方は えろてろ までご連絡おねがいします。')
            return
        else:
            worksheet_list.update_cell(id_cell.row, 7, str('finish'))  # 分配実行フラグ変更
            worksheet_list.update_cell(id_cell.row, 10, str(rbun_dia))  # 分配ダイア入力
            #            worksheet_list.update_cell(id_cell.row, 11, str(rbun_buyer))   # 購入者入力
            buyer_check = worksheet_list.cell(id_cell.row, 167).value
            # pp = int(worksheet_list.cell(id_cell.row, 9).value)
            dia = int(rbun_dia)
            id_check = list()
            cama_list = list()
            death_list = list()
            samurai_list = list()
            if buyer_check == '0':
                if pp < 10 and dia < 5000:
                    bunpa = dia / pp
                    if bunpa < 50:
                        dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                        dice_a = int(dice) + int(11)
                        ran_men = worksheet_list.cell(id_cell.row, int(dice_a)).value
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
                            id_col = int(num) + int(12)
                            await culc_channel.send('<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                            await asyncio.sleep(2)
                        #                    id_check = '\n'.join(id_check)
                        await culc_channel.send('finish')
                        return
                elif pp < 10 and dia >= 5000:
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
                        id_col = int(num) + int(12)
                        await culc_channel.send('<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>\n')
                        await asyncio.sleep(2)
                        #                    id_check = '\n'.join(id_check)
                    await culc_channel.send('finish')
                    return
                else:
                    if 10 <= pp < 25 and dia >= 5000:
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
                                id_col = int(num) + int(12)
                                await culc_channel.send(
                                    '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                                await asyncio.sleep(2)
                                #                    id_check = '\n'.join(id_check)
                            await culc_channel.send('finish')
                            # id_check = '\n'.join(id_check)

                        elif tema >= 500:
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
                                id_col = int(num) + int(12)
                                await culc_channel.send(
                                    '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                            # id_check = '\n'.join(id_check)
                            await culc_channel.send('finish!')
                        else:
                            await culc_channel.send('えろてろまで問い合わせを。')
                        return

                    elif 10 <= pp < 25 and dia < 5000:
                        tema = dia * 0.05
                        bunpb = (dia - tema) / pp
                        if bunpb < 50:
                            dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                            dice_a = int(dice) + int(11)
                            ran_men = worksheet_list.cell(id_cell.row, int(dice_a)).value
                            await culc_channel.send(
                                str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                    worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(
                                    worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n分配が50dia未満(' + str(
                                    math.floor(bunpb)) + 'dia/人)なので、抽選を行います。\n...抽選の結果、<@' + str(
                                    ran_men) + '> が当選！\n' + str(dia) + ' diaの取引をお願いします。')
                            return
                        else:
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
                                id_col = int(num) + int(12)
                                await culc_channel.send(
                                    '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>')
                            # id_check = '\n'.join(id_check)
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
                                await culc_channel.send('finish!')
                                return
                            else:
                                if not pp == reaction_num:
                                    await culc_channel.send(
                                        'Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                    return
                                cama_num = 0
                                death_num = 0
                                samurai_num = 0
                                await culc_channel.send('人数が多いため処理に数分時間がかかる場合があります。しばらくお待ちください。')
                                for num in range(pp):
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
                                await culc_channel.send('finish!')
                                return

                        elif pp >= 25 and dia < 5000:
                            # print('ここまできたよ')
                            bunpd = dia / pp
                            if bunpd < 100:
                                meishubun2 = dia / 3
                                await culc_channel.send(
                                    str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                        worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                        dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                         5).value) + 'と取引を行って下さい。\n25人以上で分配が100dia/人 未満なので全額血盟資金となります。\n' + str(
                                        math.floor(
                                            meishubun2)) + 'diaを各盟主に渡してください。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n分配者手数料はありません。\n\nfinish!')
                                return
                            else:
                                if not pp == reaction_num:
                                    await culc_channel.send(
                                        'Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                    return
                                cama_num = 0
                                death_num = 0
                                samurai_num = 0
                                for num in range(pp):
                                    id_col = int(num) + int(12)
                                    id_clan_posi = worksheet_id.find(
                                        str(worksheet_list.cell(id_cell.row, id_col).value))
                                    await asyncio.sleep(3)
                                    if id_clan_posi.col == 13:
                                        cama_list.append(
                                            '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>\n')
                                        cama_num = cama_num + 1
                                    elif id_clan_posi.col == 16:
                                        death_list.append(
                                            '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>\n')
                                        death_num = death_num + 1
                                    elif id_clan_posi.col == 19:
                                        samurai_list.append(
                                            '<@' + str(worksheet_list.cell(id_cell.row, id_col).value) + '>\n')
                                        samurai_num = samurai_num + 1
                                cama_list = '\n'.join(cama_list)
                                death_list = '\n'.join(death_list)
                                samurai_list = '\n'.join(samurai_list)
                                await culc_channel.send(
                                    str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                        worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                        dia) + ' diaで売れました。\n25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。')
                                cama_bun_total = bunpd * cama_num
                                death_bun_total = bunpd * death_num
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
                                await culc_channel.send('finish!')

                        else:
                            await culc_channel.send('えろてろまで問い合わせを。')
            elif buyer_check == '1':
                buyer_id = worksheet_list.cell(id_cell.row, 11).value
                await culc_channel.send('本案件は参加者に購入者を含む案件になります。違う場合は "えろてろ" までご連絡下さい')
                pp_a = pp - 1
                if pp < 10 and dia < 5000:
                    bunpa = dia / pp_a
                    if bunpa < 50:
                        dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                        dice_a = int(dice) + int(11)
                        ran_men = worksheet_list.cell(id_cell.row, int(dice_a)).value
                        if ran_men == buyer_id:
                            dice_retry = random.randint(1, pp)
                            while not dice == dice_retry:
                                dice_retry = random.randint(1, pp)
                            dice_a = int(dice_retry) + int(11)
                            ran_men = worksheet_list.cell(id_cell.row, int(dice_a)).value
                        await culc_channel.send(
                            str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                dia) + ' diaで売れたので分配を行います。\n' + str(
                                worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n分配が50dia未満(' + str(
                                math.floor(bunpa)) + 'dia/人)なので、抽選になります。\n抽選の結果、<@' + str(ran_men) + '> が当選！\n' + str(
                                dia) + ' diaの取引をお願いします。')
                        return
                    else:
                        if not pp == reaction_num:
                            await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                            return
                        await culc_channel.send(
                            str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                dia) + ' diaで売れました。\nメンションされている方々は以下に従い' + str(
                                worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n分配：' + str(
                                math.floor(bunpa)) + 'dia\n対象者')
                        for num in range(pp):
                            id_col = int(num) + int(12)
                            men = worksheet_list.cell(id_cell.row, id_col).value
                            if men == buyer_id:
                                #await culc_channel.send('購入者削除痕')
                                await asyncio.sleep(2)
                            else:
                                await culc_channel.send('<@' + str(men) + '>')
                                await asyncio.sleep(2)
                        #                    id_check = '\n'.join(id_check)
                        await culc_channel.send('finish')
                        return
                elif pp < 10 and dia >= 5000:
                    if not pp == reaction_num:
                        await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                        return
                    ketsu = dia * 0.03
                    bunpb = (dia - ketsu * 3) / (pp - 1)
                    await culc_channel.send(
                        str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                            worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                            dia) + ' diaで売れました。\nメンションされている方々は以下に従い' + str(
                            worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金として ' + str(
                            math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(math.floor(
                            bunpb)) + 'diaで出品して下さい。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
                    for num in range(pp):
                        id_col = int(num) + int(12)
                        men = worksheet_list.cell(id_cell.row, id_col).value
                        if men == buyer_id:
                            #await culc_channel.send('購入者削除痕')
                            await asyncio.sleep(2)
                        else:
                            await culc_channel.send('<@' + str(men) + '>\n')
                            await asyncio.sleep(2)
                        #                    id_check = '\n'.join(id_check)
                    await culc_channel.send('finish')
                    return
                else:
                    if 10 <= pp < 25 and dia >= 5000:
                        if not pp == reaction_num:
                            await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                            return
                        ketsu = dia * 0.03
                        tema = dia * 0.05
                        if tema < 500:
                            bunpb = (dia - ketsu * 3 - tema) / (pp - 1)
                            await culc_channel.send(
                                str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                    worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(
                                    worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金:' + str(
                                    math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(
                                    math.floor(bunpb)) + 'diaで出品して下さい。\nちなみに手間賃' + str(math.floor(
                                    tema)) + 'diaです。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
                            for num in range(pp):
                                id_col = int(num) + int(12)
                                men = worksheet_list.cell(id_cell.row, id_col).value
                                if str(men) == str(buyer_id):
                                    #await culc_channel.send('購入者削除痕')
                                    await asyncio.sleep(2)
                                else:
                                    await culc_channel.send('<@' + str(men) + '>\n')
                                    await asyncio.sleep(2)
                            await culc_channel.send('finish')
                            # id_check = '\n'.join(id_check)

                        elif tema >= 500:
                            if not pp == reaction_num:
                                await culc_channel.send('Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                return
                            tema = 500
                            bunpb = (dia - ketsu * 3 - tema) / (pp - 1)
                            await culc_channel.send(
                                str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                    worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(
                                    worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n血盟資金:' + str(
                                    math.floor(ketsu)) + 'diaを各盟主へ渡してください。\nメンションされている方々は ' + str(
                                    math.floor(bunpb)) + 'diaで出品して下さい。\nちなみに手間賃は上限の' + str(math.floor(
                                    tema)) + 'diaです。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n\n分配\n')
                            for num in range(pp):
                                id_col = int(num) + int(12)
                                men = worksheet_list.cell(id_cell.row, id_col).value
                                if str(men) == str(buyer_id):
                                    #await culc_channel.send('購入者削除痕')
                                    await asyncio.sleep(2)
                                else:
                                    await culc_channel.send('<@' + str(men) + '>\n')
                                    await asyncio.sleep(2)
                            await culc_channel.send('finish!')
                        else:
                            await culc_channel.send('えろてろまで問い合わせを。')
                        return

                    elif 10 <= pp < 25 and dia < 5000:
                        tema = dia * 0.05
                        bunpb = (dia - tema) / (pp - 1)
                        if bunpb < 50:
                            dice = random.randint(1, pp)  # サイコロを振る。出る目を指定。
                            dice_a = int(dice) + int(11)
                            ran_men = worksheet_list.cell(id_cell.row, int(dice_a)).value
                            await culc_channel.send(
                                str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                    worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                    dia) + ' diaで売れました。\n' + str(
                                    worksheet_list.cell(id_cell.row, 5).value) + 'と取引を行って下さい。\n分配が50dia未満(' + str(
                                    math.floor(bunpb)) + 'dia/人)なので、抽選を行います。\n...抽選の結果、<@' + str(
                                    ran_men) + '> が当選！\n' + str(dia) + ' diaの取引をお願いします。')
                            return
                        else:
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
                                id_col = int(num) + int(12)
                                men = worksheet_list.cell(id_cell.row, id_col).value
                                if str(men) == str(buyer_id):
                                    #await culc_channel.send('購入者削除痕')
                                    await asyncio.sleep(2)
                                else:
                                    await culc_channel.send('<@' + str(men) + '>\n')
                                    await asyncio.sleep(2)
                            await culc_channel.send('finish!')
                            return
                    else:
                        if pp >= 25 and dia >= 5000:
                            ketsushi = dia * 0.03
                            bunpc = (dia - ketsushi * 3) / (pp - 1)
                            if bunpc < 100:
                                meishubun1 = dia / 3
                                await culc_channel.send(
                                    str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                        worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                        dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                         5).value) + 'と取引を行って下さい。\n25人以上 / 分配 100dia未満なので全額血盟資金となります。\n３等分した' + str(
                                        math.floor(
                                            meishubun1)) + 'diaを各盟主に渡してください。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n分配者手数料はありません。')
                                await culc_channel.send('finish!')
                                return
                            else:
                                if not pp == reaction_num:
                                    await culc_channel.send(
                                        'Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                    return
                                cama_num = 0
                                death_num = 0
                                samurai_num = 0
                                await culc_channel.send('人数が多いため処理に数分時間がかかる場合があります。しばらくお待ちください。')
                                flag_del = 0
                                for num in range(pp):
                                    id_col = int(num) + int(12)
                                    id_clan_posi = worksheet_id.find(
                                        str(worksheet_list.cell(id_cell.row, id_col).value))
                                    # print(id_clan_posi.col)
                                    await asyncio.sleep(3)

                                    if id_clan_posi.col == 13:
                                        #   print('カマ')
                                        men = worksheet_list.cell(id_cell.row, id_col).value
                                        if men == buyer_id:
                                            #cama_list.append('<購入者削除痕>')
                                            flag_del = 1
                                        else:
                                            cama_list.append(
                                                '<@' + str(men) + '>')
                                            cama_num = cama_num + 1
                                    elif id_clan_posi.col == 16:
                                        #   print('デス')
                                        men = worksheet_list.cell(id_cell.row, id_col).value
                                        if men == buyer_id:
                                            #death_list.append('<購入者削除痕>')
                                            flag_del = 1
                                        else:
                                            death_list.append(
                                                '<@' + str(men) + '>')
                                            death_num = death_num + 1
                                    elif id_clan_posi.col == 19:
                                        #   print('サムライ')
                                        men = worksheet_list.cell(id_cell.row, id_col).value
                                        if men == buyer_id:
                                            #samurai_list.append('<購入者削除痕>')
                                            flag_del = 1
                                        else:
                                            samurai_list.append(
                                                '<@' + str(men) + '>')
                                            samurai_num = samurai_num + 1
                                cama_list = '\n'.join(cama_list)
                                death_list = '\n'.join(death_list)
                                samurai_list = '\n'.join(samurai_list)
                                bunpc = (dia - ketsushi * 3) / (pp - int(flag_del))
                                bun_cama = bunpc * cama_num + ketsushi
                                bun_death = bunpc * death_num + ketsushi
                                bun_samurai = bunpc * samurai_num + ketsushi
                                cama_at = (bun_cama - ketsushi) * 0.95 / cama_num
                                death_at = (bun_death - ketsushi) * 0.95 / death_num
                                samurai_at = (bun_samurai - ketsushi) * 0.95 / samurai_num

                                await culc_channel.send(
                                    str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                        worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                        dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                         5).value) + 'と取引を行って下さい。\n25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。\n尚、血盟資金 ' + str(
                                        math.floor(ketsushi)) + 'diaも含まれています。\n\n<@477504935727071232>さん： ' + str(
                                        math.floor(bun_cama)) + ' diaを受取り、以下の方に ' + str(
                                        math.floor(cama_at)) + ' diaを分配下さい。\n' + str(
                                        cama_list) + '\n\n<@363032621845839892>さん： ' + str(
                                        math.floor(bun_samurai)) + ' diaを受取り、以下の方に ' + str(
                                        math.floor(samurai_at)) + ' diaを分配下さい。\n' + str(
                                        samurai_list) + '\n\n<@290377448711782400>さん： ' + str(
                                        math.floor(bun_death)) + ' diaを受取り、以下の方に ' + str(
                                        math.floor(death_at)) + ' diaを分配下さい。\n ' + str(death_list))
                                await culc_channel.send('finish!')
                                return

                        elif pp >= 25 and dia < 5000:
                            # print('ここまできたよ')
                            bunpd = dia / (pp - 1)
                            if bunpd < 100:
                                meishubun2 = dia / 3
                                await culc_channel.send(
                                    str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                        worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                        dia) + ' diaで売れました。\n' + str(worksheet_list.cell(id_cell.row,
                                                                                         5).value) + 'と取引を行って下さい。\n25人以上で分配が100dia/人 未満なので全額血盟資金となります。\n' + str(
                                        math.floor(
                                            meishubun2)) + 'diaを各盟主に渡してください。\n血盟資金受取\n<@363032621845839892>\n<@477504935727071232>\n<@290377448711782400>\n分配者手数料はありません。\n\nfinish!')
                                return
                            else:
                                if not pp == reaction_num:
                                    await culc_channel.send(
                                        'Reaction数と登録数が違うのでまだ分配出来ません。\n<@592253165068615680>\n急いで確認よー！')
                                    return
                                cama_num = 0
                                death_num = 0
                                samurai_num = 0
                                for num in range(pp):
                                    id_col = int(num) + int(12)
                                    id_clan_posi = worksheet_id.find(
                                        str(worksheet_list.cell(id_cell.row, id_col).value))
                                    await asyncio.sleep(3)
                                    flag_del = 0
                                    if id_clan_posi.col == 13:
                                        #   print('カマ')
                                        men = worksheet_list.cell(id_cell.row, id_col).value
                                        if men == buyer_id:
                                            #cama_list.append('<購入者削除痕>')
                                            flag_del = 1
                                        else:
                                            cama_list.append(
                                                '<@' + str(men) + '>')
                                            cama_num = cama_num + 1
                                    elif id_clan_posi.col == 16:
                                        #   print('デス')
                                        men = worksheet_list.cell(id_cell.row, id_col).value
                                        if men == buyer_id:
                                            #death_list.append('<購入者削除痕>')
                                            flag_del = 1
                                        else:
                                            death_list.append(
                                                '<@' + str(men) + '>')
                                            death_num = death_num + 1
                                    elif id_clan_posi.col == 19:
                                        #   print('サムライ')
                                        men = worksheet_list.cell(id_cell.row, id_col).value
                                        if men == buyer_id:
                                            #samurai_list.append('<購入者削除痕>')
                                            flag_del = 1
                                        else:
                                            samurai_list.append(
                                                '<@' + str(men) + '>')
                                            samurai_num = samurai_num + 1
                                cama_list = '\n'.join(cama_list)
                                death_list = '\n'.join(death_list)
                                samurai_list = '\n'.join(samurai_list)
                                await culc_channel.send(
                                    str(rbun_id) + 'の' + str(worksheet_list.cell(id_cell.row, 2).value) + '/' + str(
                                        worksheet_list.cell(id_cell.row, 3).value) + ' が' + str(
                                        dia) + ' diaで売れました。\n25人以上 / 分配 100dia以上なので盟主が分配します。以下に従って盟主と取引して下さい。')
                                pp = pp - int(flag_del)
                                bunpd = dia / pp
                                cama_bun_total = bunpd * cama_num
                                death_bun_total = bunpd * death_num
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
        print(id_count)
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
            print(num)
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
            return
        worksheet_find = gc.open_by_key(SPREADSHEET_KEY).worksheet('rare(red,purple)')
        worksheet_id = gc.open_by_key(SPREADSHEET_KEY).worksheet('ID_LIST')
        worksheet_sell = gc.open_by_key(SPREADSHEET_KEY).worksheet('sell_list')
        id_count = worksheet_id.cell(6, 8).value
        await sell_channel.send('購入者が確定しました。以下一覧を参照の上、購入者は取引を開始して下さい。\nこれから読み込みますのでコマンドを打たずに少々お待ちください。')
        sell1_list = list()
        sell2_list = list()
        sell3_list = list()
        sell4_list = list()
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
                    sell1_list.append(id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : 見送り')
                elif sell_num == 2:
                    sell2_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : 見送り')
                elif sell_num == 3:
                    sell3_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : 見送り')
                elif sell_num == 4:
                    sell4_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : 見送り')
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
                    sell1_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                elif sell_num == 2:
                    sell2_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                elif sell_num == 3:
                    sell3_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                elif sell_num == 4:
                    sell4_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者 : ' + '<@' + buyer + '>')
                else:
                    await sell_channel.send('エラー発生。えろてろへ連絡を。')

            elif int(uid_count) >= 2:
                id = worksheet_sell.cell(sell_row, 1).value
                item = worksheet_sell.cell(sell_row, 3).value
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
                    sell1_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者(抽選勝者) : ' + '<@' + buyer + '>')
                elif sell_num == 2:
                    sell2_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者(抽選勝者) : ' + '<@' + buyer + '>')
                elif sell_num == 3:
                    sell3_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者(抽選勝者) : ' + '<@' + buyer + '>')
                elif sell_num == 4:
                    sell4_list.append(
                        id + '\t: ' + item + '\t/ ' + price + 'dia\n所持者 : ' + owner + '\n購入者(抽選勝者) : ' + '<@' + buyer + '>')
                else:
                    await sell_channel.send('エラー発生。えろてろへ連絡を。')
        sell1_list = '\n------------------\n'.join(sell1_list)
        sell2_list = '\n------------------\n'.join(sell2_list)
        sell3_list = '\n------------------\n'.join(sell3_list)
        sell4_list = '\n------------------\n'.join(sell4_list)
        await par_msg.edit(content='progress...100%')
        sell1_r = discord.Embed(title='第1回販売結果',
                                description='以下の方々は取引を開始して下さい。',
                                color=discord.Colour.red())
        sell1_r.add_field(name='-----', value=str(sell1_list), inline=True)
        await sell_channel.send(embed=sell1_r)
        sell2_r = discord.Embed(title='第2回販売結果',
                                description='以下の方々は取引を開始して下さい。',
                                color=discord.Colour.red())
        sell2_r.add_field(name='-----', value=str(sell2_list), inline=True)
        await sell_channel.send(embed=sell2_r)
        sell3_r = discord.Embed(title='第3回販売結果',
                                description='以下の方々は取引を開始して下さい。',
                                color=discord.Colour.red())
        sell3_r.add_field(name='-----', value=str(sell3_list), inline=True)
        await sell_channel.send(embed=sell3_r)
        sell4_r = discord.Embed(title='第4回販売結果',
                                description='以下の方々は取引を開始して下さい。',
                                color=discord.Colour.red())
        sell4_r.add_field(name='-----', value=str(sell4_list), inline=True)
        await sell_channel.send(embed=sell4_r)

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

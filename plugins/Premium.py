
import pytz
import datetime
from Script import script 
from info import *
from utils import get_seconds, temp
from database.users_chats_db import db 
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import *


@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("ᴜꜱᴇʀ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ !")
            await client.send_message(
                chat_id=user_id,
                text=script.PREMIUM_END_TEXT.format(user.mention)
            )
        else:
            await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴜꜱᴇᴅ !\nᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ, ɪᴛ ᴡᴀꜱ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ɪᴅ ?")
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /remove_premium user_id") 


@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    try:
        user = message.from_user.mention
        user_id = message.from_user.id
        data = await db.get_user(user_id)

        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time")
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")

            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ"

            caption = (
                f"⚜️ <b>ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :</b>\n\n"
                f"👤 <b>ᴜꜱᴇʀ :</b> {user}\n"
                f"⚡ <b>ᴜꜱᴇʀ ɪᴅ :</b> <code>{user_id}</code>\n"
                f"⏰ <b>ᴛɪᴍᴇ ʟᴇꜰᴛ :</b> {time_left_str}\n"
                f"⌛️ <b>ᴇxᴘɪʀʏ ᴅᴀᴛᴇ :</b> {expiry_str_in_ist}"
            )

            await message.reply_photo(
                photo=SUBSCRIPTION, 
                caption=caption,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔥 ᴇxᴛᴇɴᴅ ᴘʟᴀɴ", callback_data="premium_back")]]
                )
            )
        else:
            await message.reply_photo(
                photo="https://i.ibb.co/gMrpRQWP/photo-2025-07-09-05-21-32-7524948058832896004.jpg", 
                caption=(
                    f"<b>ʜᴇʏ {user},\n\n"
                    f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ.\n"
                    f"ʙᴜʏ ᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴊᴏʏ ᴘʀᴇᴍɪᴜᴍ ʙᴇɴᴇꜰɪᴛꜱ.</b>"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("💎 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ", callback_data='premium_back')]]
                )
            )
    except Exception as e:
        print(e)

@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)  
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}")
        else:
            await message.reply_text("ɴᴏ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ᴏꜰ ᴛʜᴇ ᴡᴀꜱ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ !")
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /get_premium user_id")

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p") 
        user_id = int(message.command[1])  
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  
            await db.update_user(user_data) 
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")         
            await message.reply_text(f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"👋 ʜᴇʏ {user.mention},\nᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.\nᴇɴᴊᴏʏ !! ✨🎉\n\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True              
            )    
            await client.send_message(PREMIUM_LOGS, text=f"#Added_Premium\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True)
                    
        else:
            await message.reply_text(
                "❌ ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ꜰᴏʀᴍᴀᴛ ❗\n"
                "🕒 ᴘʟᴇᴀsᴇ ᴜsᴇ: <code>1 day</code>, <code>1 hour</code>, <code>1 min</code>, <code>1 month</code>, or <code>1 year</code>"
            )
    else:
        await message.reply_text(
            "📌 ᴜsᴀɢᴇ: <code>/add_premium user_id time</code>\n"
            "📅 ᴇxᴀᴍᴘʟᴇ: <code>/add_premium 123456 1 month</code>\n"
            "🧭 ᴀᴄᴄᴇᴘᴛᴇᴅ ꜰᴏʀᴍᴀᴛs: <code>1 day</code>, <code>1 hour</code>, <code>1 min</code>, <code>1 month</code>, <code>1 year</code>"
            )

@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("<i>ꜰᴇᴛᴄʜɪɴɢ...</i>")
    new = f" ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ ʟɪꜱᴛ :\n\n"
    user_count = 1
    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"	 
            new += f"{user_count}. {(await client.get_users(user['id'])).mention}\n👤 ᴜꜱᴇʀ ɪᴅ : {user['id']}\n⏳ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n"
            user_count += 1
        else:
            pass
    try:    
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Paid Users:")


@Client.on_message(filters.command("plan") & filters.private)
async def plan_command(client, message):
    try:
        user_id = message.from_user.id
        user_mention = message.from_user.mention
        
        # Dynamic Buttons Generator
        buttons = []
        for price, name in PREMIUM_PLANS.items():
            buttons.append([
                InlineKeyboardButton(f"💎 {name} - ₹{price}", callback_data=f"pay_{price}_{name}")
            ])
        
        buttons.append([InlineKeyboardButton('• ʀᴇꜰᴇʀ ꜰʀɪᴇɴᴅꜱ', callback_data='reffff'), InlineKeyboardButton('ꜰʀᴇᴇ ᴛʀɪᴀʟ •', callback_data='free')])
        buttons.append([InlineKeyboardButton('🚫 ᴄʟᴏꜱᴇ 🚫', callback_data='close_data', style=enums.ButtonStyle.DANGER)])

        # Reply with Photo
        msg = await message.reply_photo(
            photo=SUBSCRIPTION,
            caption=script.BPREMIUM_TXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        # Admin Logs
        log_txt = f"<b>🚫 ᴜsᴇʀ ᴄʜᴇᴄᴋᴇᴅ /plan</b>\n\n- ɪᴅ: `{user_id}`\n- ɴᴀᴍᴇ: {user_mention}"
        await client.send_message(PREMIUM_LOGS, log_txt)

        # Auto-delete after 5 mins
        await asyncio.sleep(300)
        try:
            await msg.delete()
            await message.delete()
        except:
            pass
            
    except Exception as e:
        logging.error(f"Error in plan command: {e}")

# --- 2. PAYMENT SELECTION (EDIT MESSAGE) ---
@Client.on_callback_query(filters.regex(r"pay_\d+"))
async def payment_selection(client, query: CallbackQuery):
    try:
        # Extract Price and Plan Name from callback
        data = query.data.split("_")
        price = data[1]
        plan_name = data[2]

        # Payment Buttons
        btns = [
            [InlineKeyboardButton("📸 sᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ", url=OWNER_LNK)],
            [InlineKeyboardButton("« ʙᴀᴄᴋ ᴛᴏ ᴘʟᴀɴs", callback_data="premium_back")]
        ]

        payment_caption = (
            f"✅ <b>ᴘʟᴀɴ sᴇʟᴇᴄᴛᴇᴅ: {plan_name}</b>\n"
            f"💰 <b>ᴘᴀʏᴀʙʟᴇ ᴀᴍᴏᴜɴᴛ: ₹{price}</b>\n\n"
            f"Sᴄᴀɴ QR ᴏʀ Pᴀʏ ᴛᴏ: <code>{OWNER_UPI_ID}</code>\n\n"
            "🏁 <b>Iᴍᴘᴏʀᴛᴀɴᴛ:</b> Payment karne ke baad screenshot niche button par click karke Admin ko bhejein."
        )

        # Edit Current Message with QR and Details
        await query.edit_message_media(
            media=InputMediaPhoto(media=PAYMENT_QR, caption=payment_caption),
            reply_markup=InlineKeyboardMarkup(btns)
        )
        await query.answer(f"Selected: ₹{price}", show_alert=False)

    except Exception as e:
        logging.error(f"Error in payment selection: {e}")

# --- 3. BACK TO PLANS (EDIT BACK) ---
@Client.on_callback_query(filters.regex("premium_back"))
async def back_to_plans(client, query: CallbackQuery):
    try:
        buttons = []
        for price, name in PREMIUM_PLANS.items():
            buttons.append([InlineKeyboardButton(f"💎 {name} - ₹{price}", callback_data=f"pay_{price}_{name}")])
        
        buttons.append([InlineKeyboardButton('• ʀᴇꜰᴇʀ ꜰʀɪᴇɴᴅꜱ', callback_data='reffff'), InlineKeyboardButton('ꜰʀᴇᴇ ᴛʀɪᴀʟ •', callback_data='free')])
        buttons.append([InlineKeyboardButton('🚫 ᴄʟᴏꜱᴇ 🚫', callback_data='close_data', style=enums.ButtonStyle.DANGER)])

        await query.edit_message_media(
            media=InputMediaPhoto(media=SUBSCRIPTION, caption=script.BPREMIUM_TXT),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logging.error(f"Error in back_to_plans: {e}")

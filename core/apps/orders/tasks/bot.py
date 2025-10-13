import telebot
from telebot import types
from django.conf import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)

accepted_orders = {}  # {order_id: telegram_user_id}


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "accept_order":
        if call.message.message_id in accepted_orders:
            bot.answer_callback_query(call.id, "❌ Bu buyurtma allaqachon olingan.")
            return

        accepted_orders[call.message.message_id] = call.from_user.id

        text = (
            f"✅ Buyurtma olindi @{call.from_user.username} tomonidan.\n"
            f"❌ Bekor qilishni faqat shu foydalanuvchi bosishi mumkin."
        )

        # ✅ InlineKeyboardMarkup ishlatamiz
        buttons = types.InlineKeyboardMarkup()
        cancel_button = types.InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_order")
        buttons.add(cancel_button)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=text,
                              reply_markup=buttons)
        bot.answer_callback_query(call.id, "Buyurtma sizga biriktirildi ✅")

    elif call.data == "cancel_order":
        owner_id = accepted_orders.get(call.message.message_id)
        if owner_id != call.from_user.id:
            bot.answer_callback_query(call.id, "❌ Siz bu buyurtmani bekor qila olmaysiz.")
            return

        del accepted_orders[call.message.message_id]
        text = f"🚫 Buyurtma @{call.from_user.username} tomonidan bekor qilindi."
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=text)
        bot.answer_callback_query(call.id, "Buyurtma bekor qilindi ❌")


bot.infinity_polling()

import telebot
from telebot import types
import requests
from django.conf import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)

API_BASE_URL = settings.API_BASE_URL  # masalan: "https://yourdomain.uz/api/v1/orders/"
accepted_orders = {}  # {order_id: telegram_user_id}


@bot.callback_query_handler(func=lambda call: call.data.startswith(("accept_", "cancel_")))
def handle_order_actions(call):
    action, order_id = call.data.split("_")
    order_id = int(order_id)

    if action == "accept":
        if order_id in accepted_orders:
            bot.answer_callback_query(call.id, "❌ Bu buyurtma allaqachon olingan.")
            return

        accepted_orders[order_id] = call.from_user.id

        # ✅ backenddagi statusni o‘zgartirish
        try:
            requests.patch(f"{API_BASE_URL}{order_id}/", json={"status": "accepted"})
        except Exception as e:
            print("API xato:", e)

        text = (
            f"✅ Buyurtma olindi @{call.from_user.username} tomonidan.\n"
            f"❌ Bekor qilishni faqat shu foydalanuvchi bosishi mumkin."
        )
        buttons = types.InlineKeyboardMarkup()
        cancel_btn = types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"cancel_{order_id}")
        buttons.add(cancel_btn)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=buttons)
        bot.answer_callback_query(call.id, "Buyurtma sizga biriktirildi ✅")

    elif action == "cancel":
        owner_id = accepted_orders.get(order_id)
        if owner_id != call.from_user.id:
            bot.answer_callback_query(call.id, "❌ Siz bu buyurtmani bekor qila olmaysiz.")
            return

        del accepted_orders[order_id]

        # ✅ backenddagi statusni yangilash
        try:
            requests.patch(f"{API_BASE_URL}{order_id}/", json={"status": "cancelled"})
        except Exception as e:
            print("API xato:", e)

        text = f"🚫 Buyurtma @{call.from_user.username} tomonidan bekor qilindi."
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "Buyurtma bekor qilindi ❌")


bot.infinity_polling()

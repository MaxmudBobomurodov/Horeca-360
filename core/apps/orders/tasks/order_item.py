import requests
from celery import shared_task
from django.conf import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
GROUP_CHAT_ID = settings.TELEGRAM_GROUP_ID  # Guruh chat_id sini .env dan ol

@shared_task
def send_orders_to_tg_bot(chat_id, order_id, product_name, quantity, username, object_name=None, price=None):
    """
    Telegramga buyurtma haqida xabar yuboradi
    """
    # 🔢 Miqdorni tozalash
    if float(quantity).is_integer():
        quantity = int(quantity)

    # Text formatlash
    text = f"🆕 *Yangi buyurtma*\n" \
           f"👤 Foydalanuvchi: @{username}\n" \
           f"📦 Mahsulot: {product_name}\n" \
           f"🔢 Miqdor: {quantity}\n"

    if object_name:
        text += f"📦 Ob'ekt: {object_name}\n"
    elif price:
        text += f"💰 Narx: {price}\n"

    text += "\nQuyidagi tugmadan birini tanlang 👇"

    buttons = {
        "inline_keyboard": [
            [{"text": "✅ Buyurtmani olish", "callback_data": f"accept_{order_id}"}]
        ]
    }

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": buttons
    })




@shared_task
def send_message_order_user(chat_id, order_id):
    text = f"✅ Buyurtmangiz raqami: {order_id}\nBuyurtma muvaffaqiyatli yaratildi!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })

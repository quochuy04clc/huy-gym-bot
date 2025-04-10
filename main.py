import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- Config ---
API_TOKEN = '7020009714:AAG8zM9irHvbLEBom5NpJFt21S7PLnyGlCQ'
CHAT_ID = 5575195990  # Chat ID của anh

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# --- Messages ---
def daily_workout():
    return "💪 HUY_GYM_PT: Bài tập hôm nay: Toàn thân, chú trọng form chuẩn, thời lượng 40-60 phút! Đừng quên khởi động trước khi tập nhé anh!"

def drink_water():
    return "💧 Nhắc nhở nhẹ: Uống nước đi anh ơi, giữ cơ thể luôn đủ nước để tập hiệu quả hơn!"

def meal_reminder(meal):
    return f"🍽️ Đến giờ ăn {meal} rồi anh ơi! Nạp năng lượng đầy đủ nha."

def sleep_reminder():
    return "🌙 Anh ơi, đã đến giờ đi ngủ để phục hồi cơ bắp và giảm mỡ hiệu quả hơn nhé! Chúc anh ngủ ngon."

def sunday_cardio():
    return "🎶 Hôm nay là Chủ nhật, tới giờ khiêu vũ đốt mỡ nhẹ nhàng rồi anh ơi! 2 tiếng vui khỏe nha."

def recovery_tip():
    return "🧘‍♂️ Hồi phục sau khiêu vũ: Uống nước, giãn cơ nhẹ và nghỉ ngơi nhé anh! Tuyệt vời!"

def weekly_summary():
    return "📊 Tổng kết tuần: Anh đã hoàn thành lịch tập rất tốt! Giữ vững phong độ nha 💪"

def daily_nutrition_tip():
    return "🥗 Mẹo dinh dưỡng hôm nay: Bổ sung đủ protein và rau xanh để hỗ trợ tăng cơ anh nhé!"

# --- Scheduler jobs ---
async def send_message(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def setup_scheduler():
    scheduler.add_job(send_message, 'cron', hour=6, minute=30, args=[drink_water()])
    scheduler.add_job(send_message, 'cron', hour=7, minute=0, args=[meal_reminder('sáng')])
    scheduler.add_job(send_message, 'cron', hour=8, minute=30, args=[drink_water()])
    scheduler.add_job(send_message, 'cron', hour=12, minute=0, args=[meal_reminder('trưa')])
    scheduler.add_job(send_message, 'cron', hour=13, minute=30, args=[drink_water()])
    scheduler.add_job(send_message, 'cron', hour=15, minute=0, args=[drink_water()])
    scheduler.add_job(send_message, 'cron', hour=16, minute=0, args=[daily_workout()])
    scheduler.add_job(send_message, 'cron', hour=18, minute=30, args=[meal_reminder('tối')])
    scheduler.add_job(send_message, 'cron', hour=20, minute=30, args=[drink_water()])
    scheduler.add_job(send_message, 'cron', hour=21, minute=30, args=["🧘‍♂️ Chuẩn bị thư giãn và đi ngủ anh nha!"])
    scheduler.add_job(send_message, 'cron', hour=22, minute=0, args=[sleep_reminder()])
    scheduler.add_job(send_message, 'cron', day_of_week='sun', hour=15, minute=0, args=[sunday_cardio()])
    scheduler.add_job(send_message, 'cron', day_of_week='sun', hour=17, minute=30, args=[recovery_tip()])
    scheduler.add_job(send_message, 'cron', day_of_week='sun', hour=20, minute=0, args=[weekly_summary()])
    scheduler.add_job(send_message, 'cron', hour=9, args=[daily_nutrition_tip()])
    scheduler.start()

# --- Command handler ---
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Xin chào anh! Em là HUY_GYM_PT, huấn luyện viên cá nhân của anh đây 💪 Em sẽ đồng hành cùng anh mỗi ngày để đạt mục tiêu nhé!")
    await message.answer(f"Chat ID của anh là: {message.chat.id}\nEm đã lưu lại để gửi bài tập mỗi ngày cho anh nhé!")
    await setup_scheduler()

# --- Main ---
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

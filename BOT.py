import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# تكوين سجل التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# تعيين مفاتيح OpenAI API
openai.api_key = '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'  # قم بتعيين مفتاح API الخاص بك هنا

# تعريف وظيفة لمعالجة أمر البدء
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('مرحبًا! أنا سويبر GPT')

# تعريف وظيفة لمعالجة الرسائل النصية
def generate_response(update: Update, context: CallbackContext) -> None:
    """Generate a response using the ChatGPT model."""
    message = update.message.text
    response = generate(message)
    update.message.reply_text(response)

def generate(message: str) -> str:
    """Generate a response using the ChatGPT model."""
    # إعداد النص لتوليد استجابة
    input_text = f"User: {message}\nAI:"

    # استعلام نموذج ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=input_text,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
    )

    # استخراج النص المقترح من الاستجابة
    generated_text = response.choices[0].text.strip()

    # إرجاع النص المقترح كاستجابة
    return generated_text

def main() -> None:
    # إعداد التحديث والمسجل
    updater = Updater("5924352518:AAENdIaL5tmPTFo0UkO2gbIPabCXNjzyFTM")  # قم بتعيين توكن البوت الخاص بك هنا

    # الحصول على معرف المسجل
    dp = updater.dispatcher

    # تعيين معالج الأوامر
    dp.add_handler(CommandHandler("start", start))

    # تعيين معالج الرسائل النصية
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_response))

    # تشغيل البوت
    updater.start_polling()

    # الاستماع حتى الضغط على Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
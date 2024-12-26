from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F
import app.kbds as kb

user = Router()


GUIDE_FILE_ID = None


async def setup_file_id(message: Message):
    global GUIDE_FILE_ID
    file_path = "media/Новогодние рецепты.pdf"
    try:
        document = FSInputFile(file_path)
        msg = await message.answer_document(document)
        GUIDE_FILE_ID = msg.document.file_id  

        await message.answer(f"file_id успешно получен: {GUIDE_FILE_ID}")
    except FileNotFoundError:
        await message.answer(f"Файл не найден по пути: {file_path}")
    except Exception as e:
        await message.answer(f"Ошибка при загрузке файла: {e}")


@user.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработчик команды /start. Приветствие и предложение получить гайд.
    """
    global GUIDE_FILE_ID

    if not GUIDE_FILE_ID:
        await setup_file_id(message)
        return  


    await message.answer_photo(
        photo=FSInputFile('media/IMG_2235.PNG'),
        caption=(
            "<b>👋 Добро пожаловать в сообщество доказательных нутрициологов Казахстана!</b>\n\n"
            "<i>📚 Только научная информация о питании.</i>\n\n"
            "Нажмите кнопку ниже, чтобы получить гайд:\n\n"
            "<b>⬇️ ГАЙД 📄</b>"
        ),
        parse_mode="HTML",
        reply_markup=kb.main
    )


@user.callback_query(F.data == "get_guide")
async def send_guide(callback_query: CallbackQuery):

    global GUIDE_FILE_ID

    if GUIDE_FILE_ID:
        try:
            await callback_query.message.answer_document(
                document=GUIDE_FILE_ID,
                caption="Вот ваш гайд 📄"
            )
        except Exception as e:
            await callback_query.message.answer(
                f"Ошибка при отправке файла: {e}"
            )
    else:
        await callback_query.message.answer(
            "file_id еще не инициализирован. Попробуйте снова."
        )

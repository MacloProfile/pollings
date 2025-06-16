import io
import os.path
import pandas as pd
from aiogram import Router, types, F
from aiogram.types import FSInputFile, BufferedInputFile
import matplotlib.pyplot as plt
import seaborn as sns
import numpy
from logic.questions import QUESTIONS
from logic.user.save_to_excel import get_results, RESULTS_FILE
from logic.keyboards.menu_key import admin_menu
router = Router()

@router.callback_query(F.data == "get_results")
async def get_results_for_month(callback: types.CallbackQuery, state: FSMContext):
    results = get_results()
    current_state = await state.get_state()

    if os.path.getsize(RESULTS_FILE) > 0:
        await callback.message.answer_document(document=FSInputFile(RESULTS_FILE,filename="all_results.xlsx"), caption="Для более подробных результатов ознакомтесь с Excel-файлом")

    if not results:
        await callback.answer("Результаты опроса за текущий месяц пусты.")
        return

    questions = QUESTIONS['Пройти опрос']['1_to_5']
    question_answers = {}
    for q in questions:
        question_answers[q] = []
    flag = 0
    for r in results:
        if(len(questions) < len(r)):
            flag = 1
            break

    if(flag):
     for r in results:
        if(len(questions) < len(r)):
            for i, q in enumerate(questions):
                value = r.get(list(r.keys())[i + 3], None)
                if value is not None and pd.notna(value) and isinstance(value, (int, float)):
                    question_answers[q].append(int(value))



     q_averages = {}
     for q,a in question_answers.items():
         q_averages[q] = numpy.mean([i for i in a if isinstance(i,(int,float))])

     keys = list(q_averages.keys())
     values = list(q_averages.values())

     sns.set_theme(style='whitegrid', palette='pastel')
     plt.figure(figsize=(12,6))
     plt.bar(keys, values, color='green')
     plt.xlabel("Вопросы")
     plt.ylabel("Среднее значение")
     plt.title("Средние значения ответов на вопросы (за текущий месяц)")
     plt.xticks(rotation=45,ha='right',fontsize=8)
     plt.tight_layout()


     img_stream = io.BytesIO()
     plt.savefig(img_stream, format='png')
     img_stream.seek(0)
     plt.close()
     with open("bar_chart.png", "wb") as f:
        f.write(img_stream.getvalue())


     await callback.message.answer_photo(photo=FSInputFile("bar_chart.png"), caption="Средние значения ответов на вопросы (за текущий месяц)")
    await callback.message.answer("Выберите действие:", reply_markup=admin_menu())
    await callback.answer()



@router.callback_query(F.data == "clear_results")
async def clear_results(callback: types.CallbackQuery):
    if os.path.getsize(RESULTS_FILE) > 0:
        await callback.message.answer_document(document=FSInputFile(RESULTS_FILE,filename="all_results.xlsx"), caption="Результаты опроса (Excel-файл)")
        with open(RESULTS_FILE, 'w'):
            pass
        await callback.message.answer("Результаты очищены.", reply_markup=admin_menu())
    else:
        await callback.message.answer("Файл результатов пуст.", reply_markup=admin_menu())



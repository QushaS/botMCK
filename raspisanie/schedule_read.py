import urllib
import requests
import json
from xlrd import open_workbook

parts = ('ИКиМ', 'ИПиС', 'ПОиСПА', 'ЭУиК')

"""folder_url = 'https://disk.yandex.ru/d/Xc08g8WbTavdHQ'

for i in parts:
    file_url = f'10.06.2023/{i}.xls'
    url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download' + '?public_key=' + urllib.parse.quote(
        folder_url) + '&path=/' + urllib.parse.quote(file_url)

    print(requests.get(url).text)

    with open(f'{i}.xls', 'wb') as file:
        req = requests.get(h)
        file.write(req.content)
        file.flush()"""

# Основной класс для работы с расписанием, чтение и парсинг
class ParseSchedule():

    def read_schedule(self):

        self.schedule_dict = {}
        for part in parts:
            wb = open_workbook(f'resources/{part}.xls', on_demand=True)
            indexes = wb.nsheets
            for sheet_n in range(indexes):
                sheet = wb.sheet_by_index(sheet_n)
                step = 3
                for list in range(int((sheet.ncols - 3) / 3)):
                    group = sheet.cell(7, step)
                    info = []
                    for lessons in range(6):
                        lesson_step = 8 + lessons
                        if sheet.cell(lesson_step, step).ctype == 0:
                            continue
                        print(group.value, sheet.cell(lesson_step, step).ctype)
                        info.append({lessons + 1 : (sheet.cell(lesson_step, step).value,
                                                    sheet.cell(lesson_step, step + 2).value,
                                                    sheet.cell(lesson_step, step - 1).value,
                                                    sheet.cell(lesson_step, step + 1).value)})
                        step += 3
                        self.schedule_dict[group.value] = info

        return self.schedule_dict

a = ParseSchedule()
a.read_schedule()
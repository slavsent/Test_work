import pygsheets


def parsing_log(file_sheet, file_log):
    """
    данных по примеру лога amo crm у меня нет. Из условий теста не понятно нужно ли проверять
    файл, что он сделан большим днем чем предыдущий и не ясно от куда его брать
    поэтому за основу взять, что каждый день запускается этот скрипт с указанием
    файла с данными google таблицы и новым лог файлом
    :param file_sheet: Файл с google таблицой
    :param file_log: Log файл
    :return: Данные с log файла заносятся в следующую свободную ячейку
    """
    try:
        gc = pygsheets.authorise()
        sh = gc.open(file_sheet)
    except Exception:
        print(f'Что-то с файлом: {file_sheet} не так, не возможно его открыть!')
        return
    else:
        row_name = 'A'
        column_num = 1
        while True:
            if sh.sheet1.get(row_name+str(column_num)) != '':

                if column_num > 365: # пусть есть проверка что в строку заносятся только данные за один год
                    row_name = chr(ord(row_name) + 1)
                    # дальше отдельная функцию лучше сделать для двойных и тройных букв
                else:
                    column_num += 1
            else:
                try:
                    with open(file_log, 'r', encoding='utf-8') as open_file:
                        content = open_file.read()
                        sh.sheet1.update_cells((row_name + str(column_num)), content)

                except FileNotFoundError:
                    print(f'Логфайл - {file_log} не найден')
                    return
                else:
                    gc.close(file_sheet)
                    break



if __name__ == '__main__':
    test_sheet = "my_sheet"
    file_log = 'amolog_20122022.log'
    parsing_log(test_sheet, file_log)

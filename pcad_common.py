#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Модуль pcad_common.py общих параметров всех модулей программы. """

#                Автор: Л.М.Матвеев

from common import printm

from os.path import splitext, split, join, exists, isdir
from      os import remove, rename, listdir
from  shutil import copy2
import re
import radio_component

pcad_code = 'cp1251'  # Кодировка исходного PCB файла
pcad_linesep = '\r\n'

# Если нет входной ЕИ, то копировать в ЕИ имеющуюся точку
EI_CONST = {
'R': {
     'range_out': (1e9, 1e6, 1e3, 0., ),
     'mults_out': (1e9, 1e6, 1e3, 1., ),
     'units_out': (' ГОм', ' МОм', ' кОм', ' Ом', ),
      'mults_in': (1., 1e3, 1e6, ),
      'units_in': ({'', '.', 'r', 'e', 'е', 'ом', 'ohm', 'om', },
                    {'k', 'к', 'ком', 'kohm', 'kom', },
                    {'m', 'м', 'мом', 'mohm', 'mom', }, ), },
'C': {
     'range_out': (1e-8, 0., ),     # 1e-9,
     'mults_out': (1e-6, 1e-12, ),  # 1e-9,
     'units_out': (' мкФ', ' пФ', ),  # ' нФ', ' мФ', ),
      'mults_in': (1e-12, 1e-9, 1e-6, 1e-3, ),
      'units_in': ({'', 'p', 'п', 'пф', 'pf', },
                    {'n', 'н', 'нф', 'nf', },
                    {'.', '', 'мк', 'мкф', 'uf', },
                    {'m', 'м', 'мф', 'mf', }, ), },
'L': {
     'range_out': (1., 1e-3, 0., ),
     'mults_out': (1., 1e-3, 1e-6, ),
     'units_out': (' Гн', ' мГн', ' мкГн', ),
      'mults_in': (1e-9, 1e-6, 1e-3, 1., ),
      'units_in': ({'n', 'н', 'нг', 'нгн', 'nh', 'nhn', },
                    {'', 'мк', 'мкг', 'мкгн', 'uh', 'uhn', },
                    {'m', 'м', 'мг', 'мгн', 'mh', 'mhn', },
                    {'г', 'гн', 'h', 'hn', }, ), },
'p': {
     'range_out': (0., ),
     'mults_out': (1., ),
     'units_out': ('%', ),
      'mults_in': (1., ),
      'units_in': ({'%', }, ), },
'v': {
     'range_out': (0., ),
     'mults_out': (1., ),
     'units_out': ('В', ),
      'mults_in': (1., ),
      'units_in': ({'v', 'в', 'b'}, ), },
'w': {
     'range_out': (0., ),
     'mults_out': (1., ),
     'units_out': ('Вт', ),
      'mults_in': (1e-3, 1., ),
      'units_in': ({'mw', 'мвт'},
                    {'w', 'вт', 'bt'}, ), },
'Q': {
     'range_out': (1e9, 1e6, 1e3, 0., ),
     'mults_out': (1e9, 1e6, 1e3, 1., ),
     'units_out': (' ГГц', ' МГц', ' кГц', ' Гц', ),
      'mults_in': (1e9, 1e6, 1e3, 1., ),
      'units_in': ({'ghz', 'ggz', 'ггц'},
                    {'mhz', 'mgz', 'мгц'},
                    {'khz', 'kgz', 'кгц'},
                    {'hz', 'gz', 'гц'}, ), },
'i': {
     'range_out': (1., 1e-3, 0., ),
     'mults_out': (1., 1e-3, 1e-6, ),
     'units_out': ('А', 'мА', 'мкА', ),
      'mults_in': (1e-6, 1e-3, 1., ),
      'units_in': ({'мка', 'ua', },
                    {'ма', 'ma', },
                    {'а', 'a', }, ), }, }

avt_rdes = {'R', 'C', 'L', 'Q', }

dop_ei = ('p',) + tuple(set(EI_CONST) - avt_rdes - set(['p']))

#==============================================================================
exts = {"PCB": {'pr_fn': "PCB", 'pr_name': 'PCB'},  # 'pr_fpne': '',
        "SCH": {'pr_fn': "SCH", 'pr_name': 'Schematic'},
        "LIB": {'pr_fn': "CMP"},
        "LIA": {'pr_fn': "CMP", 'pr_name': 'Library Executive'},
        #"PY": {'pr_fn': "CMP", 'pr_name': 'Library Executive'}
        }

pcad_path = None

#------------------------------------------------------------------------------
def search_for_files_path(begin_paths, end_path_fsiles, search_depth):
    for i in range(search_depth):
        for begin_path in begin_paths:  # Проверка, нет ли ПКАД-а в указ папках
            for end_path_fsile in end_path_fsiles:
                if not exists(join(begin_path, end_path_fsile)):
                    break
            else:  # Все файлы есть
                return begin_path
        # Если не нашли на этом уровне вложености, поищем ещё глубже
        # Строим список вложенных папок
        begin_paths = [join(begin_path, p)
            for begin_path in begin_paths
                if exists(begin_path)
                    for p in listdir(begin_path)
                        if isdir(join(begin_path, p))]
    return None


#------------------------------------------------------------------------------
def complete_exts():
    """ Дополняет словарь расширений ПКАД-файлов
    полными именами соответствующих программ """
    global pcad_path

    #drives = ['%s:\\' % d for d in 'CDEF' if exists('%s:' % d)] + ['/media', '?']
    drives = ['C:\\', 'D:\\', 'E:\\', 'F:\\', '/media', '?']
    files = ['P-CAD 2006/%s.EXE' % fn for fn in ('PCB', 'SCH', 'CMP')]
    path = search_for_files_path(drives, files, 3)

    if path:
        pcad_path = join(path, r'P-CAD 2006')
        printm('\n  ПКАД-exe-файлы найдены в:\n"%s"\n\n' % pcad_path)
    else:
        printm('  ПКАД-exe-файлы на дисках НЕ НАЙДЕНЫ.\n')

#..............................................................................
complete_exts()

ww = [{}, {}]
# 'ext', 'fpne', 'fpn', 'compInst', 'net'


#------------------------------------------------------------------------------
def ind_sch_pcb():
    """ Возвращает индексы файлов по расширению. """
    i_sch, i_pcb = -1, -1
    for i in range(2):
        if ww[i].get('ext') == "SCH":
            i_sch = i
        elif ww[i].get('ext') == "PCB":
            i_pcb = i
    return i_sch, i_pcb
#..............................................................................


#------------------------------------------------------------------------------
def fields_count(field):
    """ Возвращает количество ПКАД-файлов из которых извлечены соотв поля. """
    n = 0
    for i in range(2):
        if field in ww[i]:
            n += 1
    return n
#..............................................................................


#------------------------------------------------------------------------------
def ReadFile(fpne, i):
    """ Считывает ПКАД-файл в список. """

    if not fpne:
        return

    fpn, ext = splitext(fpne)
    ext = ext[1:].upper()

    #get_elem_cp.comps = []
    ww[i] = {}
    ww[i]['ext'] = ext
    ww[i]['fpne'] = fpne
    ww[i]['fpn'] = fpn

    printm('%s\n' % fpne)
    printm('  Проверка файла на пригодность\n')

    if not exists(fpne):
        printm('  Ошибка! Файл не cуществует\n')
        return

    if ext not in exts:   # Проверка типа файла по расшир
        printm('  Ошибка! Расширение у файла д.б. %s\n' %
                                                ' или '.join(exts))
        return

    FIn = open(fpne, 'rb')   # Возможно обрамить Тру Кечем
    test_accel_ascii = 'ACCEL_ASCII "'
    InL0 = FIn.read(len(test_accel_ascii)).decode(pcad_code)
    if InL0 == test_accel_ascii:
        # Ура! Это скорей всего файл в ASCII формате
        InL0 += FIn.read(512).decode(pcad_code)
        FIn.close()   # Оценка содержимого файла
        InL0 = InL0.split(pcad_linesep)
        if InL0[1]:  # Вторая строка д.б. пустая в обоих форматах
            printm("  Ошибка! Вторая строка файла не пустая.\n")
            return
        if not (InL0[0].startswith('ACCEL_ASCII "') and
                InL0[5].startswith('  (program "P-CAD 2006 %s" ' %
                                exts[ext]['pr_name'])):
            # Первая и шестая строки должны начинаться так для ASCII формата
            printm('  Ошибка! Нестандартный формат ASCII файла\n')
            return
        FIn = open(fpne, 'rb')   # Возможно обрамить Тру Кечем
        lines = FIn.read().replace(b'\x00', b'').decode(
                                                pcad_code).split(pcad_linesep)

    else:  # Это скорей всего файл в бинарном формате
        if ext in {'SCH', 'PCB'}:  # Возможно это схема или плата
            InL0 += FIn.read(128).decode(pcad_code)
            InL0 = InL0.split(pcad_linesep)
            if len(InL0) < 2:  # Вторая строка д.б. пустая в обоих форматах
                printm("  Ошибка! Начало файла не соотв PCAD-файлам.\n")
                return
            if InL0[1]:  # Вторая строка д.б. пустая в обоих форматах
                printm("  Ошибка! Вторая строка PCAD-файла не пустая.\n")
                return
            if not InL0[3].startswith('P-CAD 2006 %s Binary (Rev ' %
                                    exts[ext]['pr_name']):
                # Четвёртая строка должна начинаться так для бинарного формата
                printm('  Ошибка! Формат файла не соответствует PCAD\n')
                return

        printm('  Необходимо преобразование файла в "ACCEL ASCII" формат.\n')
         # Поиск программы для преобразования файла
        #pcad_exe = exts[ext]['pr_fpne']
        pcad_exe = join(pcad_path, exts[ext]['pr_fn'] + '.EXE')
        if not exists(pcad_exe):   # В имени не нужны кавычки
            printm('  Ошибка! Не найдена необходимая '
                            'для этого программа : \n%s\n' % pcad_exe)
            printm('    %s-файл невозможно преобразовать '
                            'в "ACCEL ASCII" формат.\n' % ext)
            printm('    Пересохраните %s-файл '
                            'в "ACCEL ASCII" формате.\n' % ext)
            return

        pcad_in = r'_b_i_n_.' + ext  # Не любить ПКАД рус букв в командной строке
        copy2(fpne, pcad_in)
        #printm('  Исходный файл скопирован во временный файл.\n')
        printm('    Что-бы не терять времени, впредь используйте '
                            'файлы в "ACCEL ASCII" формате.\n')
        printm('    Подождите пару минут, производится преобразование . . .\n')
        pcad_out = r'_a_s_c_i_i_.' + ext
        bat_t = r'"%s" /A %s %s' % (pcad_exe, pcad_in, pcad_out)

        import subprocess
        import shlex
        args = shlex.split(bat_t)
        p = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        kv = p.communicate()[0]

        remove(pcad_in)

        if kv or not exists(pcad_out):
            printm('  Ошибка! Неудалось преобразовать '
                            'файл в "ACCEL ASCII" формат.\n')
            printm('    Возможно PCAD не 2006 '
                            'или не установлены "Сервис-паки".\n')
            printm('    Пересохраните %s-файл '
                            'в "ACCEL ASCII" формате.\n' % ext)
            return

        FIn = open(pcad_out, 'rb')  # Возможно обрамить Тру Кечем
        lines = FIn.read().replace(b'\x00', b'').decode(
                                                pcad_code).split(pcad_linesep)
        FIn.close()
        #remove(pcad_out)

        pcad_out2 = '_ASCII'.join(splitext(fpne))
        pcad_out3 = '_ASCII'.join(splitext(fpne))+ '.BAK'
        if exists(pcad_out2):
            remove(pcad_out2)
        if exists(pcad_out3):
            remove(pcad_out3)
        rename(pcad_out, pcad_out2)
        printm('  Файл преобразован в "ACCEL ASCII" формат и сохранён с именем:\n' +
            '%s\n' % pcad_out2)

    del(InL0)
    FIn.close()

    if not lines:
        printm('  Ошибка! Файл неудалось считать.\n')
        return

    printm('  Файл из %s строк считан.\n' % len(lines))

    ww[i]['lines'] = lines
    ExtractInf(i)
#..............................................................................


#------------------------------------------------------------------------------
def ExtractInf(i, kits=None):
    """ Производит начальное извлечение интересующей
        информации во вложенные словари """
    components = {}
    nets = {}
    rez = {}
    rez['net'] = {}

    lines = ww[i].get('lines', [])
    if not lines:
        return

    kits = {
    ''                     '(library "':
        {
            ''             '  (patternDefExtended "':
                (
                    ''     '    (patternGraphicsNameRef "',
                    ''     '      (patternGraphicsNameDef "',  # множество
                ),
            ''             '  (compDef "':
                (
                    ''     '      (sourceLibrary "',
                    ''     '      (compType ',
                    ''     '      (numPins ',
                    ''     '      (numParts ',
                    ''     '    (compPin "',  # множество (для симв пит)
                    ''     '    (attachedSymbol (',   # список
                    ''     '    (attachedPattern (',
                    ''     '      (numPads ',
                ),
        },
    ''                     '(netlist "':
        {
            ''             '  (compInst "':
                (
                    ''     '    (originalName "',
                    ''     '    (compValue "',
                    ''     '    (compRef "',
                ),
            ''             '  (net "':
                (
                    ''     '    (node "',
                ),
        },
    ''                     '(pcbDesign "':
        {
            ''             '  (multiLayer ':
                (
                    ''     '    (pattern (patternRef "',
                ),
        },
}

    level = 0

    for sIn in lines:

        if level == 0:  # Нет интересующей части
            for key in kits:  # Перебор интересующих частей
                if sIn.startswith(key):  # Проверка соответствия
                    level = 1
                    key_0 = key
                    kit_0 = kits[key].keys()  # Текущий набор 0 уровня
                    #sIn0 = sIn
                    break
            continue

        if sIn == ')':  # Проверка окончания части
            level = 0
            continue

        if level == 1:  # Нет интересующей секции
            for key in kit_0:  # Перебор интересующих секций
                if sIn.startswith(key):  # Проверка соответствия
                    level = 2
                    kit_1 = kits[key_0][key]  # Текущий набор 0 уровня
                    #sIn1 = sIn
                    x = sIn.split(None, 1)
                    section = x[0][1:]  # Текущая секция
                    if len(x) == 1:  # У '  (multiLayer ' нет имени (елемента)
                        elem = None  # Передавать параметром хоть что-то
                    else:
                        elem = x[1].split('"', 2)[1]  # Текущее имя елемента
                        #elem = '"'.join(x[1].split('"', 4)[1:4:2])
                    break
            continue

        if sIn == '  )':  # Проверка окончания секции
            level = 1
            continue

        for key in kit_1:  # Перебор интересующих параметров
            if sIn.startswith(key):  # Проверка соответствия
                #sIn2 = sIn
                x = sIn.split(None, 1)
                param = x[0][1:]  # Текущий параметр (его тип) без откр скобки

                numb_quot = x[1].count('"')

                if numb_quot >= 4:
                    val = tuple(x[1].split('"', 4)[1::2])
                elif numb_quot == 2:
                    val = x[1].split('"', 2)[1]
                elif not numb_quot:
                    val = x[1][:-1]  # Без заверш закрыв скобки
                else:
                    1/0

                #fun(section, elem, param, val)
                if section not in rez:
                    rez[section] = {elem: {param: [val]}}
                    break   # Создали новую секцию с
                            # елементом и парой параметр-значение
                if elem not in rez[section]:
                    rez[section][elem] = {param: [val]}
                    break  # Создали новый елемент с парой параметр-значение
                if param not in rez[section][elem]:
                    rez[section][elem][param] = [val]
                    break  # Создали новый параметр с значением
                # Добавление значениe к списку
                rez[section][elem][param].append(val)

                break

    if not rez:
        printm('  НЕУДАЛОСЬ извлечь обходимые для идентификации данные.\n')
        return

    printm('  Необходимые для идентификации данные извлечены.\n')

    pattern = {}
    if 'patternDefExtended' in rez and 'multiLayer' in rez:
        pattern = {refDesRef: patternRef for patternRef, refDesRef
                            in rez['multiLayer'][None]['pattern']}

    pows = set()  # Компоненты-символы питания
    # Формируем список экземпляров класса TComponent
    for elem in rez['compInst']:
        component = radio_component.TComponent(elem)

        # Добавляем поля в экземпляр класса
        for param, val in rez['compInst'][elem].items():
            setattr(component, param, val[0])  # Открытие одноэлем списка
        for param, val  in rez['compDef'][component.compRef].items():
            if param == 'compPin':
                compPins = val  # Только для символов питания
            elif param == 'attachedSymbol':
                setattr(component, param, val)  # Список оставляем
            else:
                setattr(component, param, val[0])  # Открытие одноэлем списка

        if (    'compType' in component.__dict__ and
                component.compType == 'Power' and
                'numPads' not in component.__dict__ and
                'attachedPattern' not in component.__dict__):
            # Этот компонент-символ питания
            # Варианты подключения компонента к цепям (ЕЛЕМ-ВЫВОД)
            # pin может быть не кортежем, а строкой, если пины без имени
            pows |= {(elem, pin if isinstance(pin, str) else pin[0])
                                    for pin in compPins}  # StringTypes
            continue

        del component.compRef  # был необх только для выбора compDef

        # Разбиение и приведение номинала к стандартному виду
        # Может быть только перед сравнением
        component.mix_value()

        if pattern:
            x = rez['patternDefExtended'][pattern[elem]]
            setattr(component,  # Открытие одноэлем списка
                'patternGraphicsNameRef', x['patternGraphicsNameRef'][0])
            setattr(component,  # Список оставляем множеством
                'patternGraphicsNameDef', set(x['patternGraphicsNameDef']))

        components[elem] = component

    ww[i]['components'] = components

    nets = {elem: set(rez['net'][elem]['node']) - pows
                                    for elem in rez['net'].keys()}
    ww[i]['nets'] = nets

    printm('  Идентифицировано компонентов - %s, цепей - %s\n' %
              (len(components), len(nets)))
#..............................................................................


#------------------------------------------------------------------------------
def otobp_dict(rez):
    """  Печать словарей  """

    for section in ('compInst', 'net'):
        printm('%s\n' % section)
        for elem in sorted(rez[section]):
            if section == 'net':
                printm('    %s =' % elem)
                for param in sorted(rez[section][elem]):
                    printm(' %s' % param)
                printm('\n')
            else:
                printm('    %s\n' % elem)
                for param in sorted(rez[section][elem]):
                    printm('        %s = %s\n' %
                                (param, rez[section][elem][param]))
#..............................................................................


#------------------------------------------------------------------------------
def set_to_str(st, sep=',', diapp='…'):
    """ Преобразует множество в компактную строку """

    ss = {}
    for rd in st:
        # Фильтрация RefDes-а
        r, k = '', ''
        for ch in reversed(rd):
            if r:
                r = ch + r
            elif '0' <= ch <= '9':
                k = ch + k
            else:
                r = ch + r
        if r not in ss:
            ss[r] = [k]  # {k} #
        else:
            ss[r].append(k)  # .add(k) #

    s = ''
    for r in sorted(ss):
        ns = ss[r]
        if len(ns) == 1:
            s += sep + r + ns[0]
            continue

        ns.sort(key=int)

        s += sep + r + ns[0]
        n = 1
        j = int(ns[0]) + 1

        for i in range(1, len(ns)):
            k = int(ns[i])

            if j == k:
                n += 1
                j += 1  # j = k + 1
                continue

            if n == 1:
                s += sep + r + ns[i]
            elif n == 2:
                s += sep + r + ns[i - 1] + sep + r + ns[i]
            else:
                s += diapp + r + ns[i - 1] + sep + r + ns[i]

            n = 1
            j = k + 1

        else:
            if n == 1:
                pass
            elif n == 2:
                s += sep + r + ns[i]
            else:
                s += diapp + r + ns[i]

    return s[len(sep):]
#..............................................................................


#------------------------------------------------------------------------------
def split_ref_des(ref_des):
    """ Обработывает текст """
    # Фильтрация RefDes-а
    r, n = '', ''
    for ch in reversed(ref_des):
        if r:
            r = ch + r
        elif ch.isdigit():
            n = ch + n
        else:
            r = ch + r
    if not n:
        n = '0'
    return r, int(n)
#..............................................................................


#------------------------------------------------------------------------------
def str_to_val(s, ei):
    """ Преобразует сокращённое обозначение величины в значение """

    frag_types = ''  # Типы фрагментов
    frags = []

    # Разбор входной строки на фрагменты типов d,p,e
    ch0_type = ''
    frag = ''
    for ch in s:  # .lower()
        # Определяем тип символа
        if ch.isdigit():
            ch_type = 'd'  # цифра
        elif ch in ',.':
            ch_type = 'p'  # точка
        else:
            ch_type = 'e'  # другое

        # Новый ли тип символа тип символа
        if not frag:
            ch0_type = ch_type
        elif ch0_type != ch_type:
            frags.append(frag)
            frag = ''
            frag_types += ch0_type
            ch0_type = ch_type
        frag += ch
    else:
        frags.append(frag)
        frag_types += ch0_type

    # Сокращённое символьное обозначение ЕИ
    i = frag_types.find('e')
    if i >= 0:
        pref_meas = frags[i]
    elif 'p' in frag_types:
        pref_meas = '.'
    else:
        pref_meas = ''
    # Поиск индекса символьного обозначения ЕИ
    for ind, variants in enumerate(EI_CONST[ei]['units_in']):
        if pref_meas in variants:
            break
    else:
        return -1  # Несоответвтующее правилам число

    # Выделение значения
    if     (frag_types == 'ded' and len(frags[1]) == 1 or
            frag_types == 'dpde' or
            frag_types == 'dpd'):
        number = frags[0] + '.' + frags[2]
    elif   (frag_types == 'ed' and len(frags[0]) == 1 or
            frag_types == 'pde' or
            frag_types == 'pd'):
        number = '.' + frags[1]
    elif   (frag_types == 'd' or
            frag_types == 'de' or
            frag_types == 'dp' or
            frag_types == 'dpe'):
        number = frags[0]
    else:
        return -1  # Несоответвтующее правилам число

    return float(number) * EI_CONST[ei]['mults_in'][ind]
#..............................................................................


#------------------------------------------------------------------------------
def val_to_str(f, ei):
    """ Преобразует значение в кратчайшую строку с ЕИ """
    for i, r in enumerate(EI_CONST[ei]['range_out']):
        if f >= r:
            sv = '%s' % (f / EI_CONST[ei]['mults_out'][i])
            if sv.endswith('.0'):
                sv = sv[:-2]
            return sv + EI_CONST[ei]['units_out'][i]
#..............................................................................


#------------------------------------------------------------------------------
def norm_value(rd, Value):
    """ Обработывает текст поля "Value" и возвращает словарь из составляющих
            значения (в зависимости от возможности их разпознать).
        Текст поля "Value" может состоять из основной и
            дополнительных величин разделённых разделителем.
        Для резисторов это м.б. сопротивление и точность (%).
        Для конденсаторов это м.б. ёмкость и напряжение
            (дополнительные величины добавляются к типу компонента).
    Для компонентов, отличных от avt_rdes анализ и разбиение не производится.

    Выходной словарь обязательно содержит:
Mix['Value'] # = строка Value исходное значение
Mix['mark']  # = строка '*' или ''
Mix['norm]   # = строка mark + valstr2 или др. нормализованное представл
   # (маленькие буквы, только точки) для сравнения
    Выходной словарь может содержать:
Mix['nom_f'] # 'R', 'C', 'L' номинал в Float виде
Mix['nom_s'] # 'R', 'C', 'L' строка номинал в симв виде с ЕИ
Mix['dev']   # 'p' строка точность в симв виде с ЕИ
Mix['lims']  # 'v', 'w', 'i' пары доп знач в симв виде с ЕИ
Mix['errs']  # = [,,,] пары нерасп частей значения
    """

    Mix = {}
    Mix['Value'] = Value

    valstr2 = Value.strip().lower().replace(',', '.')
    mark = '*'  # Можно любой значёк подставить, при необходимости
    if mark in valstr2:
        valstr2 = valstr2.replace(mark, '')
    else:
        mark = ''
    Mix['mark'] = mark

    if not valstr2 or 'value' in valstr2 or 'none' in valstr2:
        # Нет значения
        Mix['norm'] = mark
        return Mix  # -->

    # Фильтрация значений
    rdp = split_ref_des(rd)[0]
    if rdp not in avt_rdes:
        # Это значение не разбивается
        Mix['norm'] = mark + valstr2
        return Mix  # -->

    ss = re.split('[ /xх-]', valstr2)
    for i in range(len(ss) - 1, -1, -1):
        if not ss[i]:
            del(ss[i])
    if not ss:
        # После разбиения не осталось значимыъх частей
        Mix['norm'] = mark + valstr2
        return Mix  # -->

    norm_str = ''
    for i, s in enumerate(ss):
        for j, ei in enumerate((rdp,) + dop_ei):
            v = str_to_val(s, ei)
            if v >= 0:
                s = val_to_str(v, ei)
                if ei == rdp:
                # if j == 0:
                    #Mix['noms'] = v, s
                    Mix['nom_f'] = v
                    Mix['nom_s'] = s
                elif ei == 'p':
                # elif j == 1:
                    Mix['dev'] = s
                elif 'lims' not in Mix:
                    Mix['lims'] = [(ei, s)]
                else:
                    Mix['lims'].append((ei, s))
                break
        else:
            if 'errs' not in Mix:
                Mix['errs'] = [(i, s)]
            else:
                Mix['errs'].append((i, s))

        if not norm_str:
            norm_str = s
        else:
            norm_str += ' ' + s

    Mix['norm'] = mark + norm_str

    return Mix  # -->
#..............................................................................




#------------------------------------------------------------------------------
def main(args):
    """ Получает список файлов, переданных в параметрах командной
    строки. Значение "_n_args" должно соответствовать требуемому
    количеству передаваемых файлов. """
    global sch_index, pcb_index

    for i, fpne in enumerate(args):
        ReadFile(fpne, i)  # pcad_common.
##        ExtractInf(i)


#------------------------------------------------------------------------------
if __name__ == '__main__':

    from common import main0
    _n_args = [2]
    main0(main, _n_args)  # Нет необходимости трогать

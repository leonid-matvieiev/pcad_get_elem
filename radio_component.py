#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Модуль radio_component.py  модуль
    может найти информацию о radio_component.py """

#                Автор: Л.М.Матвеев

r""" Модуль ....py  модуль
Символы подстановки (метасимволы):

sudo позволяет использовать знаки подстановки, подобные знакам подстановки
оболочки, для использования в именах пути также, как в параметрах командной
строки в файле sudoers. Знаки подстановки соответствуют -1POSIX fnmatch(3).
Обратите внимание, что это не регулярные выражения.

"*"
    Соответствует любому количеству символов, в том числе нулю.
"?"
    Соответствует любому одному символу.
"[...]"
    Соответствует любому символу в заданном диапазоне.
"[!...]"
    Соответствует любому символу не в указанном диапазоне.
"\x"
    Для любого символа x, принять значение x. Это необходимо для использования
    специальных символов: *, ?, [, и }.

Обратите внимание, что знак слэша ('/') не будет соответствовать символам
подстановки используемым в имени пути. Однако, если сравнивать с параметрами
командной строки, слэш будет соответствовать символу подстановки. Это делает
путь подобный:


    /usr/bin/*

соответствующим /usr/bin/who, но не /usr/bin/X11/xterm.
Исключения из правил символов подстановки:

К вышеприведенным правилам применимы следующие исключения:

"" ""
    Если единственным параметром командной строки, в записи sudoers, является
    пустая строка "", это означает, что команда не может быть выполнена ни с
    какими параметрами.


Другие специальные символы и зарезервированные слова:

Знак фунта ('#') используется для обозначения комментария (если это происходит
не в контексте имени пользователя, сопровождается одной или более цифр и
обрабатывается как универсальный идентификатор пользователя (uid)). И знак
комментария, и любой текст после него, игнорируются до конца строки.

Зарезервированное слово -1ALL является встроенным псевдонимом, которое всегда
имеет определение. Это может использоваться везде, где было бы уместно
использование псевдонимов Cmnd_Alias, User_Alias, Runas_Alias, или Host_Alias.
Вы не должны пытаться назначить свой собственный псевдоним с именем -1ALL,
поскольку встроенный псевдоним будет использоваться вместо вашего собственного.
Помните, что использование -1ALL в контексте команды опасно, так как позволит
пользователю выполнить любую команду в системе.

Знак восклицания (!') может быть использован как логический оператор не, как в
псевдониме, так и перед Cmnd. Это позволяет исключать некоторые значения.
Обратите внимание, что использование ! в сочетании с встроенным псевдонимом ALL
для разрешения выполнения пользователем всего кроме нескольких команд не всегда
работает должным образом (см. -1БЕЗОПАСНОСТЬ -1ПРИМЕЧАНИЯ ниже).

Длинные строки могут быть перенесены при помощи обратного слэша (\'), если он
является последним символом в строке.

Пробелы между элементами описания, также как и специальные синтаксические
символы в Спецификации пользователя ('=, :, (, )'), являются необязательными.

Следующие символы должны начинаться с символа обратного слэша (\'), когда
используются как часть слова (т.е. имя пользователя или имя компьютера):
    '@, !, =, :, ,, (, ), \.
    может найти информацию о .
"""
############################################################################

_TITLES_BY_REFDES = {
    'A': 'Устройства',    # А
    'B': 'Преобразователи, датчики',    # В
    'BA': 'Громкоговорители',    # ВА
    'BB': 'Магнитострикционные элементы',    # ВВ
    'BC': 'Сельсин-датчики',    # ВС
    'BD': 'Детекторы ионизирующих излучений',
    'BE': 'Сельсин-приемники',
    'BF': 'Телефоны (капсюли)',    # В
    'BK': 'Тепловые датчики',    # ВК
    'BL': 'Фотоэлементы',
    'BM': 'Микрофоны',    # ВМ
    'BP': 'Датчики давления',    # ВР
    'BQ': 'Пьезоэлементы',
    'BR': 'Тахогенераторы',
    'BS': 'Звукосниматели',
    'BV': 'Датчики скорости',
    'C': 'Конденсаторы',
    'D': 'Схемы интегральные, микросборки',
    'DA': 'Схемы интегральные аналоговые',
    'DD': 'Схемы интегральные цифровые',
    'DS': 'Устройства памяти',
    'DT': 'Устройства задержки',
    'E': 'Элементы разные',    # Е
    'EK': 'Нагревательные элементы',    # ЕК
    'EL': 'Лампы осветительные',
    'ET': 'Пиропатроны',    # ЕТ
    'F': 'Предохранители, устройства защитные',
    'FA': 'Элементы защиты по току мгновенные',
    'FP': 'элементы защиты по току инерционные',
    'FU': 'Предохранители плавкие',
    'FV': 'Элементы защиты по напряжению',
    'G': 'Генераторы, источники питания',
    'GB': 'Батареи',
    'H': 'Устройства индикаторные и сигнальные',
    'HA': 'Приборы звуковой сигнализации',    # НА
    'HG': 'Индикаторы символьные',
    'HL': 'Приборы световой сигнализации',
    'J': 'Джамперы',
    'K': 'Реле, контакторы, пускатели',    # К
    'KA': 'Реле токовые',    # КА
    'KH': 'Реле указательные',    # КН
    'KK': 'Реле электротепловые',    # КК
    'KM': 'Контакторы, магнитные пускатели',    # КМ
    'KT': 'Реле времени',    # КТ
    'KV': 'Реле напряжения',
    'L': 'Индуктивности',
    'LL': 'Дроссели люминесцентного освещения',
    'M': 'Двигатели',    # М
    'P': 'Приборы измерительные',    # Р
    'PA': 'Амперметры',    # РА
    'PC': 'Счетчики импульсов',
    'PF': 'Частотомеры',
    'PI': 'Счетчики активной энергии',
    'PK': 'Счетчик реактивной энергии',    # РК
    'PR': 'Омметры',
    'PS': 'Регистрирующие приборы',
    'PT': 'Часы',    # РТ
    'PV': 'Вольтметры',
    'PW': 'Ваттметры',
    'QF': 'Выключатели автоматические',
    'QK': 'Короткозамыкатели',
    'QS': 'Разъединители',
    'R': 'Резисторы',
    'RK': 'Терморезисторы',
    'RP': 'Потенциометры',
    'RS': 'Шунты измерительные',
    'RU': 'Варисторы',
    'S': 'Устройства коммутационные маломощные',
    'SA': 'Выключатели или переключатели',
    'SB': 'Выключатели кнопочные',
    'SF': 'Выключател автоматические',
    'SK': 'Выключатели от температуры',
    'SL': 'Выключатели от уровня',
    'SP': 'Выключатели от давления',
    'SQ': 'Выключатели от положения',
    'SR': 'Выключатели от частоты вращения',
    'T': 'Трансформаторы, автотрансформаторы',    # Т
    'TA': 'Трансформаторы тока',    # ТА
    'TS': 'Электромагнитные стабилизаторы',
    'TV': 'Трансформаторы напряжения',
    'U': 'Устройства связи, преобразователи',
    'UB': 'Модуляторы',
    'UI': 'Дискриминаторы',
    'UR': 'Демодуляторы',
    'UZ': 'Преобразователи частотные, выпрямители',
    'V': 'Приборы электровакуумные и полупроводниковые',
    'VD': 'Диоды, стабилитроны',
    'VL': 'Приборы электровакуумные',
    'VS': 'Тиристоры',
    'VT': 'Транзисторы',
    'W': 'Элементы СВЧ, антенны',
    'WA': 'Антеннаы',
    'WE': 'Ответвители',
    'WK': 'Короткозамыкатели',
    'WS': 'Вентили',
    'WT': 'СВЧ трансформаторы, неоднородности, фазовращатели',
    'WU': 'Аттенюаторы',
    'X': 'Соединения контактные',
    'XA': 'Токосъемники',
    'XP': 'Штыри',
    'XS': 'Гнёзда',
    'XT': 'Соединения разборные',
    'XW': 'Соединители высокочастотные',
    'Y': 'Устройства механические с электромагнитным приводом',
    'YA': 'Электромагниты',
    'YB': 'Тормоза с электромагнитным приводом',
    'YC': 'Муфты с электромагнитным приводом',
    'YH': 'Электромагнитные патроны, плиты',
    'Z': 'Фильтры, ограничители',
    'ZL': 'Ограничители',
    'ZQ': 'Фильтры кварцевые',
            # Исходя из сложившейся практики
    'Q': 'Резонаторы кварцевые',
    'BU': 'Приборы звуковой сигнализации',
    }

'''
chr_error_ru_en = {'К': 'K', 'Е': 'E', 'Н': 'H', 'Х': 'X', 'В': 'B',
    'А': 'A', 'Р': 'P', 'О': 'O', 'С': 'C', 'М': 'M', 'Т': 'T', }
_TITLES_BY_REFDES2 = []
for a in _TITLES_BY_REFDES:
    a2 = ''
    p = ''
    for c in a:
        if c in chr_error_ru_en:
            a2 += chr_error_ru_en[c]
            p += c
        else:
            a2 += c
    if p:
        p = '    # ' + p
    _TITLES_BY_REFDES2.append((a2, _TITLES_BY_REFDES[a], p))
for a2, v, p in sorted(_TITLES_BY_REFDES2):
    print "    '%s': '%s',%s" % (a2, v, p)
'''

##_SMD_SUFFIXES = {
##    'L': ', SMD',
##    'C': ', керамический SMD',
##    'R': ', SMD',
##    }

_SMD_SUFFIXES = {
    'L': '',
    'C': 'X7R',
    'R': '',
    }

_SMD_TYPE_SIZES = {  # Типоразмеры
    '0201': '0201',
    '0402': '0402',
    '0603': '0603',
    '0804': '0805',
    '0805': '0805',
    '1206': '1206',
    '1210': '1210',
    '1812': '1812',
    '2010': '2010',
    '2220': '2220',
    '2512': '2512',
    }

_DEVIATIONS = {  # Точности по умолчанию
    'L': ('#20%', '#20%'),  # nosmd, smd
    'C': ('#20%', '#10%'),  # nosmd, smd
    'R': ('#5%', '#5%'),    # nosmd, smd
    }

_LIMITS = {  # Максимально-допустимые значения
    '': {  # Не SMD
        'L': '#1A',
        'C': '#100В',
        'R': '#0.5Вт'},
    '0201': {
        'L': '#1A',
        'C': '12В',
        'R': '0.05Вт'},
    '0402': {
        'L': '#1A',
        'C': '50В',
        'R': '0.063Вт'},
    '0603': {
        'L': '#1A',
        'C': '50В',
        'R': '0.1Вт'},
    '0805': {
        'L': '#1A',
        'C': '150В',
        'R': '0.125Вт'},
    '1206': {
        'L': '#1 A',
        'C': '200 В',
        'R': '0.25 Вт'},
    '1210': {
        'L': '#1A',
        'C': '200В',
        'R': '0.5Вт'},
    '1812': {
        'L': '#1A',
        'C': '200В',
        'R': '0.5Вт'},
    '2010': {
        'L': '#1A',
        'C': '200В',
        'R': '0.75Вт'},
    '2220': {
        'L': '#1A',
        'C': '200В',
        'R': '0.75Вт'},
    '2512': {
        'L': '#1A',
        'C': '200В',
        'R': '1Вт'},
    }

_FILDS_BY_TYPE = {
'PUMH11':{
    'pe_postname': ', два цифровых n-p-n',
    },
'BC857[C]':{
    'pe_postname':', биполярный p-n-p',
    'peNote': 'Корпус SOT-23',
    },
'IRLML6402':{
    'pe_postname':', полевой Р-канальный',
    'peNote': 'Корпус SOT-23',
    },
'BCP53':{
    'peTitle':'Транзисторы',
    'pe_postname':', биполярный  p-n-p',
    'peNote': 'Корпус SOT-223',
    },
'IRLM6802':{
    'pe_postname':', полевой Р-канальный',
    'peNote': 'Корпус SOT-23-6',
    },
'BAT54C':{
    'pe_postname':', переключающий 70В 200мА',
    'peNote': 'Корпус SOT-23',
    },
'15MQ040N':{
    'pe_postname':', Шоттки 40V 3A',
    'peNote': 'Корпус SMA',
    },
'ESDA6V1W5':{
    'peTitle': 'Диоды, стабилитроны',
    'pe_postname': ', Защитная ИС',
    'peNote': 'Корпус SOT-353-5L',
    },
}


import pcad_common
from fnmatch import fnmatch

##SPLIT_ORIGNAME = False
##SPLIT_PATTERN = False
SPLIT_ORIGNAME = True
SPLIT_PATTERN = True


def tuple_to_color_str(t, d=False):
    """
    Возвращает: фрагмент HTML кода с раскраской, если необходимо
    Вход:
        кортеж: первое значение - текст, второе - цвет
        кортеж: первое значение - текст, второе - лог-я достоверность
        две строки: первое значение - текст, второе - цвет
        строка и лог-я достоверность: первое значение - текст, второе - ...
        строка: текст, лог-я достоверность по умолч "False"
    """
    if isinstance(t, tuple):
        t_, d_ = t
    else:
        t_, d_ = t, d
    if not t_:
        return ''
    if isinstance(d_, str):
        return '<span style="background:%s">%s</span>' % (d_, t_)
    if isinstance(d_, bool):
        if d_ or t_ == '':
            return t_
        # Цвет окраски по умолчанию "yellow" задаётся здесь
        return '<span style="background:yellow">%s</span>' % t_
    return ''


def tuple_tuple_to_color_str(ts, ds=None):
    """
    Возвращает: фрагмент HTML кода с раскраской, если необходимо
    Вход:
        два кортежи: - тексты, - цвета
        кортеж кортежей: - (текст, цвет)
    """
    if ds is not None:
        # Парная упаковка двух последовательностей
        tt = zip(ts, ds)
    elif isinstance(ts, tuple):
        # Последовательность пар
        tt = ts
    elif isinstance(ts, list):
        # Пара последовательностей
        tt = zip(ts[0], ts[1])
    else:
        # Непонятно что, пусть будет тоже пара последовательностей
        tt = zip(ts[0], ts[1])

    tmp = ''
    for td in tt:
        if tmp and (td[0][:1] not in '.,'):
            tmp += '&nbsp;'
        tmp += tuple_to_color_str(td)
    return tmp


class TComponent:
    """  """

    def __init__(_, RefDes):
        _.RefDes = RefDes

    def mix_value(_):
        # лучше разпотрошить по отдельным полям
        _.Mix = pcad_common.norm_value(_.RefDes, getattr(_, 'compValue', ''))


    def form_html_str_in(_):
        """ представление исходных данных (строка HTML таблицы) """

        # Всё в одной ячейке
##        _.htmOrig = ''
        _.htmOrig = '(%s)' % _.attachedSymbol[0]  # Первый символ списка

        if _.Mix['Value'] != _.originalName:
            _.htmOrig += ' %s' % _.Mix['Value']

        _.htmOrig += ' тип %s' % _.originalName

        if 'numPads' in _.__dict__:
            _.htmOrig += ' в %s-выв' % _.numPads
        else:
            _.htmOrig += tuple_to_color_str(' выв?')

        if 'attachedPattern' in _.__dict__:
            _.htmOrig += ' %s' % _.attachedPattern
        else:
            _.htmOrig += tuple_to_color_str(' корпус?')

        if (    'patternGraphicsNameDef' in _.__dict__ and
                len(_.patternGraphicsNameDef) > 1 and
                'patternGraphicsNameRef' in _.__dict__):
            _.htmOrig += ' &lt;%s&gt;' % _.patternGraphicsNameRef

##        _.htmOrig += ' (%s)' % _.attachedSymbol[0]  # Первый символ списка


    def set_properties(_):

        _.RefDesPrefix, _.RefDesNumber = pcad_common.split_ref_des(_.RefDes)

        # Промежуточные (после сравнения) Значения
        _.pe_mark = (_.Mix['mark'], False)

        _.nom_f = _.Mix.get('nom_f', -1)
        if 'nom_s' in _.Mix:
            _.pe_nom_s = (_.Mix['nom_s'], True)
        else:
            _.pe_nom_s = (_.Mix['norm'], False)

        if 'dev' in _.Mix:
            _.pe_dev = (_.Mix['dev'], True)

        if 'lims' in _.Mix:
            _.pe_lim = (' '.join([x for k, x in _.Mix['lims']]), True)

        if 'errs' in _.Mix:  # Пристроить
            _.pe_errs = (' '.join([x for k, x in _.Mix['errs']]), False)

        if _.RefDesPrefix in _TITLES_BY_REFDES:
            _.peTitle = ((_TITLES_BY_REFDES[_.RefDesPrefix], True), )
        # Если у имени после префикса "pe" или "sp" продолжение
        #   начинается с заглавной буквы, то это кортеж кортежей
        # Если у имени после префикса "pe" или "sp" продолжение
        #   начинается с подчёркивания и строчной буквы, то это кортеж

        for template in _FILDS_BY_TYPE:
            if fnmatch(_.originalName, template):
                ##for  in : setattr(, , )getattr(
                if 'peNote' in _FILDS_BY_TYPE[template]:
                    _.peNote = ((_FILDS_BY_TYPE[template]['peNote'], True), )

                if 'pe_postname' in _FILDS_BY_TYPE[template]:
                    _.pe_postname = (_FILDS_BY_TYPE[template]['pe_postname'], True)

                if 'peTitle' in _FILDS_BY_TYPE[template]:
                    _.peTitle = ((_FILDS_BY_TYPE[template]['peTitle'], True), )
                break

##        if 'attachedPattern' in _.__dict__:
##            for template in fields_by_pattern:
##                if fnmatch(_.attachedPattern, template):
##                    if 'peNote' in fields_by_pattern[template]:
##                        _.peNote = ((fields_by_pattern[template]['peNote'], True),)
##                    break


        # Запуск вспом функций
        _.form_html_str_in()
        _.form_html_filds_pe_sp()


    def form_html_filds_pe_sp(_):
        """
        Для Перечня необходимы:
            _.peTitle
            _.peName
            _.peNote
        Для Спецификации необходимы:
            _.spTitle
            _.spName
        """

        # Наименование раздела т.п.

        # Это попозже, если не будет в СМД ???????????????????????????
        if 'peTitle' not in _.__dict__:
            _.peTitle = (('Нет в ГОСТ', False), )
        _.spTitle =_.peTitle

        if SPLIT_ORIGNAME:
            orig_name = _.originalName.split('_', 1)[0]
        else:
            orig_name = _.originalName

        if 'attachedPattern' in _.__dict__:
            if SPLIT_PATTERN:
                att_pattern = _.attachedPattern.split('_', 1)[0]
            else:
                att_pattern = _.attachedPattern


        if _.RefDesPrefix not in {'R', 'C', 'L'}:
            # Компонент не RCL (самых многочисленных) типов
            pass
            # Значение поля "Названия" для ПЭ
            if _.Mix['Value']:
                _.pe_name = (_.Mix['Value'], True)
            else:
                _.pe_name = (orig_name, False)

            if 'pe_postname' in _.__dict__:
                _.peName = (_.pe_name, _.pe_postname)
            else:
                _.peName = (_.pe_name, )

        else:  # Компонент RCL (топовый тип)
            _.smd_tr = ''  # Проверяем СМД-шность
            if 'attachedPattern' in _.__dict__:
                for tr in _SMD_TYPE_SIZES:
                    if tr in _.attachedPattern and _.numPads == '2':
                        _.smd_tr = _SMD_TYPE_SIZES[tr]
                        break

            if 'pe_dev' in _.__dict__:
                pass
            elif _.RefDesPrefix in _DEVIATIONS:
                dev = _DEVIATIONS[_.RefDesPrefix][bool(_.smd_tr)]
                if dev[:1] == '#':
                    _.pe_dev = (dev[1:], False)
                else:
                    _.pe_dev = (dev, True)
            else:
                _.pe_dev = ('', False)

            if 'pe_lim' not in _.__dict__:
                lim = _LIMITS[_.smd_tr][_.RefDesPrefix]

                if lim[:1] == '#':
                    _.pe_lim = (lim[1:], False)
                else:
                    _.pe_lim = (lim, True)

            if _.smd_tr:
                _.peName = (('SMD', True), (_.smd_tr, True), _.pe_nom_s, _.pe_lim,
                            (_SMD_SUFFIXES[_.RefDesPrefix], False), _.pe_dev)

                if 'peNote' not in _.__dict__:
                    _.peNote = (('', True), )

            else:
                _.peName = (_.pe_nom_s, _.pe_lim, _.pe_dev)


            _.spName = (_.pe_nom_s,)
            if _.RefDesPrefix in ('R',):  # Можно не только 'R'

                if _.smd_tr:
                    _.spTitle =_.spTitle + (('SMD', True), (_.smd_tr, True),)
                    if (    'pe_lim' in _.__dict__ and
                            'pe_dev' in _.__dict__):
                        _.spTitle =_.spTitle + ((',', True), _.pe_lim, _.pe_dev,)
                    elif 'pe_lim' in _.__dict__:
                        _.spTitle =_.spTitle + ((',', True), _.pe_lim,)
                    elif 'pe_dev' in _.__dict__:
                        _.spTitle =_.spTitle + ((',', True), _.pe_dev,)
                else:
                    if 'pe_lim' in _.__dict__:
                        _.spName =_.spName + (_.pe_lim,)
                    if 'pe_dev' in _.__dict__:
                        _.spName =_.spName + (_.pe_dev,)

                    if 'attachedPattern' in _.__dict__:
                        _.spName = _.spName + (('(%s)' % att_pattern, False),)
                    else:
                        _.spName = _.spName + (('(Корпус?)', False),)

            else:  #elif _.RefDesPrefix in ('L', 'C',): # Остальные
                    #
                if 'pe_lim' in _.__dict__:
                    _.spName =_.spName + (_.pe_lim,)
                if _.smd_tr:
                    _.spName =_.spName + ((_SMD_SUFFIXES[_.RefDesPrefix], False),)
                if 'pe_dev' in _.__dict__:
                    _.spName =_.spName + (_.pe_dev,)

                if _.smd_tr:
                    _.spTitle =_.spTitle + (('SMD', True), (_.smd_tr, True),)
                else:
                    if 'attachedPattern' in _.__dict__:
                        _.spName = _.spName + (('(%s)' % att_pattern, False),)
                    else:
                        _.spName = _.spName + (('(Корпус?)', False),)

        if 'peNote' not in _.__dict__:
            if 'attachedPattern' in _.__dict__:
                _.peNote = (('Корпус', True), (att_pattern, False))
            else:
                _.peNote = (('Корпус?', False), )

        if 'spName' not in _.__dict__:
            _.spName = (_.pe_name,)

            if 'attachedPattern' not in _.__dict__:
                _.spName = _.spName + (('(Корпус?)', False),)
            elif _.pe_name[0] != _.attachedPattern:
                _.spName = _.spName + (('(%s)' % att_pattern, False),)


        _.peTitleRepack = [list(t) for t in zip(*_.peTitle)]
        _.peNameRepack  = [list(t) for t in zip(*_.peName)]
        _.peNoteRepack  = [list(t) for t in zip(*_.peNote)]

        _.spTitleRepack = [list(t) for t in zip(*_.spTitle)]
        _.spNameRepack  = [list(t) for t in zip(*_.spName)]

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Программа-модуль get_elem_cp.py (командной строки) для получения
заготовок файлов "Перечня элементов" и "Спецификации" из PCB-файла.
"""

#                Автор: Л.М.Матвеев

import os
import common
import pcad_common
import pcad_compare_cp
from  common import printm
import radio_component as rc
from functools import reduce

from os import startfile

# Глобальные переменные
pe_suffix = '_ПЭ3'
sp_suffix = '_СП'
sch_index = -1
pcb_index = -1
table_bord = 1


#------------------------------------------------------------------------------
def add_over_sp():
    """  """

    components.sort(key=lambda x: (x.spTitleRepack[0], x.RefDesPrefix,
                        x.nom_f, x.spName, x.pe_mark,   x.htmOrig))

    # Перебор / группировка строк одинаковых компонентов
    for i, compon in enumerate(components + [components[0]]):

        if i:  # Если не первый

            if (compon_old.spTitleRepack[0] == compon.spTitleRepack[0] and
                compon_old.RefDesPrefix == compon.RefDesPrefix and
                compon_old.spNameRepack[0] == compon.spNameRepack[0] and
                compon_old.pe_mark == compon.pe_mark and
                ('pe_errs' not in compon_old.__dict__ and
                'pe_errs' not in compon.__dict__ or
                'pe_errs' in compon_old.__dict__ and
                'pe_errs' in compon.__dict__ and
                compon_old.pe_errs == compon.pe_errs)
                ):  # проверка одинаковости компонентов по содержимому

                # Если одинаковые
                set_RefDes.add(compon.RefDes)

                # Правильное объединение полей по цвету
                for j in range(len(spTitleColors)):
                    spTitleColors[j] = spTitleColors[j] and compon.spTitle[j][1]
                for j in range(len(spNameColors)):
                    spNameColors[j] = spNameColors[j] and compon.spName[j][1]
                continue

            # Получили компонет, с отличающимся содержаним:
            # Формируем групповую цветную строку HTML формата
            name_all = [[compon_old.pe_mark[0]] + compon_old.spNameRepack[0],
                        [compon_old.pe_mark[1]] + spNameColors]

            if 'pe_errs' in compon_old.__dict__:
                name_all[0].append(compon_old.pe_errs[0])
                name_all[1].append(compon_old.pe_errs[1])

##            # Перенос * к значению (если СМД)
##            if name_all[0][0] == '*' and name_all[0][1] == 'SMD':
##                name_all[0] = name_all[0][1:3] + name_all[0][:1] + name_all[0][3:]
##                name_all[1] = name_all[1][1:3] + name_all[1][:1] + name_all[1][3:]

            name_html = rc.tuple_tuple_to_color_str(name_all).replace(
                                '>*</span>&nbsp;', '>*</span>')

            spRowUnion = '<TD align="center">&nbsp;<TD>%s' % name_html
            spRowUnion += '<TD align="center">%s<TD>%s' % (len(set_RefDes),
                                pcad_common.set_to_str(set_RefDes))  # , sep=','

            components[i - 1].spRowUnion = spRowUnion

        # Запоминаем текущие значения необходимых полей
        spNameColors = compon.spNameRepack[1]
        spTitleColors = compon.spTitleRepack[1]
        set_RefDes = {compon.RefDes}
        compon_old = compon
#..............................................................................


#------------------------------------------------------------------------------
def build_sp(sp_fpne, flag_orig=False):
    """  """
    sp_head = (('Ф.', 35), ('З.', 25), ('П.', 25),
                    ('Обозначение', 150), ('Наименование_', 400),
                    ('Кол.', 35), ('Примечание', 150))
    sp_width = reduce(lambda a, b: a + b + table_bord,
                            list(zip(*sp_head))[1], table_bord)
    ss = '''
<!DOCTYPE html>
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=%s">
<TITLE>Спецификация (заготовка)</TITLE>
</HEAD>
<BODY>
  <TABLE cellspacing="0" border="%s"  width="%s">
    <TR>''' % (common.web_chr_set, table_bord, sp_width)
    for k, v in sp_head:  # не "map" Заголовок
        ss += '<TH width="%s">%s' % (v, k)

    spTitle_old = None
    set_RefDes = set()
    for i, compon in enumerate(components):  # Перебор строк

        if spTitle_old != compon.spTitleRepack:   # ? spTitle
            spTitle_old = compon.spTitleRepack    # ? spTitle
            ss += '\n<TR>' + 7 * '<TD>&nbsp;'
            ss += ('\n<TR>' + 4 * '<TD>&nbsp;' + '<TD align="center">'
                    '<Big><U>%s</U></Big>' + #&nbsp;
                    2 * '<TD>&nbsp;') % rc.tuple_tuple_to_color_str(spTitle_old)
            ss += '\n<TR>' + 7 * '<TD>&nbsp;'

        if flag_orig:
            if set_RefDes == set() or htmOrig_old == compon.htmOrig:
                set_RefDes.add(compon.RefDes)
            else:
                ss += ('\n<TR bgcolor=#E0FFFF><font color="red">' +
                            3 * '<TD>&nbsp;' +
                            '<TD colspan="4">' + htmOrig_old +
                            (' | %s | %s' % (len(set_RefDes),
                            pcad_common.set_to_str(set_RefDes))))  # , sep=','
                set_RefDes = {compon.RefDes}
            htmOrig_old = compon.htmOrig

            if 'spRowUnion' in compon.__dict__:
                ss += ('\n<TR bgcolor=#E0FFFF><font color="red">' +
                            3 * '<TD>&nbsp;' +
                            '<TD colspan="4">' + compon.htmOrig +
                            (' | %s | %s' % (len(set_RefDes),
                            pcad_common.set_to_str(set_RefDes))))  # , sep=','
                set_RefDes = set()

        if 'spRowUnion' in compon.__dict__:
            ss += '\n<TR>' + 3 * '<TD>&nbsp;' + compon.spRowUnion

    ss += '''  </TABLE>
</BODY>
</HTML>'''

    printm("\n%s\n" % sp_fpne)
    try:
        fp = open(sp_fpne, 'w', encoding=common.web_code)
    except IOError:
        printm('    Неудались запись и открытие Файла. '
                            'Возможно он занят другой программой.\n')
        return
    fp.write(ss)  # .encode(common.web_code)
    fp.close()
#    if  sys.platform in ('win32', 'win64'):
    if common.win:
#        if zap_pe == 1:
#        if not flag_orig:
            printm('      Возможно, открытия файлов придётся '
                            'минутку подождать.\n')
            startfile(sp_fpne)
#            prog = r'D:\Portables\UniversalViewerPro\Viewer.exe'
#            os.spawnl(os.P_NOWAIT, prog, prog, '"%s"' % sp_fpne)
#            os.system((r'start D:\Portables\UniversalViewerPro\Viewer.exe "%s"' % sp_fpne).encode('cp866'))
#            os.system(r'D:\Portables\UniversalViewerPro\Viewer.exe d:\1.txt')
#            import subprocess
#            subprocess.Popen((r'D:\Portables\UniversalViewerPro\Viewer.exe', r'd:\1.txt'))
#..............................................................................


#------------------------------------------------------------------------------
def add_over_pe():
    """  """

    components.sort(key=lambda x: (x.peTitleRepack[0], x.RefDesPrefix,
                                    x.RefDesNumber, x.pe_mark))  # x.peTitle

    # Перебор / группировка строк одинаковых компонентов
    for i, compon in enumerate(components + [components[0]]):

        if i:  # Если не первый

            if (compon_old.peTitleRepack[0] == compon.peTitleRepack[0] and
                compon_old.RefDesPrefix == compon.RefDesPrefix and
                compon_old.peNameRepack[0] == compon.peNameRepack[0] and
                compon_old.peNoteRepack[0] == compon.peNoteRepack[0] and
                compon_old.pe_mark == compon.pe_mark and
                ('pe_errs' not in compon_old.__dict__ and
                'pe_errs' not in compon.__dict__ or
                'pe_errs' in compon_old.__dict__ and
                'pe_errs' in compon.__dict__ and
                compon_old.pe_errs == compon.pe_errs)
                ):  # проверка одинаковости компонентов по содержимому

                # Если одинаковые
                set_RefDes.add(compon.RefDes)

                # Правильное объединение полей по цвету
                for j in range(len(peTitleColors)):
                    peTitleColors[j] = peTitleColors[j] and compon.peTitle[j][1]
                for j in range(len(peNameColors)):
                    peNameColors[j] = peNameColors[j] and compon.peName[j][1]
                for j in range(len(peNoteColors)):
                    peNoteColors[j] = peNoteColors[j] and compon.peNote[j][1]
                continue

            # Получили компонет, с отличающимся содержаним:
            # Формируем групповую цветную строку HTML формата
            name_all = [[compon_old.pe_mark[0]] +
                                compon_old.peNameRepack[0],
                        [compon_old.pe_mark[1]] +
                                peNameColors]
            if 'pe_errs' in compon_old.__dict__:
                name_all[0].append(compon_old.pe_errs[0])
                name_all[1].append(compon_old.pe_errs[1])

            # Перенос * к значению (если СМД)
            if name_all[0][0] == '*' and name_all[0][1] == 'SMD':
                name_all[0] = name_all[0][1:3] + name_all[0][:1] + name_all[0][3:]
                name_all[1] = name_all[1][1:3] + name_all[1][:1] + name_all[1][3:]

            name_html = rc.tuple_tuple_to_color_str(name_all).replace(
                                '>*</span>&nbsp;', '>*</span>')

            note_html = rc.tuple_tuple_to_color_str(
                        compon_old.peNoteRepack[0], peNoteColors)

            peRowUnion = '<TD align="center">%s<TD>%s' % (
                    pcad_common.set_to_str(set_RefDes), name_html, )  # , sep=','
            peRowUnion += '<TD align="center">%s<TD>%s' % (len(set_RefDes), note_html)

            components[i - 1].peRowUnion = peRowUnion

        # Запоминаем текущие значения необходимых полей
        peTitleColors = compon.peTitleRepack[1]
        peNameColors = compon.peNameRepack[1]
        peNoteColors = compon.peNoteRepack[1]
        set_RefDes = {compon.RefDes}
        compon_old = compon
#..............................................................................


#------------------------------------------------------------------------------
def build_pe(pe_fpne, flag_orig=False):
    """  """
    pe_head = (('Поз. обозн.', 150), ('Наименование', 330),
                ('Кол.', 35), ('Примечание', 150))
    pe_width = reduce(lambda a, b: a + b + table_bord,
                            zip(*pe_head)[1], table_bord)
    ss = '''
<!DOCTYPE html>
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=%s">
<TITLE>Перечень элементов (заготовка)</TITLE>
</HEAD>
<BODY>
  <TABLE cellspacing="0" border="%s"  width="%s">
    <TR>''' % (common.web_chr_set, table_bord, pe_width)
    for k, v in pe_head:  # не "map" Заголовок
        ss += '<TH width="%s">%s' % (v, k)

    peTitle_old = None
    set_RefDes = set()
    for i, compon in enumerate(components):  # components[-1:] + Перебор строк

        if peTitle_old != compon.peTitle:   # ? peTitleRepack
            peTitle_old = compon.peTitle    # ? peTitleRepack
            ss += '\n<TR>' + 4 * '<TD>&nbsp;'
            ss += ('\n<TR><TD>&nbsp;<TD align="center">'
                    '<Big><U>%s</U></Big><TD>&nbsp;<TD>&nbsp;'
                    ) % rc.tuple_tuple_to_color_str(peTitle_old)
            ss += '\n<TR>' + 4 * '<TD>&nbsp;'

        if flag_orig:
            if set_RefDes == set() or htmOrig_old == compon.htmOrig:
                set_RefDes.add(compon.RefDes)
            else:
                ss += ('\n<TR bgcolor=#E0FFFF><font color="red">' +
                            ('<TD colspan="4">%s | ' %
                            pcad_common.set_to_str(set_RefDes)) +  # , sep=','
                            htmOrig_old + (' | %s' % len(set_RefDes)))
                set_RefDes = {compon.RefDes}
            htmOrig_old = compon.htmOrig

            if 'peRowUnion' in compon.__dict__:
                ss += ('\n<TR bgcolor=#E0FFFF><font color="red">' +
                            ('<TD colspan="4">%s | ' %
                            pcad_common.set_to_str(set_RefDes)) +  # , sep=','
                            compon.htmOrig + (' | %s' % len(set_RefDes)))
                set_RefDes = set()

        if 'peRowUnion' in compon.__dict__:
            ss += '\n<TR>' + compon.peRowUnion

    ss += '''  </TABLE>
</BODY>
</HTML>'''

    printm("\n%s\n" % pe_fpne)
    try:
        fp = open(pe_fpne, 'w')
    except IOError:
        printm('    Неудались запись и открытие Файла. '
                            'Возможно он занят другой программой.\n')
        return
    fp.write(ss.encode(common.web_code))
    fp.close()
    #if  sys.platform in ('win32', 'win64'):
    if common.win:
        #if zap_pe == 1:
        printm('      Возможно, открытия файлов придётся '
                            'минутку подождать.\n')
        startfile(pe_fpne)
#..............................................................................
# <span style="background-color: #00ff00; color: #000000;">==Зеленый фон?==</span>
# <font size="5" color="blue">текст будет синего цвета, «пятого» размера</font>
# <p style="background: #0000ff;">Фон под текстом</p>
# <b style="background:#FFFFCC">Жирный текст.</b>
# <span style="background:#FFFFCC">Обычный текст.</span>
# <SPAN STYLE="BACKGROUND-COLOR: black;color:white">текст</span>


#------------------------------------------------------------------------------
def form_components():
    """ Получает список файлов, переданных в параметрах командной
    строки. Значение "_n_args" должно соответствовать требуемому
    количеству передаваемых файлов. """
    global sch_index, pcb_index
    global components

    components = []

    sch_index, pcb_index = pcad_common.ind_sch_pcb()

    if sch_index < 0 and pcb_index < 0:
        printm('    Ошибка! Нет файла - SCH и/или PCB.\n')
        return

    elif pcb_index < 0:
        printm('\n    Предупреждение! Файл только SCH, '
                        'можно лохануться с корпусами.\n\n')
        pcad_common.ExtractInf(sch_index)
        sch_components = pcad_common.ww[sch_index]['components']
        for RefDes, compon in sch_components.items():  # Компоненты схемы
            compon.set_properties()
        components = list(sch_components.values())

    elif sch_index < 0:
        printm('\n    Предупреждение! Файл только PCB, '
                        'можно лохануться с номиналами.\n\n')
        pcad_common.ww[sch_index]['fpn'] = pcad_common.ww[pcb_index]['fpn']
        pcad_common.ExtractInf(pcb_index)  # ????
        pcb_components = pcad_common.ww[pcb_index]['components']
        for RefDes, compon in pcb_components.items():  # Компоненты схемы
            compon.set_properties()
        components = list(pcb_components.values())

    else:  # elif sch_index >= 0 and pcb_index >= 0:

        sch_components = pcad_common.ww[sch_index]['components']
        pcb_components = pcad_common.ww[pcb_index]['components']

        # Необходимо к компонентам схемы добавить информацию о корпусах платы
        # Должен содерж инф необх для сортировки, для объединения и формирования
        #    окончательных раскрашенных строк, промежуточные раскрашенные строки
        params = {'attachedPattern', 'numPads', # Порядок не важен
                    'patternGraphicsNameDef', 'patternGraphicsNameRef'}
        for RefDes, compon in sch_components.items():  # Компоненты схемы
            for param in params:
                if (RefDes in pcb_components and
                        param in pcb_components[RefDes].__dict__):
                    setattr(compon, param,
                            getattr(pcb_components[RefDes], param))
            compon.set_properties()
        components = list(sch_components.values())
#..............................................................................


#------------------------------------------------------------------------------
def main(args):
    """ Получает список файлов, переданных в параметрах командной
    строки. Значение "_n_args" должно соответствовать требуемому
    количеству передаваемых файлов. """
    global sch_index, pcb_index
    global components

    for i, fpne in enumerate(args):
        pcad_common.ReadFile(fpne, i)

    sch_index, pcb_index = pcad_common.ind_sch_pcb()

    if sch_index < 0 and pcb_index < 0:
        printm('    Ошибка! Нет файла - SCH и/или PCB.\n')
        return

    elif pcb_index < 0:
        printm('\n    Предупреждение! Файл только SCH, '
                        'можно лохануться с корпусами.\n\n')
        pcad_common.ExtractInf(sch_index)
        sch_components = pcad_common.ww[sch_index]['components']
        for RefDes, compon in sch_components.items():  # Компоненты схемы
            compon.set_properties()
        components = sch_components.values()

    elif sch_index < 0:
        printm('\n    Предупреждение! Файл только PCB, '
                        'можно лохануться с номиналами.\n\n')
        pcad_common.ww[sch_index]['fpn'] = pcad_common.ww[pcb_index]['fpn']
        pcad_common.ExtractInf(pcb_index)
        pcb_components = pcad_common.ww[pcb_index]['components']
        for RefDes, compon in pcb_components.items():  # Компоненты схемы
            compon.set_properties()
        components = pcb_components.values()

    else:  # elif sch_index >= 0 and pcb_index >= 0:

        pcad_compare_cp.compare_lines()

        sch_components = pcad_common.ww[sch_index]['components']
        pcb_components = pcad_common.ww[pcb_index]['components']

        # Необходимо к компонентам схемы добавить информацию о корпусах платы
        # Должен содерж инф необх для сортировки, для объединения и формирования
        #    окончательных раскрашенных строк, промежуточные раскрашенные строки
        params = {'attachedPattern', 'numPads', # Порядок не важен
                    'patternGraphicsNameDef', 'patternGraphicsNameRef'}
        for RefDes, compon in sch_components.items():  # Компоненты схемы
            for param in params:
                if (RefDes in pcb_components and
                        param in pcb_components[RefDes].__dict__):
                    setattr(compon, param,
                            getattr(pcb_components[RefDes], param))
            compon.set_properties()
        components = sch_components.values()

    pe_fpne = pcad_common.ww[sch_index]['fpn'] + pe_suffix
    add_over_pe()
    build_pe(pe_fpne + '_tmp.html', flag_orig=True)#type_outfile='.html')
    build_pe(sp_fpne + '.html', flag_orig=False)#type_outfile='.html')

    sp_fpne = pcad_common.ww[sch_index]['fpn'] + sp_suffix
    add_over_sp()
    build_sp(sp_fpne + '_tmp.html', flag_orig=True)#type_outfile='.html')
    build_sp(sp_fpne + '.html', flag_orig=False)#type_outfile='.html')
#..............................................................................


#------------------------------------------------------------------------------
if __name__ == '__main__':

    from common import main0
    _n_args = [1,2]
    main0(main, _n_args)  # Нет необходимости трогать

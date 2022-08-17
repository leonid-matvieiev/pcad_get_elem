#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding: utf8

"""    Программа get_elem_tk.py - графическая оболочка для
    программы-модуля get_elem_cp.py (командной строки) для получения
    заготовок файлов "Перечня элементов" и "Спецификации" из PCB-файла. """

#                Автор: Л.М.Матвеев

from common import trm_code
import sys


#------------------------------------------------------------------------------
def printm(s):
    """ Печать Юникод-строк в терминал и скриптер.
        Автоматический перевод строки не производится. """
    sys.stdout.write(s)
    if prn_only:
        return
    txt.insert(END, s)
    txt.yview(END)
    root.update()
#..............................................................................
prn_only = True
# Переопределение функции печати
import common
common.printm = printm

import pcad_common
import pcad_compare_cp
import get_elem_cp
import radio_component

from os.path import split, splitext

#------------------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog
root = Tk()
root.title('  Сравнение PCAD-файлов, создание Спецификации и Перечня.')
root.resizable(False, False)  # запрет изм разм окна по гориз и по верт


fra1 = LabelFrame(root, text=' Лог операций ', labelanchor='n')
fra1.pack()
txt = Text(fra1, font="Verdana 10")
scr = Scrollbar(fra1, command=txt.yview)
txt.configure(yscrollcommand=scr.set)
scr.grid(row=0, column=1, sticky=NS, padx=3, pady=3)
txt.grid(row=0, column=0, padx=3, pady=4)

fpnes_ini_str = "\nfpnes_ini = ["
fpnes_ini = [
'D:/0d/OneDrive/W/MLM/Temes2/PC83-Pul',
    't/pcad/ai/Plata_AI_Ver_1_3_1.sch',
'D:/0d/OneDrive/W/MLM/Temes2/PC83-Pul',
    't/pcad/ai/Plata_AI-T_Ver_1_0.sch']
fpnes = [''.join(fpnes_ini[:2]), ''.join(fpnes_ini[2:])]


#------------------------------------------------------------------------------
def SelectFiles(i):
    """ Выбор исходных файлов. """
    if i == 0 or fpnes[1] == '':
        fp, fne = split(fpnes[0])
    else:
        fp, fne = split(fpnes[1])
    fpne = filedialog.askopenfilename(initialdir=fp,
            title='Выбор исходных файлов',
            initialfile=fne)
    if not fpne:
        return

    if i == 0:
        fpnes[0] = fpne
        LabelA['text'] = ''
        varFpneA.set('')
        #pcad_common.ww[0] ={}
        pcad_common.ReadFile(fpne, 0)
        k = len(pcad_common.ww[0].get('lines', []))
        if k:
            LabelA['text'] = k
            varFpneA.set(fpnes[0])
            edOpenFileA.xview_scroll(1000, UNITS)
    else:
        fpnes[1] = fpne
        LabelB['text'] = ''
        varFpneB.set('')
        #pcad_common.ww[1] ={}
        pcad_common.ReadFile(fpne, 1)
        k = len(pcad_common.ww[1]['lines'])
        if k:
            LabelB['text'] = k
            varFpneB.set(fpnes[1])
            edOpenFileB.xview_scroll(1000, UNITS)
    pcad_compare_cp.compare_complete = False
    BtnEnables()
#..............................................................................


#------------------------------------------------------------------------------
def ClearFilds(i):
    """ Очистка полей имён файлов. """
    pcad_common.ww[i] = {}
    if i == 0:
        LabelA['text'] = ''
        varFpneA.set('')
    else:
        LabelB['text'] = ''
        varFpneB.set('')
    pcad_compare_cp.compare_complete = False
    BtnEnables()
#..............................................................................


#------------------------------------------------------------------------------
def BtnEnables():
    """ Управление доступностью кнопок. """
    btCompare['state'] = DISABLED
    btWriteSP['state'] = DISABLED
    btWritePE['state'] = DISABLED

    if pcad_compare_cp.compare_complete:
        if (set([pcad_common.ww[i].get('ext') for i in range(2)]) ==
                {"PCB", "SCH"}):
            btWriteSP['state'] = NORMAL
            btWritePE['state'] = NORMAL
        else:
            pass
    elif pcad_common.fields_count('components') == 1:
            btWriteSP['state'] = NORMAL
            btWritePE['state'] = NORMAL

    elif pcad_common.fields_count('lines') == 2:
        btCompare['state'] = NORMAL

#..............................................................................


#------------------------------------------------------------------------------
def OpenFiles():
    """ Открытие исходных файлов. """
    printm('\n    Открытие исходных файлов\n')
    pcad_common.OpenFiles(fpnes)
    BtnEnables()
#..............................................................................


#------------------------------------------------------------------------------
def CompareFiles():
    """ Сравнение исходных файлов. """
    pcad_compare_cp.compare_lines()
    BtnEnables()
    printm('\nСравнение файлов выполнено!\n')
#..............................................................................


#------------------------------------------------------------------------------
def bindShortNames():
    radio_component.SPLIT_ORIGNAME = fShortNames.get()
    radio_component.SPLIT_PATTERN = fShortNames.get()
#..............................................................................


#------------------------------------------------------------------------------
def WritePE():
    """ Формирование заготовки файла Перечня элементов """
    get_elem_cp.sch_index, get_elem_cp.pcb_index = pcad_common.ind_sch_pcb()
    if get_elem_cp.sch_index < 0:
        pcad_common.ww[get_elem_cp.sch_index]['fpn'] = \
                pcad_common.ww[get_elem_cp.pcb_index]['fpn']
    fp, fn = split(pcad_common.ww[get_elem_cp.sch_index]['fpn'])
    fn = fn + get_elem_cp.pe_suffix
    fpne = filedialog.asksaveasfilename(initialdir=fp,
            title='Имя файла "Перечня элементов"',
            initialfile=fn,
            defaultextension=vFrmtFile.get(),
            filetypes=[('%s-файл' % vFrmtFile.get()[1:],
                        "*" + vFrmtFile.get())])
    if fpne:
         # Формирование, запись и открытие файла
        get_elem_cp.form_components()
        get_elem_cp.add_over_pe()
        if fNoCheckFile.get():
            get_elem_cp.build_pe(fpne, flag_orig=False)
        if fCheckFile.get():
            get_elem_cp.build_pe('_tmp'.join(splitext(fpne)), flag_orig=True)
#..............................................................................


#------------------------------------------------------------------------------
def WriteSP():
    """ Формирование заготовки файла Спецификации """
    get_elem_cp.sch_index, get_elem_cp.pcb_index = pcad_common.ind_sch_pcb()
    if get_elem_cp.sch_index < 0:
        pcad_common.ww[get_elem_cp.sch_index]['fpn'] = \
                pcad_common.ww[get_elem_cp.pcb_index]['fpn']
    fp, fn = split(pcad_common.ww[get_elem_cp.sch_index]['fpn'])
    fn = fn + get_elem_cp.sp_suffix
    fpne = filedialog.asksaveasfilename(initialdir=fp,
            title='Имя файла "Спецификации"',
            initialfile=fn,
            defaultextension=vFrmtFile.get(),
            filetypes=[('%s-файл' % vFrmtFile.get()[1:],
                        "*" + vFrmtFile.get())])
    if fpne:
         # Формирование, запись и открытие файла
        get_elem_cp.form_components()
        get_elem_cp.add_over_sp()
        if fNoCheckFile.get():
            get_elem_cp.build_sp(fpne, flag_orig=False)
        if fCheckFile.get():
            get_elem_cp.build_sp('_tmp'.join(splitext(fpne)), flag_orig=True)

#..............................................................................


#------------------------------------------------------------------------------
fra3 = LabelFrame(root, text=' Имена исходных PCAD-файлов ', labelanchor='n')
fra3.pack()

LabelA = Label(fra3, text='', width=7)
LabelB = Label(fra3, text='', width=7)
LabelA.grid(column=1, row=1)
LabelB.grid(column=1, row=2)

btSelectFileA = Button(fra3, text=">>", command=lambda: SelectFiles(0))
btSelectFileA.grid(column=3, row=1)
btSelectFileA.bind('<Button-1>')
btSelectFileA.focus_set()

btSelectFileB = Button(fra3, text=">>", command=lambda: SelectFiles(1))
btSelectFileB.grid(column=3, row=2)
btSelectFileB.bind('<Button-1>')

btClearFildA = Button(fra3, text=" - ", command=lambda: ClearFilds(0))
btClearFildA.grid(column=4, row=1, padx=3, pady=3)
btClearFildA.bind('<Button-1>')

btClearFildB = Button(fra3, text=" - ", command=lambda: ClearFilds(1))
btClearFildB.grid(column=4, row=2, padx=3, pady=3)
btClearFildB.bind('<Button-1>')

varFpneA = StringVar()
varFpneB = StringVar()
ed_width = (txt['width'] - LabelB['width'] -
            btSelectFileA['width'] - btClearFildA['width'] - 10)
edOpenFileA = Entry(fra3, bd=2, textvariable=varFpneA, width=ed_width)  # 95
edOpenFileB = Entry(fra3, bd=2, textvariable=varFpneB, width=ed_width)
edOpenFileA.grid(column=2, row=1, padx=3, pady=3, sticky=EW)  # , columnspan=5
edOpenFileB.grid(column=2, row=2, padx=3, pady=3, sticky=EW)

varFpneA.set(fpnes[0])
varFpneB.set(fpnes[1])

#------------------------------------------------------------------------------
fra4 = Frame(root)
fra4.pack()
#------------------------------------------------------------------------------
fra42 = LabelFrame(fra4, labelanchor='n',
    text=' параметры Сецификации и Перечня ')
fra42.pack(side=LEFT)

fra421 = Frame(fra42)
fra421.pack(side=LEFT)

vFrmtFile = StringVar()
vFrmtFile.set(".HTM")
rbXLS = Radiobutton(fra421, text="Вых. формат XLS", value=".XLS",
                variable=vFrmtFile, font="Verdana 8")
rbHTM = Radiobutton(fra421, text="Вых. формат HTM", value=".HTM",
                variable=vFrmtFile, font="Verdana 8")
rbDOC = Radiobutton(fra421, text="Вых. формат DOC", value=".DOC",
                variable=vFrmtFile, font="Verdana 8")
rbXLS.pack()
rbHTM.pack()
rbDOC.pack()

fra422 = Frame(fra42)
fra422.pack(side=LEFT)

fCheckFile = BooleanVar()
fNoCheckFile = BooleanVar()
fShortNames = BooleanVar()
cbCheckFile = Checkbutton(fra422, text="Файлы для контроля",
                variable=fCheckFile, onvalue=True, offvalue=False)
cbNoCheckFile = Checkbutton(fra422, text="Файлы без контроля",
                variable=fNoCheckFile, onvalue=True, offvalue=False)
cbShortNames = Checkbutton(fra422, text="Типы и Корпуса до _",
                variable=fShortNames, onvalue=True, offvalue=False,
                command=bindShortNames)

cbCheckFile.pack(padx=5,)
cbNoCheckFile.pack(padx=5)
cbShortNames.pack(padx=5)
fCheckFile.set(False)
fNoCheckFile.set(True)
fShortNames.set(False)
cbShortNames.bind('<Button-1>')

#------------------------------------------------------------------------------
fra43 = Frame(fra4)
fra43.pack(side=LEFT)

btCompare = Button(fra43, text="Сравнить", width=20,  # "Сравнить файлы"
                state=DISABLED, command=CompareFiles)
btCompare.bind('<Button-1>')
btCompare.pack(padx=5, pady=5)

btWritePE = Button(fra43, text='Перечень элементов',
                command=WritePE, width=20, state=DISABLED)
btWriteSP = Button(fra43, text='Спецификация',
                command=WriteSP, width=20, state=DISABLED)
btWritePE.pack(padx=5)
btWriteSP.pack(padx=5, pady=5)
btWritePE.bind('<Button-1>')
btWriteSP.bind('<Button-1>')
#------------------------------------------------------------------------------

prn_only = False
root.mainloop()
prn_only = True

from os.path import splitext
#------------------------------------------------------------------------------
# Сохранение полного имени последних исходных файлов
while (''.join(fpnes_ini[:2]) != fpnes[0] or
        ''.join(fpnes_ini[2:]) != fpnes[1]):
    if  splitext(__file__)[1].upper() == '.PYC':
        break

    fd = open(__file__, 'r', encoding='utf8')
    ss = fd.read()
    fd.close()

    i1 = ss.find(fpnes_ini_str)
    if i1 <= 0:
        break

    i1 += len(fpnes_ini_str)
    i2 = ss.find("]", i1)
    if i2 < i1:
        break

    x = []
    for fpne in fpnes:
        n = len(fpne) // 2 + 2
        x += [fpne[:n], fpne[n:]]
    s = "\n'%s',\n    '%s',\n'%s',\n    '%s'" % tuple(x)

    ss = ss[:i1] + s + ss[i2:]

    fd = open(__file__, 'w', encoding='utf8')  # , 'wb'
    #fd = open('_'.join(splitext(__file__)), 'wb')
    fd.write(ss)
    fd.close()
    printm('\n    Сохранение полных имён последних '
            'исходных файлов произведено.\n%s\n    %s\n%s\n    %s' %
            (x[0], x[1], x[2], x[3]))
    break

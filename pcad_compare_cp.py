#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Программа-модуль pcad_compare_cp.py (командной строки)
    для сравнения ПКАД файлов.   """

#                Автор: Л.М.Матвеев

import pcad_common
from common import printm

from os.path import split, splitext, exists, join


# Определяем отсутствие (несовпадение) соотв значений в компонентах
#    Интересует compValue, patternName, originalName
# Параметры элементов, для сравнения
params = None
params_const = {
    'attachedPattern': 'типов корпуса',  # HC-49
    'attachedSymbol': 'УГО',  # CRISTAL
    'compPin': 'обозначений выводов',  # set(['1"1', '2"2'])
    'compValue': 'номиналов',  # 18.432 MHz
##    'Mix': '',  # Набор нормализованных значений с ЕИ
    'numPads': 'количеств выводов корпуса',  # 2
    'numParts': 'количеств секций УГО',  # 1
    'numPins': 'количеств выводов УГО',  # 2
    'originalName': 'типов',  # QUARTZ
    'sourceLibrary': 'библиотек',  # G7_ROM-NEW.LIB
##    'patternGraphicsNameDef': 'набор изображений корпуса',  # Primary
##    'patternGraphicsNameRef': 'изображение корпуса',  # Primary
    }
w_unic_comps = []
nesovp_params = {}
unic_nets = []
renamed_nets = []
crossed_nodes = [{}, {}]
compare_complete = False


#------------------------------------------------------------------------------
def compare_dicts():
    """ Сравнивает компоненты и цепи обработанных файлов """
    global w_unic_comps, nesovp_params, unic_nets, renamed_nets
    global params, crossed_nodes

    if     (pcad_common.fields_count('nets') < 2 or
            pcad_common.fields_count('components') < 2):
        printm('\n    ОШИБКА! Недостаточно пригодных файлов для сравнения.\n')
        return

    # ******* Секция сравнения компонентов ********

    w_components = [w['components'] for w in pcad_common.ww]
    # Взаимно-отсутствующие компоненты
    w_unic_comps = [set(w_components[i]) - set(w_components[1 - i]) for i in range(2)]
    # Компоненты, имеющиеся в наличии в обоих файлах
    match_comps = set(w_components[0]) & set(w_components[1])

    # Определяем отсутствие (несовпадение) соотв значений в компонентах
    #    Интересует compValue, patternName, originalName ??????
    params = params_const.copy()
    if 'SCH' not in {pcad_common.ww[i].get('ext', '') for i in range(2)}:
        params.update({  # ??????? Для след запуска может не надо ??????
            'patternGraphicsNameDef': 'набор изображений корпуса',  # Primary
            'patternGraphicsNameRef': 'изображение корпуса',  # Primary
            })
    # Сравнение общих компонентов
    nesovp_params = {}
    for rdes in match_comps:
        for param in params:
            param_vals = tuple([getattr(w_components[i][rdes], param, None)
                    # По умолчанию можно и соответствующий пустой тип
                    for i in range(2)])  # д.б. tuple как ключ к словарю

            if param_vals[0] == param_vals[1]:
                continue

            if (param == 'compValue' and
                    w_components[0][rdes].Mix['norm'] ==
                    w_components[1][rdes].Mix['norm']):
                continue

            # Значит в список несовпадающих параметров
            # Адаптируем для ключа  # Строки и кортежи не трогаем
            param_vals = tuple([tuple(param_vals[i])
                if isinstance(param_vals[i], (list, type(set())))
                else param_vals[i] for i in range(2)])

            if param not in nesovp_params:
                nesovp_params[param] = {param_vals: {rdes}}
            elif param_vals not in nesovp_params[param]:
                nesovp_params[param][param_vals] = {rdes}
            else:
                nesovp_params[param][param_vals].add(rdes)

    # ******* Секция сравнения цепей  ********

    nets = [w['nets'] for w in pcad_common.ww]
    unic_nets = [list(nets[i].keys()) for i in range(2)]  # не tuple() !!!
    # Перед сравнением цепей исключаем выводы (узлы) сомпонентов (уник),
    # которые отсутствуют в симметричном файле
    for i in range(2):  # Для каждого файла
        for net in tuple(unic_nets[i]):  # Для каждого файла
            nodes = nets[i][net]
            for node in tuple(nodes):  # Для каздого вывода (узла)
                RefDes = node[0]
                if RefDes in w_unic_comps[i]:
                    nets[i][net].remove(node)  # Исключение вывода (узла)
            if len(nodes) < 2:
                unic_nets[i].remove(net)

    crossed_nodes = [{}, {}]
    renamed_nets = []
    common_nets = []
    crossed_nets = []
    net = ['', '']
    nodes = [{}, {}]

    for i in range(len(unic_nets[0]) - 1, -1, -1):
        net[0] = unic_nets[0][i]
        nodes[0] = nets[0][net[0]]
        for j in range(len(unic_nets[1]) - 1, -1, -1):
            net[1] = unic_nets[1][j]
            nodes[1] = nets[1][net[1]]
            if nodes[0] == nodes[1]:  # Если цепи совпадают
                if net[0] != net[1]:  # Запоминание переименованых
                    renamed_nets.append((net[0], net[1]))
                common_nets.append((net[0], net[1]))
                break
            if nodes[0] & nodes[1]:  # Если цепи перекрываются
                # Запоминание перекрывающихся цепей
                crossed_nets.append((net[0], net[1]))
                for k in range(2):
                    dnodes = nodes[k] - nodes[1 - k]
                    if dnodes:
                        if net[k] not in crossed_nodes[k]:
                            crossed_nodes[k][net[k]] = {net[1 - k]:dnodes}
                        else:
                            crossed_nodes[k][net[k]][net[1 - k]] = dnodes

    for net0, net1 in common_nets + crossed_nets:
        # Исключение совпадающих и перекрывающихся
        if net0 in unic_nets[0]:
            unic_nets[0].remove(net0)
        if net1 in unic_nets[1]:
            unic_nets[1].remove(net1)
#..............................................................................


#------------------------------------------------------------------------------
def otobr_all():
    """ Отображает результат сравнения файлов. """
    #global w_unic_comps, nesovp_params, unic_nets, renamed_nets, crossed_nets

    printm('\n    Несоответствия, найденные в результате сравнения компонентов:\n')

    for i in range(2):
        if w_unic_comps[i]:
            printm('\n    В %s-ом файле уникальных компонентов - %s шт: ' %
                                  (i + 1, len(w_unic_comps[i])))
            printm(pcad_common.set_to_str(w_unic_comps[i]) + '\n')

    for param in nesovp_params:
        printm('\n    Несовпадения %s компонентов.\n' % params[param])
        twos = []
        for vs in nesovp_params[param]:
            rds = nesovp_params[param][vs]
            two = (pcad_common.set_to_str(rds) + '\n',
                ('    В 1-ом файле "%s", во 2-ом "%s" ' +
                '- %s шт: ') % (vs + (len(rds),)))
            twos.append(two)
        twos.sort()
        for two in twos:
            printm(two[1] + two[0])

    printm('\n    Несоответствия, найденные в результате сравнения цепей:\n')

    if renamed_nets:  # Переименованные цепи
        printm('\n    В нетлистах 1-го и 2-го файлов '
                'разные имена одинаковых цепей: ')
        s = ''
        for ns in renamed_nets:
            s += ', %s - %s' % ns
        printm(s[2:] + '\n')

    for i in range(2):  # Уникальные цепи
        u = unic_nets[i]
        if not u:
            continue
        printm('\n    В %s-ом файле уник цепей - %s шт: ' % (i + 1, len(u)))
        printm(pcad_common.set_to_str(u) + '\n')

    printm('\n')
    for i in range(2):  # Перекрывающиеся цепи
        for net in crossed_nodes[i]:
            nets2 = crossed_nodes[i][net]
            for net2 in nets2:
                nodes = nets2[net2]
                printm(('    К цепи %s %s-го файла '
                        'относительно %s %s-го доп подкл %s выв: ') %
                        (net, i + 1, net2, 2 - i, len(nodes)))
                printm(set_to_str(nodes))
#..............................................................................


#------------------------------------------------------------------------------
def set_to_str(nodes):  # Сделать другой для узлов
    """ . """
    return pcad_common.set_to_str(
                    {'-'.join(reversed(node)) for node in nodes}
                    #{'-'.join(node) for node in nodes}  # Вид как в менеджере
                    ) + '\n'
#..............................................................................


#------------------------------------------------------------------------------
def compare_lines():
    """ . """
    global compare_complete

    if pcad_common.fields_count('lines') < 2:
        printm('\n    ОШИБКА! Нет двух считанных файлов для обработки.\n')
        return

    if     (pcad_common.fields_count('nets') < 2 or
            pcad_common.fields_count('components') < 2):
        printm('\n    ОШИБКА! Нет двух пригодных файлов для сравнения.\n')
        return

    compare_dicts()
    otobr_all()
    compare_complete = True
#..............................................................................


#------------------------------------------------------------------------------
def main(args):
    """ Получает список файлов, переданных в параметрах командной
    строки. Значение "_n_args" должно соответствовать требуемому
    количеству передаваемых файлов. """

    for i, fpne in enumerate(args):
        pcad_common.ReadFile(fpne, i)

    compare_lines()
#..............................................................................


#------------------------------------------------------------------------------
if __name__ == '__main__':

    from common import main0
    _n_args = [2]
    main0(main, _n_args)  # Нет необходимости трогать

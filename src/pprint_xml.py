#!/usr/bin/env python
# coding: utf-8

#
# Как оказалось, в стандартной поставке Python до сих пор нет адекватного
# способа записать форматированный xml (так как использовать параметры indent, addindent, newl
# нельзя при перезаписи xml); потому для работы записываем raw-xml, а этот скрипт поможет его
# просмотреть
#

import xmldom

if __name__ == '__main__':
    from parse_options import parse_one_arg
    fpath = parse_one_arg("data.xml")

    print xmldom.parse(fpath).toprettyxml(encoding="utf-8")
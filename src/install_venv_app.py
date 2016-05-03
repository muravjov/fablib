#!/usr/bin/env python
# coding: utf-8

#
# install_venv_app - утилита прописывания пути к приложению посредством механизма .pth/site.py
#
# Причина: для конечных web-приложений на Python не требуется полноценная упаковка в пакеты для virtualenv,
# так как они только потребители кода других библиотек; однако прописаться в .pth venv-а со временем становится
# необходимой потребностью
#
# Для этого данный скрипт на лету создает в venv-е минимальный пакет, единственно важное действие которого - добавить
# в easy_install.pth указанную вторым аргументом папку

# Расчет папки в venv, где будут находиться .pth:
#
# distutils.dist.py: Distribution.get_command_obj("install") => Command.ensure_finalized(self) =>
# =>  distutils/command/install.py : install.finalize_options
# 
# См. шаблоны в INSTALL_SCHEMES, например:
# 'unix_prefix': {
#     'purelib': '$base/lib/python$py_version_short/site-packages',
#     'platlib': '$platbase/lib/python$py_version_short/site-packages',
#     'headers': '$base/include/python$py_version_short/$dist_name',
#     'scripts': '$base/bin',
#     'data'   : '$base',
# },
#
# Собственно обновление .pth проходит в setuptools/command/easy_install.py: update_pth()

import os

def install(pkg_name, src_path):
    # :TRICKY: приходится менять путь
    old_dir = os.getcwd()
    os.chdir(src_path)
    
    try:
        from setuptools import setup
        
        setup(
            name = pkg_name,
            version = 1,    
        
            # выбор директории, которая будет прописана в .pth - см. код egg_info.finalize_options():
            #     self.egg_base = (self.distribution.package_dir or {}).get('',os.curdir)
            #package_dir = {'': 'src'},
            
            # с этими же аргументами запускает setup.py и venv/pip install -e src_path,
            # см. install_editable()
            script_args = ["develop", "--no-deps"],
            
            script_name = '', # :KLUDGE: без setup.py (но warning остается)
        )
    finally:
        os.chdir(old_dir)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pkg_name")
    parser.add_argument("src_path")
    args = parser.parse_args()
    
    install(args.pkg_name, args.src_path)
    
if __name__ == "__main__":
    main()
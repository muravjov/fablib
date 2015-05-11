# coding: utf-8

# Note: This is from Guido van Rossums "Unifying types and classes in
# Python 2.2" metaclass example.
# http://www.python.org/download/releases/2.2/descrintro/

class _autosuper (type) :
    def __init__ (cls, name, bases, dict) :
        super   (_autosuper, cls).__init__ (name, bases, dict)
        setattr (cls, "_%s__super" % name, super (cls))
    # end def __init__
# end class _autosuper

class Autosuper(object):
    __metaclass__ = _autosuper
    pass
# end class autosuper

# ##############
# Для старых классов (не порожденных от object) пользуемся так:
#   make_super_for_classic_class(MyOld, Old)
# , установить после (!) описания класса MyOld

class Super(object):
    ''' По примеру http://www.python.org/download/releases/2.2/descrintro/#superexample '''
    def __init__(self, typ, obj):
        self.typ = typ
        self.obj = obj
    def __getattr__(self, attr):
        dct = self.typ.__dict__
        if attr in dct:
            x = dct[attr]
            if hasattr(x, "__get__"):
                # привязка метода x к объекту self.obj
                x = x.__get__(self.obj)
            return x
        raise AttributeError, attr

def make_super_for_classic_class(cls, parent_cls):
    def get_super_attr(obj):
        return Super(parent_cls, obj)
    # добавляем атрибут __super через setattr из-за скрытности первого
    # вне класса cls
    setattr(cls, "_%s__super" % cls.__name__, property(get_super_attr))

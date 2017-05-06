# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_PyBoolean')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_PyBoolean')
    _PyBoolean = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_PyBoolean', [dirname(__file__)])
        except ImportError:
            import _PyBoolean
            return _PyBoolean
        try:
            _mod = imp.load_module('_PyBoolean', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _PyBoolean = swig_import_helper()
    del swig_import_helper
else:
    import _PyBoolean
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

SHARED_PTR_DISOWN = _PyBoolean.SHARED_PTR_DISOWN
class BooleanEngine(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BooleanEngine, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BooleanEngine, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    if _newclass:
        create = staticmethod(_PyBoolean.BooleanEngine_create)
    else:
        create = _PyBoolean.BooleanEngine_create
    __swig_destroy__ = _PyBoolean.delete_BooleanEngine
    __del__ = lambda self: None

    def set_mesh_1(self, vertices, faces):
        return _PyBoolean.BooleanEngine_set_mesh_1(self, vertices, faces)

    def set_mesh_2(self, vertices, faces):
        return _PyBoolean.BooleanEngine_set_mesh_2(self, vertices, faces)

    def get_vertices(self):
        return _PyBoolean.BooleanEngine_get_vertices(self)

    def get_faces(self):
        return _PyBoolean.BooleanEngine_get_faces(self)

    def clean_up(self):
        return _PyBoolean.BooleanEngine_clean_up(self)

    def compute_union(self):
        return _PyBoolean.BooleanEngine_compute_union(self)

    def compute_intersection(self):
        return _PyBoolean.BooleanEngine_compute_intersection(self)

    def compute_difference(self):
        return _PyBoolean.BooleanEngine_compute_difference(self)

    def compute_symmetric_difference(self):
        return _PyBoolean.BooleanEngine_compute_symmetric_difference(self)

    def get_face_sources(self):
        return _PyBoolean.BooleanEngine_get_face_sources(self)

    def serialize_xml(self, filename):
        return _PyBoolean.BooleanEngine_serialize_xml(self, filename)
BooleanEngine_swigregister = _PyBoolean.BooleanEngine_swigregister
BooleanEngine_swigregister(BooleanEngine)

def BooleanEngine_create(engine_name):
    return _PyBoolean.BooleanEngine_create(engine_name)
BooleanEngine_create = _PyBoolean.BooleanEngine_create

class CSGTree(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSGTree, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CSGTree, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    if _newclass:
        create = staticmethod(_PyBoolean.CSGTree_create)
    else:
        create = _PyBoolean.CSGTree_create
    if _newclass:
        create_leaf = staticmethod(_PyBoolean.CSGTree_create_leaf)
    else:
        create_leaf = _PyBoolean.CSGTree_create_leaf
    __swig_destroy__ = _PyBoolean.delete_CSGTree
    __del__ = lambda self: None

    def set_operand_1(self, tree):
        return _PyBoolean.CSGTree_set_operand_1(self, tree)

    def set_operand_2(self, tree):
        return _PyBoolean.CSGTree_set_operand_2(self, tree)

    def compute_union(self):
        return _PyBoolean.CSGTree_compute_union(self)

    def compute_intersection(self):
        return _PyBoolean.CSGTree_compute_intersection(self)

    def compute_difference(self):
        return _PyBoolean.CSGTree_compute_difference(self)

    def compute_symmetric_difference(self):
        return _PyBoolean.CSGTree_compute_symmetric_difference(self)

    def get_face_sources(self):
        return _PyBoolean.CSGTree_get_face_sources(self)

    def get_mesh_sources(self):
        return _PyBoolean.CSGTree_get_mesh_sources(self)

    def get_vertices(self):
        return _PyBoolean.CSGTree_get_vertices(self)

    def get_faces(self):
        return _PyBoolean.CSGTree_get_faces(self)

    def get_num_vertices(self):
        return _PyBoolean.CSGTree_get_num_vertices(self)

    def get_num_faces(self):
        return _PyBoolean.CSGTree_get_num_faces(self)
CSGTree_swigregister = _PyBoolean.CSGTree_swigregister
CSGTree_swigregister(CSGTree)

def CSGTree_create(engine_name):
    return _PyBoolean.CSGTree_create(engine_name)
CSGTree_create = _PyBoolean.CSGTree_create

def CSGTree_create_leaf(engine_name, vertices, faces):
    return _PyBoolean.CSGTree_create_leaf(engine_name, vertices, faces)
CSGTree_create_leaf = _PyBoolean.CSGTree_create_leaf

# This file is compatible with both classic and new-style classes.



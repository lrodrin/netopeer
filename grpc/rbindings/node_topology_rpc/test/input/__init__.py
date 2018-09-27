# -*- coding: utf-8 -*-
from collections import OrderedDict

import six
from pyangbind.lib.base import PybindBase
from pyangbind.lib.yangtypes import YANGDynClass

# PY3 support of some PY2 keywords (needs improved)
if six.PY3:
    import builtins as __builtin__

    long = int
elif six.PY2:
    import __builtin__

from . import input_container


class input(PybindBase):
    """
    This class was auto-generated by the PythonClass plugin for PYANG
    from YANG module node-topology - based on the path /node_topology_rpc/test/input. Each member element of
    the container is represented as a class variable - with a specific
    YANG type.
    """
    __slots__ = ('_path_helper', '_extmethods', '__input_container',)

    _yang_name = 'input'

    _pybind_generated_by = 'container'

    def __init__(self, *args, **kwargs):

        self._path_helper = False

        self._extmethods = False
        self.__input_container = YANGDynClass(base=input_container.input_container, is_container='container',
                                              yang_name="input-container", parent=self, path_helper=self._path_helper,
                                              extmethods=self._extmethods, register_paths=False, extensions=None,
                                              namespace='urn:node-topology', defining_module='node-topology',
                                              yang_type='container', is_config=True)

        load = kwargs.pop("load", None)
        if args:
            if len(args) > 1:
                raise TypeError("cannot create a YANG container with >1 argument")
            all_attr = True
            for e in self._pyangbind_elements:
                if not hasattr(args[0], e):
                    all_attr = False
                    break
            if not all_attr:
                raise ValueError("Supplied object did not have the correct attributes")
            for e in self._pyangbind_elements:
                nobj = getattr(args[0], e)
                if nobj._changed() is False:
                    continue
                setmethod = getattr(self, "_set_%s" % e)
                if load is None:
                    setmethod(getattr(args[0], e))
                else:
                    setmethod(getattr(args[0], e), load=load)

    def _path(self):
        if hasattr(self, "_parent"):
            return self._parent._path() + [self._yang_name]
        else:
            return [u'node_topology_rpc', u'test', u'input']

    def _get_input_container(self):
        """
        Getter method for input_container, mapped from YANG variable /node_topology_rpc/test/input/input_container (container)
        """
        return self.__input_container

    def _set_input_container(self, v, load=False):
        """
        Setter method for input_container, mapped from YANG variable /node_topology_rpc/test/input/input_container (container)
        If this variable is read-only (config: false) in the
        source YANG file, then _set_input_container is considered as a private
        method. Backends looking to populate this variable should
        do so via calling thisObj._set_input_container() directly.
        """
        if hasattr(v, "_utype"):
            v = v._utype(v)
        try:
            t = YANGDynClass(v, base=input_container.input_container, is_container='container',
                             yang_name="input-container", parent=self, path_helper=self._path_helper,
                             extmethods=self._extmethods, register_paths=False, extensions=None,
                             namespace='urn:node-topology', defining_module='node-topology', yang_type='container',
                             is_config=True)
        except (TypeError, ValueError):
            raise ValueError({
                'error-string': """input_container must be of a type compatible with container""",
                'defined-type': "container",
                'generated-type': """YANGDynClass(base=input_container.input_container, is_container='container', yang_name="input-container", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=False, extensions=None, namespace='urn:node-topology', defining_module='node-topology', yang_type='container', is_config=True)""",
            })

        self.__input_container = t
        if hasattr(self, '_set'):
            self._set()

    def _unset_input_container(self):
        self.__input_container = YANGDynClass(base=input_container.input_container, is_container='container',
                                              yang_name="input-container", parent=self, path_helper=self._path_helper,
                                              extmethods=self._extmethods, register_paths=False, extensions=None,
                                              namespace='urn:node-topology', defining_module='node-topology',
                                              yang_type='container', is_config=True)

    input_container = __builtin__.property(_get_input_container, _set_input_container)

    _pyangbind_elements = OrderedDict([('input_container', input_container), ])

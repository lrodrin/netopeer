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


class nominal_central_frequency(PybindBase):
    """
    This class was auto-generated by the PythonClass plugin for PYANG
    from YANG module node-topology - based on the path /node/port/available-core/available-frequency-slot/nominal-central-frequency. Each member element of
    the container is represented as a class variable - with a specific
    YANG type.
    """
    __slots__ = ('_path_helper', '_extmethods', '__grid_type', '__adjustment_granularity', '__channel_number',)

    _yang_name = 'nominal-central-frequency'

    _pybind_generated_by = 'container'

    def __init__(self, *args, **kwargs):

        self._path_helper = False

        self._extmethods = False
        self.__channel_number = YANGDynClass(base=six.text_type, is_leaf=True, yang_name="channel-number", parent=self,
                                             path_helper=self._path_helper, extmethods=self._extmethods,
                                             register_paths=True, namespace='urn:node-topology',
                                             defining_module='node-topology', yang_type='string', is_config=True)
        self.__adjustment_granularity = YANGDynClass(base=six.text_type, is_leaf=True,
                                                     yang_name="adjustment-granularity", parent=self,
                                                     path_helper=self._path_helper, extmethods=self._extmethods,
                                                     register_paths=True, namespace='urn:node-topology',
                                                     defining_module='node-topology', yang_type='string',
                                                     is_config=True)
        self.__grid_type = YANGDynClass(base=six.text_type, is_leaf=True, yang_name="grid-type", parent=self,
                                        path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True,
                                        namespace='urn:node-topology', defining_module='node-topology',
                                        yang_type='string', is_config=True)

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
            return [u'node', u'port', u'available-core', u'available-frequency-slot', u'nominal-central-frequency']

    def _get_grid_type(self):
        """
        Getter method for grid_type, mapped from YANG variable /node/port/available_core/available_frequency_slot/nominal_central_frequency/grid_type (string)
        """
        return self.__grid_type

    def _set_grid_type(self, v, load=False):
        """
        Setter method for grid_type, mapped from YANG variable /node/port/available_core/available_frequency_slot/nominal_central_frequency/grid_type (string)
        If this variable is read-only (config: false) in the
        source YANG file, then _set_grid_type is considered as a private
        method. Backends looking to populate this variable should
        do so via calling thisObj._set_grid_type() directly.
        """
        if hasattr(v, "_utype"):
            v = v._utype(v)
        try:
            t = YANGDynClass(v, base=six.text_type, is_leaf=True, yang_name="grid-type", parent=self,
                             path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True,
                             namespace='urn:node-topology', defining_module='node-topology', yang_type='string',
                             is_config=True)
        except (TypeError, ValueError):
            raise ValueError({
                'error-string': """grid_type must be of a type compatible with string""",
                'defined-type': "string",
                'generated-type': """YANGDynClass(base=six.text_type, is_leaf=True, yang_name="grid-type", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='urn:node-topology', defining_module='node-topology', yang_type='string', is_config=True)""",
            })

        self.__grid_type = t
        if hasattr(self, '_set'):
            self._set()

    def _unset_grid_type(self):
        self.__grid_type = YANGDynClass(base=six.text_type, is_leaf=True, yang_name="grid-type", parent=self,
                                        path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True,
                                        namespace='urn:node-topology', defining_module='node-topology',
                                        yang_type='string', is_config=True)

    def _get_adjustment_granularity(self):
        """
        Getter method for adjustment_granularity, mapped from YANG variable /node/port/available_core/available_frequency_slot/nominal_central_frequency/adjustment_granularity (string)
        """
        return self.__adjustment_granularity

    def _set_adjustment_granularity(self, v, load=False):
        """
        Setter method for adjustment_granularity, mapped from YANG variable /node/port/available_core/available_frequency_slot/nominal_central_frequency/adjustment_granularity (string)
        If this variable is read-only (config: false) in the
        source YANG file, then _set_adjustment_granularity is considered as a private
        method. Backends looking to populate this variable should
        do so via calling thisObj._set_adjustment_granularity() directly.
        """
        if hasattr(v, "_utype"):
            v = v._utype(v)
        try:
            t = YANGDynClass(v, base=six.text_type, is_leaf=True, yang_name="adjustment-granularity", parent=self,
                             path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True,
                             namespace='urn:node-topology', defining_module='node-topology', yang_type='string',
                             is_config=True)
        except (TypeError, ValueError):
            raise ValueError({
                'error-string': """adjustment_granularity must be of a type compatible with string""",
                'defined-type': "string",
                'generated-type': """YANGDynClass(base=six.text_type, is_leaf=True, yang_name="adjustment-granularity", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='urn:node-topology', defining_module='node-topology', yang_type='string', is_config=True)""",
            })

        self.__adjustment_granularity = t
        if hasattr(self, '_set'):
            self._set()

    def _unset_adjustment_granularity(self):
        self.__adjustment_granularity = YANGDynClass(base=six.text_type, is_leaf=True,
                                                     yang_name="adjustment-granularity", parent=self,
                                                     path_helper=self._path_helper, extmethods=self._extmethods,
                                                     register_paths=True, namespace='urn:node-topology',
                                                     defining_module='node-topology', yang_type='string',
                                                     is_config=True)

    def _get_channel_number(self):
        """
        Getter method for channel_number, mapped from YANG variable /node/port/available_core/available_frequency_slot/nominal_central_frequency/channel_number (string)
        """
        return self.__channel_number

    def _set_channel_number(self, v, load=False):
        """
        Setter method for channel_number, mapped from YANG variable /node/port/available_core/available_frequency_slot/nominal_central_frequency/channel_number (string)
        If this variable is read-only (config: false) in the
        source YANG file, then _set_channel_number is considered as a private
        method. Backends looking to populate this variable should
        do so via calling thisObj._set_channel_number() directly.
        """
        if hasattr(v, "_utype"):
            v = v._utype(v)
        try:
            t = YANGDynClass(v, base=six.text_type, is_leaf=True, yang_name="channel-number", parent=self,
                             path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True,
                             namespace='urn:node-topology', defining_module='node-topology', yang_type='string',
                             is_config=True)
        except (TypeError, ValueError):
            raise ValueError({
                'error-string': """channel_number must be of a type compatible with string""",
                'defined-type': "string",
                'generated-type': """YANGDynClass(base=six.text_type, is_leaf=True, yang_name="channel-number", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='urn:node-topology', defining_module='node-topology', yang_type='string', is_config=True)""",
            })

        self.__channel_number = t
        if hasattr(self, '_set'):
            self._set()

    def _unset_channel_number(self):
        self.__channel_number = YANGDynClass(base=six.text_type, is_leaf=True, yang_name="channel-number", parent=self,
                                             path_helper=self._path_helper, extmethods=self._extmethods,
                                             register_paths=True, namespace='urn:node-topology',
                                             defining_module='node-topology', yang_type='string', is_config=True)

    grid_type = __builtin__.property(_get_grid_type, _set_grid_type)
    adjustment_granularity = __builtin__.property(_get_adjustment_granularity, _set_adjustment_granularity)
    channel_number = __builtin__.property(_get_channel_number, _set_channel_number)

    _pyangbind_elements = OrderedDict([('grid_type', grid_type), ('adjustment_granularity', adjustment_granularity),
                                       ('channel_number', channel_number), ])

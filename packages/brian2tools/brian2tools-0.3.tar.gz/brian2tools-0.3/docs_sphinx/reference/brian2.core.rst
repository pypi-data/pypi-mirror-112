core package
============

.. automodule:: brian2.core
    :show-inheritance:


:mod:`base` module
------------------

.. automodule:: brian2.core.base
    :show-inheritance:

**Classes**

.. autosummary:: BrianObject
    :toctree:

.. autosummary:: BrianObjectException
    :toctree:

**Functions**

.. autosummary:: brian_object_exception
    :toctree:

.. autosummary:: device_override
    :toctree:

.. autosummary:: weakproxy_with_fallback
    :toctree:


:mod:`clocks` module
--------------------

.. automodule:: brian2.core.clocks
    :show-inheritance:

**Classes**

.. autosummary:: Clock
    :toctree:

.. autosummary:: DefaultClockProxy
    :toctree:

**Functions**

.. autosummary:: check_dt
    :toctree:

**Objects**

.. autosummary:: defaultclock
    :toctree:


:mod:`core_preferences` module
------------------------------

.. automodule:: brian2.core.core_preferences
    :show-inheritance:

**Functions**

.. autosummary:: default_float_dtype_validator
    :toctree:

.. autosummary:: dtype_repr
    :toctree:


:mod:`functions` module
-----------------------

.. automodule:: brian2.core.functions
    :show-inheritance:

**Classes**

.. autosummary:: Function
    :toctree:

.. autosummary:: FunctionImplementation
    :toctree:

.. autosummary:: FunctionImplementationContainer
    :toctree:

.. autosummary:: SymbolicConstant
    :toctree:

.. autosummary:: log10
    :toctree:

**Functions**

.. autosummary:: declare_types
    :toctree:

.. autosummary:: implementation
    :toctree:

.. autosummary:: timestep
    :toctree:


:mod:`magic` module
-------------------

.. automodule:: brian2.core.magic
    :show-inheritance:

**Classes**

.. autosummary:: MagicError
    :toctree:

.. autosummary:: MagicNetwork
    :toctree:

**Functions**

.. autosummary:: collect
    :toctree:

.. autosummary:: get_objects_in_namespace
    :toctree:

.. autosummary:: restore
    :toctree:

.. autosummary:: run
    :toctree:

.. autosummary:: start_scope
    :toctree:

.. autosummary:: stop
    :toctree:

.. autosummary:: store
    :toctree:

**Objects**

.. autosummary:: magic_network
    :toctree:


:mod:`names` module
-------------------

.. automodule:: brian2.core.names
    :show-inheritance:

**Classes**

.. autosummary:: Nameable
    :toctree:

**Functions**

.. autosummary:: find_name
    :toctree:


:mod:`namespace` module
-----------------------

.. automodule:: brian2.core.namespace
    :show-inheritance:

**Functions**

.. autosummary:: get_local_namespace
    :toctree:


:mod:`network` module
---------------------

.. automodule:: brian2.core.network
    :show-inheritance:

**Classes**

.. autosummary:: Network
    :toctree:

.. autosummary:: ProfilingSummary
    :toctree:

.. autosummary:: SchedulingSummary
    :toctree:

.. autosummary:: TextReport
    :toctree:

**Functions**

.. autosummary:: profiling_summary
    :toctree:

.. autosummary:: schedule_propagation_offset
    :toctree:

.. autosummary:: scheduling_summary
    :toctree:


:mod:`operations` module
------------------------

.. automodule:: brian2.core.operations
    :show-inheritance:

**Classes**

.. autosummary:: NetworkOperation
    :toctree:

**Functions**

.. autosummary:: network_operation
    :toctree:


:mod:`preferences` module
-------------------------

.. automodule:: brian2.core.preferences
    :show-inheritance:

**Classes**

.. autosummary:: BrianGlobalPreferences
    :toctree:

.. autosummary:: BrianGlobalPreferencesView
    :toctree:

.. autosummary:: BrianPreference
    :toctree:

.. autosummary:: DefaultValidator
    :toctree:

.. autosummary:: ErrorRaiser
    :toctree:

.. autosummary:: PreferenceError
    :toctree:

**Functions**

.. autosummary:: check_preference_name
    :toctree:

.. autosummary:: parse_preference_name
    :toctree:

**Objects**

.. autosummary:: brian_prefs
    :toctree:

.. autosummary:: prefs
    :toctree:


:mod:`spikesource` module
-------------------------

.. automodule:: brian2.core.spikesource
    :show-inheritance:

**Classes**

.. autosummary:: SpikeSource
    :toctree:


:mod:`tracking` module
----------------------

.. automodule:: brian2.core.tracking
    :show-inheritance:

**Classes**

.. autosummary:: InstanceFollower
    :toctree:

.. autosummary:: InstanceTrackerSet
    :toctree:

.. autosummary:: Trackable
    :toctree:


:mod:`variables` module
-----------------------

.. automodule:: brian2.core.variables
    :show-inheritance:

**Classes**

.. autosummary:: ArrayVariable
    :toctree:

.. autosummary:: AuxiliaryVariable
    :toctree:

.. autosummary:: Constant
    :toctree:

.. autosummary:: DynamicArrayVariable
    :toctree:

.. autosummary:: LinkedVariable
    :toctree:

.. autosummary:: Subexpression
    :toctree:

.. autosummary:: Variable
    :toctree:

.. autosummary:: VariableView
    :toctree:

.. autosummary:: Variables
    :toctree:

**Functions**

.. autosummary:: get_dtype
    :toctree:

.. autosummary:: get_dtype_str
    :toctree:

.. autosummary:: linked_var
    :toctree:

.. autosummary:: variables_by_owner
    :toctree:



stateupdaters package
=====================

.. automodule:: brian2.stateupdaters
    :show-inheritance:


:mod:`GSL` module
-----------------

.. automodule:: brian2.stateupdaters.GSL
    :show-inheritance:

**Classes**

.. autosummary:: GSLContainer
    :toctree:

.. autosummary:: GSLStateUpdater
    :toctree:

**Objects**

.. autosummary:: gsl_rk2
    :toctree:

.. autosummary:: gsl_rk4
    :toctree:

.. autosummary:: gsl_rk8pd
    :toctree:

.. autosummary:: gsl_rkck
    :toctree:

.. autosummary:: gsl_rkf45
    :toctree:


:mod:`base` module
------------------

.. automodule:: brian2.stateupdaters.base
    :show-inheritance:

**Classes**

.. autosummary:: StateUpdateMethod
    :toctree:

.. autosummary:: UnsupportedEquationsException
    :toctree:

**Functions**

.. autosummary:: extract_method_options
    :toctree:


:mod:`exact` module
-------------------

.. automodule:: brian2.stateupdaters.exact
    :show-inheritance:

**Classes**

.. autosummary:: IndependentStateUpdater
    :toctree:

.. autosummary:: LinearStateUpdater
    :toctree:

**Functions**

.. autosummary:: get_linear_system
    :toctree:

**Objects**

.. autosummary:: exact
    :toctree:

.. autosummary:: independent
    :toctree:

.. autosummary:: linear
    :toctree:


:mod:`explicit` module
----------------------

.. automodule:: brian2.stateupdaters.explicit
    :show-inheritance:

**Classes**

.. autosummary:: ExplicitStateUpdater
    :toctree:

**Functions**

.. autosummary:: diagonal_noise
    :toctree:

.. autosummary:: split_expression
    :toctree:

**Objects**

.. autosummary:: euler
    :toctree:

.. autosummary:: heun
    :toctree:

.. autosummary:: milstein
    :toctree:

.. autosummary:: rk2
    :toctree:

.. autosummary:: rk4
    :toctree:


:mod:`exponential_euler` module
-------------------------------

.. automodule:: brian2.stateupdaters.exponential_euler
    :show-inheritance:

**Classes**

.. autosummary:: ExponentialEulerStateUpdater
    :toctree:

**Functions**

.. autosummary:: get_conditionally_linear_system
    :toctree:

**Objects**

.. autosummary:: exponential_euler
    :toctree:



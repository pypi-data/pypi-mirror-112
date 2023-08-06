codegen package
===============

.. automodule:: brian2.codegen
    :show-inheritance:


:mod:`_prefs` module
--------------------

.. automodule:: brian2.codegen._prefs
    :show-inheritance:


:mod:`codeobject` module
------------------------

.. automodule:: brian2.codegen.codeobject
    :show-inheritance:

**Classes**

.. autosummary:: CodeObject
    :toctree:

**Functions**

.. autosummary:: check_compiler_kwds
    :toctree:

.. autosummary:: constant_or_scalar
    :toctree:

.. autosummary:: create_runner_codeobj
    :toctree:


:mod:`cpp_prefs` module
-----------------------

.. automodule:: brian2.codegen.cpp_prefs
    :show-inheritance:

**Functions**

.. autosummary:: get_compiler_and_args
    :toctree:

.. autosummary:: update_for_cross_compilation
    :toctree:


:mod:`get_cpu_flags` module
---------------------------

.. automodule:: brian2.codegen.get_cpu_flags
    :show-inheritance:


:mod:`optimisation` module
--------------------------

.. automodule:: brian2.codegen.optimisation
    :show-inheritance:

**Classes**

.. autosummary:: ArithmeticSimplifier
    :toctree:

.. autosummary:: Simplifier
    :toctree:

**Functions**

.. autosummary:: cancel_identical_terms
    :toctree:

.. autosummary:: collect
    :toctree:

.. autosummary:: collect_commutative
    :toctree:

.. autosummary:: evaluate_expr
    :toctree:

.. autosummary:: expression_complexity
    :toctree:

.. autosummary:: optimise_statements
    :toctree:

.. autosummary:: reduced_node
    :toctree:


:mod:`permutation_analysis` module
----------------------------------

.. automodule:: brian2.codegen.permutation_analysis
    :show-inheritance:

**Classes**

.. autosummary:: OrderDependenceError
    :toctree:

**Functions**

.. autosummary:: check_for_order_independence
    :toctree:


:mod:`statements` module
------------------------

.. automodule:: brian2.codegen.statements
    :show-inheritance:

**Classes**

.. autosummary:: Statement
    :toctree:


:mod:`targets` module
---------------------

.. automodule:: brian2.codegen.targets
    :show-inheritance:


:mod:`templates` module
-----------------------

.. automodule:: brian2.codegen.templates
    :show-inheritance:

**Classes**

.. autosummary:: CodeObjectTemplate
    :toctree:

.. autosummary:: LazyTemplateLoader
    :toctree:

.. autosummary:: MultiTemplate
    :toctree:

.. autosummary:: Templater
    :toctree:

**Functions**

.. autosummary:: autoindent
    :toctree:

.. autosummary:: autoindent_postfilter
    :toctree:

.. autosummary:: variables_to_array_names
    :toctree:


:mod:`translation` module
-------------------------

.. automodule:: brian2.codegen.translation
    :show-inheritance:

**Classes**

.. autosummary:: LineInfo
    :toctree:

**Functions**

.. autosummary:: analyse_identifiers
    :toctree:

.. autosummary:: get_identifiers_recursively
    :toctree:

.. autosummary:: is_scalar_expression
    :toctree:

.. autosummary:: make_statements
    :toctree:


Subpackages
-----------

.. toctree::
    :maxdepth: 2

    brian2.codegen.generators
    brian2.codegen.runtime


parsing package
===============

:mod:`bast` module
------------------

.. automodule:: brian2.parsing.bast
    :show-inheritance:

**Classes**

.. autosummary:: BrianASTRenderer
    :toctree:

**Functions**

.. autosummary:: brian_ast
    :toctree:

.. autosummary:: brian_dtype_from_dtype
    :toctree:

.. autosummary:: brian_dtype_from_value
    :toctree:

.. autosummary:: is_boolean
    :toctree:

.. autosummary:: is_boolean_dtype
    :toctree:

.. autosummary:: is_float
    :toctree:

.. autosummary:: is_float_dtype
    :toctree:

.. autosummary:: is_integer
    :toctree:

.. autosummary:: is_integer_dtype
    :toctree:


:mod:`dependencies` module
--------------------------

.. automodule:: brian2.parsing.dependencies
    :show-inheritance:

**Functions**

.. autosummary:: abstract_code_dependencies
    :toctree:

.. autosummary:: get_read_write_funcs
    :toctree:


:mod:`expressions` module
-------------------------

.. automodule:: brian2.parsing.expressions
    :show-inheritance:

**Functions**

.. autosummary:: is_boolean_expression
    :toctree:

.. autosummary:: parse_expression_dimensions
    :toctree:


:mod:`functions` module
-----------------------

.. automodule:: brian2.parsing.functions
    :show-inheritance:

**Classes**

.. autosummary:: AbstractCodeFunction
    :toctree:

.. autosummary:: FunctionRewriter
    :toctree:

.. autosummary:: VarRewriter
    :toctree:

**Functions**

.. autosummary:: abstract_code_from_function
    :toctree:

.. autosummary:: extract_abstract_code_functions
    :toctree:

.. autosummary:: substitute_abstract_code_functions
    :toctree:


:mod:`rendering` module
-----------------------

.. automodule:: brian2.parsing.rendering
    :show-inheritance:

**Classes**

.. autosummary:: CPPNodeRenderer
    :toctree:

.. autosummary:: NodeRenderer
    :toctree:

.. autosummary:: NumpyNodeRenderer
    :toctree:

.. autosummary:: SympyNodeRenderer
    :toctree:


:mod:`statements` module
------------------------

.. automodule:: brian2.parsing.statements
    :show-inheritance:

**Functions**

.. autosummary:: parse_statement
    :toctree:


:mod:`sympytools` module
------------------------

.. automodule:: brian2.parsing.sympytools
    :show-inheritance:

**Classes**

.. autosummary:: CustomSympyPrinter
    :toctree:

**Functions**

.. autosummary:: check_expression_for_multiple_stateful_functions
    :toctree:

.. autosummary:: expression_complexity
    :toctree:

.. autosummary:: str_to_sympy
    :toctree:

.. autosummary:: sympy_to_str
    :toctree:

**Objects**

.. autosummary:: PRINTER
    :toctree:



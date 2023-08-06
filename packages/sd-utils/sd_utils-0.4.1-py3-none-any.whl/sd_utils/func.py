from __future__ import print_function

import ast
import types
import numbers
import collections


def create_function(name, signature, callback):  # noqa: C901
    """Dynamically creates a function that wraps a call to *callback*, based
    on the provided *signature*.
    Note that only default arguments with a value of `None` are supported. Any
    other value will raise a `TypeError`.
    """
    # utils to set default values when creating a ast objects
    # Loc = lambda cls, **kw: cls(annotation=None, lineno=1, col_offset=0, **kw)
    def Loc(cls, **kw):
        return cls(annotation=None, lineno=1, col_offset=0, **kw)

    # Name = lambda id, ctx=None: Loc(ast.Name, id=id, ctx=ctx or ast.Load())
    def Name(id, ctx=None):
        return Loc(ast.Name, id=id, ctx=ctx or ast.Load())

    # vars for the callback call
    call_args = []
    call_keywords = []  # PY3
    call_starargs = None  # PY2
    call_kwargs = None  # PY2

    # vars for the generated function signature
    func_args = []
    func_defaults = []
    vararg = None
    kwarg = None

    # vars for the args with default values
    defaults = []

    # assign args based on *signature*
    for param in viewvalues(signature.parameters):
        if param.default is not param.empty:
            if isinstance(param.default, type(None)):
                # `ast.NameConstant` is used in PY3, but both support `ast.Name`
                func_defaults.append(Name("None"))
            elif isinstance(param.default, bool):
                # `ast.NameConstant` is used in PY3, but both support `ast.Name`
                typ = str
                func_defaults.append(Name(typ(param.default)))
            elif isinstance(param.default, numbers.Number):
                func_defaults.append(Loc(ast.Num, n=param.default))
            elif isinstance(param.default, str):
                func_defaults.append(Loc(ast.Str, s=param.default))
            elif isinstance(param.default, bytes):
                typ = ast.Bytes
                func_defaults.append(Loc(typ, s=param.default))
            elif isinstance(param.default, list):
                func_defaults.append(
                    Loc(ast.List, elts=param.default, ctx=ast.Load())
                )
            elif isinstance(param.default, tuple):
                func_defaults.append(
                    Loc(ast.Tuple, elts=list(param.default), ctx=ast.Load())
                )
            elif isinstance(param.default, dict):
                func_defaults.append(
                    Loc(
                        ast.Dict,
                        keys=list(viewkeys(param.default)),
                        values=list(viewvalues(param.default)),
                    )
                )
            else:
                err = "unsupported default argument type: {}"
                raise TypeError(err.format(type(param.default)))
            defaults.append(param.default)
            # func_defaults.append(Name('None'))
            # defaults.append(None)

        if param.kind in {param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD}:
            call_args.append(Name(param.name))
            func_args.append(Loc(ast.arg, arg=param.name))
        elif param.kind == param.VAR_POSITIONAL:
            call_args.append(
                Loc(ast.Starred, value=Name(param.name), ctx=ast.Load())
            )
            vararg = Loc(ast.arg, arg=param.name)
        elif param.kind == param.KEYWORD_ONLY:
            err = "TODO: KEYWORD_ONLY param support, param: {}"
            raise TypeError(err.format(param.name))
        elif param.kind == param.VAR_KEYWORD:
            call_keywords.append(
                Loc(ast.keyword, arg=None, value=Name(param.name))
            )
            kwarg = Loc(ast.arg, arg=param.name)

    # generate the ast for the *callback* call
    call_ast = Loc(
        ast.Call,
        func=Name(callback.__name__),
        args=call_args,
        keywords=call_keywords,
        starargs=call_starargs,
        kwargs=call_kwargs,
    )

    # generate the function ast
    func_ast = Loc(
        ast.FunctionDef,
        name=to_func_name(name),
        args=ast.arguments(
            posonlyargs=func_args,
            args=func_args,
            vararg=vararg,
            defaults=func_defaults,
            kwarg=kwarg,
            kwonlyargs=[],
            kw_defaults=[],
        ),
        body=[Loc(ast.Return, value=call_ast)],
        decorator_list=[],
        returns=None,
    )

    # compile the ast and get the function code
    mod_ast = ast.Module(body=[func_ast], type_ignores=[])
    module_code = compile(mod_ast, "<generated-ast>", "exec")
    func_code = [
        c for c in module_code.co_consts if isinstance(c, types.CodeType)
    ][0]

    # return the generated function
    return types.FunctionType(
        func_code, {callback.__name__: callback}, argdefs=tuple(defaults)
    )


def viewitems(obj):
    return getattr(obj, "viewitems", obj.items)()


def viewkeys(obj):
    return getattr(obj, "viewkeys", obj.keys)()


def viewvalues(obj):
    return getattr(obj, "viewvalues", obj.values)()


def to_func_name(name):
    # func.__name__ must be bytes in Python2
    return to_unicode(name)


def to_bytes(s, encoding="utf8"):
    if isinstance(s, bytes):
        pass
    elif isinstance(s, str):
        s = s.encode(encoding)
    return s


def to_unicode(s, encoding="utf8"):
    if isinstance(s, bytes):
        s = s.decode(encoding)
    elif isinstance(s, str):
        pass
    elif isinstance(s, dict):
        s = {to_unicode(k): to_unicode(v) for k, v in viewitems(s)}
    elif isinstance(s, collections.Iterable):
        s = [to_unicode(x, encoding) for x in s]
    return s

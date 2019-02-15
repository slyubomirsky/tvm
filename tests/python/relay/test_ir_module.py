"""Test the Relay Module data structure."""
import tvm
from tvm import relay

def test_initializing_from_map():
    f1 = relay.GlobalVar("f1")
    f2 = relay.GlobalVar("f2")
    f3 = relay.GlobalVar("f3")

    a = relay.TypeVar("a")
    x = relay.Var("x", a)
    func1 = relay.Function([x], relay.Tuple([x, x]),
                           relay.TupleType([a, a]), [a])

    b = relay.TypeVar("b")
    y = relay.Var("y", b)
    func2 = relay.Function([y], f1(y), relay.TupleType([b, b]), [b])

    c = relay.TypeVar("c")
    d = relay.TypeVar("d")
    z = relay.Var("z", c)
    w = relay.Var("w", d)
    func3 = relay.Function([z, w], relay.Tuple([f1(z), f2(w)]),
                           relay.TupleType([relay.TupleType([c, c]),
                                            relay.TupleType([d, d])]),
                           [c, d])

    mapping = {f1 : func1} # , f2 : func2, f3 : func3}
    mod = relay.Module(mapping)

    expected_types = {f1 : relay.FuncType([a],
                                          relay.TupleType([a, a]),
                                          [a]),
                      f2 : relay.FuncType([a],
                                          relay.TupleType([a, a]),
                                          [a]),
                      f3 : relay.FuncType([a, b],
                                          relay.TupleType([
                                              relay.TupleType([a, a]),
                                              relay.TupleType([b, b])
                                          ]),
                                          [a, b])
    }

    for var in [f1]:
        func = mod.Lookup(var)
        assert func.checked_type == expected_types[var]

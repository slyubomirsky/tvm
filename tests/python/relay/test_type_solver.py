import tvm
from tvm import relay


def make_rel(name, args, num_inputs=None, attrs=None):
    func = tvm.get_env_func("tvm.relay.type_relation." + name)
    if num_inputs is None:
        num_inputs = len(args) - 1
    return relay.ty.TypeRelation(func, args, num_inputs, attrs)

def make_solver():
    solver = relay._ir_pass._test_type_solver()
    solver.Solve = solver("Solve")
    solver.Unify = solver("Unify")
    solver.Resolve = solver("Resolve")
    solver.AddConstraint = solver("AddConstraint")

    def gen_type(name, args, out=None):
        out = out if out else relay.ty.IncompleteType()
        solver.AddConstraint(make_rel(name, args + [out]))
        return out

    solver.gen_type = gen_type
    return solver


def test_bcast():
    solver = make_solver()
    t0 = relay.ty.TensorType((10, 20), "float32")
    t1 = relay.ty.TensorType((10, 1), "float32")
    tc = relay.ty.TensorType((10, 1, 1), "float32")
    t2 = solver.gen_type("Broadcast", [t0, t1])
    t3 = solver.gen_type("Identity", [t2])
    t4 = solver.gen_type("Broadcast", [t3, tc])
    assert solver.Solve()
    assert solver.Resolve(t2) == relay.ty.TensorType((10, 20), "float32")
    assert solver.Resolve(t4) == relay.ty.TensorType((10, 10, 20), "float32")


def test_backward_solving():
    solver = make_solver()
    t0 = relay.ty.TensorType((10, 20), "float32")
    tc = relay.ty.TensorType((10, 1, 1), "float32")
    t1 = relay.ty.IncompleteType()
    t3 = solver.gen_type("Broadcast", [t0, t1])
    t2 = solver.gen_type("Identity", [t1], out=tc)
    assert solver.Solve()
    assert solver.Resolve(t3) == relay.ty.TensorType((10, 10, 20), "float32")


def test_unify_tuple():
    solver = make_solver()
    t1 = relay.ty.IncompleteType()
    t2 = relay.ty.IncompleteType()
    t3 = relay.ty.TensorType((10, 20), "float32")

    tup1 = relay.ty.TupleType([t1, t2])
    tup2 = relay.ty.TupleType([t3, t3])

    unified = solver.Unify(tup1, tup2)
    assert unified == tup2


def test_unify_functype():
    solver = make_solver()
    t1 = relay.ty.IncompleteType()
    t2 = relay.ty.IncompleteType()
    t3 = relay.ty.IncompleteType()

    unit = relay.ty.TupleType([])
    tensor1 = relay.ty.TensorType((10, 20), "float32")
    tensor2 = relay.ty.TensorType((10,), "float32")

    ft1 = relay.ty.FuncType([t1, t2], t3)
    ft2 = relay.ty.FuncType([tensor1, tensor2], unit)

    unified = solver.Unify(ft1, ft2)
    assert unified == ft2


def test_recursive_unify():
    solver = make_solver()
    t1 = relay.ty.IncompleteType()
    t2 = relay.ty.IncompleteType()

    tensor1 = relay.ty.TensorType((10, 10, 20), "float32")
    tensor2 = relay.ty.TensorType((10, 20), "float32")

    tup1 = relay.ty.TupleType([relay.ty.TupleType([t1, t2]), t2])
    tup2 = relay.ty.TupleType([relay.ty.TupleType([tensor1, tensor2]), tensor2])

    ft1 = relay.ty.FuncType([tup1, tensor2], tensor2)
    ft2 = relay.ty.FuncType([tup2, tensor2], tensor2)

    unified = solver.Unify(ft1, ft2)
    assert unified == ft2


def test_recursive_backward_solving():
    solver = make_solver()

    tensor1 = relay.ty.TensorType((10, 20), "float32")
    tensor2 = relay.ty.TensorType((10, 1, 1), "float32")
    tensor3 = relay.ty.TensorType((10,), "float32")

    t1 = relay.ty.IncompleteType()
    t2 = relay.ty.IncompleteType()
    t3 = relay.ty.IncompleteType()

    tup1 = relay.ty.TupleType([relay.ty.TupleType([tensor1, tensor2]), tensor3])
    tup2 = relay.ty.TupleType([relay.ty.TupleType([t1, t2]), t3])
    solver.gen_type("Identity", [tup1], out=tup2)

    assert solver.Solve()
    assert solver.Resolve(tup2) == tup1


if __name__ == "__main__":
    test_bcast()
    test_backward_solving()
    test_unify_tuple()
    test_unify_functype()
    test_recursive_unify()
    test_recursive_backward_solving()

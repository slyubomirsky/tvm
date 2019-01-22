# pylint: disable=no-else-return, unidiomatic-typecheck, invalid-name
"""Algebraic data types in Relay."""
from .base import RelayNode, register_relay_node, NodeBase
from . import _make
from .ty import Type
from .expr import Expr, Call


class Pattern(RelayNode):
    """Base type for pattern matching constructs."""
    pass

@register_relay_node
class PatternWildcard(Pattern):
    """Wildcard pattern in Relay: Matches any ADT and binds nothing."""

    def __init__(self):
        """Constructs a wildcard pattern.

        Parameters
        ----------
        None

        Returns
        -------
        wildcard: PatternWildcard
            a wildcard pattern.
        """
        self.__init_handle_by_constructor__(_make.PatternWildcard)


@register_relay_node
class PatternVar(Pattern):
    """Variable pattern in Relay: Matches anything and binds it to the variable."""

    def __init__(self, var):
        """Construct a variable pattern.

        Parameters
        ----------
        var: tvm.relay.Var

        Returns
        -------
        pv: PatternVar
            A variable pattern.
        """
        self.__init_handle_by_constructor__(_make.PatternVar, var)


@register_relay_node
class PatternConstructor(Pattern):
    """Constructor pattern in Relay: Matches an ADT of the given constructor, binds recursively."""

    def __init__(self, con, pat=None):
        """Construct a constructor pattern.

        Parameters
        ----------
        con: Constructor
            The constructor.
        pat: Optional[List[Pattern]]
            Optional subpatterns: for each field of the constructor,
            match to the given subpattern (treated as a variable pattern by default).

        Returns
        -------
        wildcard: PatternWildcard
            a wildcard pattern.
        """
        if pat is None:
            pat = []
        self.__init_handle_by_constructor__(_make.PatternConstructor, con, pat)


@register_relay_node
class Constructor(Expr):
    """Relay ADT constructor."""

    def __init__(self, name_hint, inp, belong_to):
        """Defines an ADT constructor.

        Parameters
        ----------
        name_hint : str
            Name of constructor (only a hint).
        inp : List[Type]
            Input types.
        belong_to : tvm.relay.GlobalTypeVar
            Denotes which ADT the constructor belongs to.

        Returns
        -------
        con: Constructor
            A constructor.
        """
        self.__init_handle_by_constructor__(_make.Constructor, name_hint, inp, belong_to)

    def __call__(self, *args):
        """Call the constructor.

        Parameters
        ----------
        args: List[relay.Expr]
            The arguments to the constructor.

        Returns
        -------
        call: relay.Call
            A call to the constructor.
        """
        return Call(self, args)


@register_relay_node
class TypeData(Type):
    """Stores the definition for an Algebraic Data Type (ADT) in Relay."""

    def __init__(self, header, tv, constructors):
        """Defines a TypeData object.

        Parameters
        ----------
        header: tvm.relay.GlobalTypeVar
            The name of the ADT.
            ADTs with the same constructors but different names are
            treated as different types.
        tv: List[TypeVar]
            Type variables that appear in constructors.
        constructors: List[tvm.relay.Constructor]
            The constructors for the ADT.

        Returns
        -------
        type_data: TypeData
            The adt declaration.
        """
        self.__init_handle_by_constructor__(_make.TypeData, header, tv, constructors)


@register_relay_node
class Clause(NodeBase):
    """Clause for pattern matching in Relay."""

    def __init__(self, lhs, rhs):
        """Construct a clause.

        Parameters
        ----------
        lhs: tvm.relay.Pattern
            Left-hand side of match clause.
        rhs: tvm.relay.Expr
            Right-hand side of match clause.

        Returns
        -------
        clause: Clause
            The Clause.
        """
        self.__init_handle_by_constructor__(_make.Clause, lhs, rhs)


@register_relay_node
class Match(Expr):
    """Pattern matching expression in Relay."""

    def __init__(self, data, pattern):
        """Construct a Match.

        Parameters
        ----------
        data: tvm.relay.Expr
            The value being deconstructed and matched.
        pattern: [tvm.relay.Clause]
            The pattern match clauses.
        Returns
        -------
        match: tvm.relay.Expr
            The match expression.
        """
        self.__init_handle_by_constructor__(_make.Match, data, pattern)

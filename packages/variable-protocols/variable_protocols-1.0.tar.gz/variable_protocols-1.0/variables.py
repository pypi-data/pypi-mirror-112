from typing import Literal, Protocol, NamedTuple, Tuple, Union, Set


class BaseVariable(Protocol):
    type: Literal['bounded', '1hot', '2vec', 'gaussian']


class Bounded(NamedTuple):
    max: float
    min: float
    type = 'bounded'


class OneHot(NamedTuple):
    n_category: int
    type = '1hot'


class CatVec(NamedTuple):
    n_category: int
    n_embedding: int
    type = '2vec'


class Gaussian(NamedTuple):
    mean: float = 0
    var: float = 1
    type = 'gaussian'


VariableTensor = Tuple[BaseVariable, Tuple[int, ...]]


class VariableGroup(NamedTuple):
    name: str
    variables: Set[Union[VariableTensor, 'VariableGroup']]


def named_variable(name: str, variable: VariableTensor):
    return VariableGroup(name, variables={variable})


def fmt_var_group(g: VariableGroup, indent: int = 0) -> str:
    s = ""
    s += f"{g.name}\n" + (indent * " ") + "{"
    indent += len(s)
    for var in g.variables:
        if isinstance(var, Tuple):
            s += f"{var}, "
        else:
            s += fmt_var_group(var, indent)
    s += "}\n"
    return s

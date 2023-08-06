# float MNIST input
from variables import VariableGroup, VariableTensor, Bounded, OneHot

mnist_in = VariableGroup(name="mnist_in",
                         variables={
                             VariableTensor(Bounded(max=1, min=0), (28, 28))
                         })
mnist_out = VariableGroup(name="mnist_out",
                          variables={
                              VariableTensor(OneHot(n_category=10), (1,))
                          })

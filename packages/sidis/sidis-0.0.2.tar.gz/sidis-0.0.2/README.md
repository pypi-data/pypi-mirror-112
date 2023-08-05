# ***sidis*** : ***si***mple ***d***ata ***i***nterface**s**
> is a Python module that aims to reduce common programming tasks to a single line of code, such as typecasting and data conversion, sorting and mapping, accessing and assigning values through loops, *etc*. The name is a tribute to the early American polymath, William James Sidis. Documentation can be found on the respective pages in the docs website at https://noeloikeau.github.io/sidis/. Here we give a brief overview of some of the main utilities.


## Install

`pip install sidis`

## How to use

```python
import sidis
from sidis import *
```

## Typecasting

Sidis supports extensible typecasting between iterables and non-iterables, letting you do intuitive conversions such as:

```python
cast(0,list)
```




    [0]



```python
cast([0.9,1.1],int)
```




    [0, 1]



or define your own rules:

```python
mycast = Caster()
mycast[list][float] = lambda t: sum(t)
mycast([0.9,1.1],float)
```




    2.0



## Sorting and converting complex datastructures

Sidis lets you sort python objects by the result of maps over those objects, and provides convenient conversion functions.

```python
from sidis import sort, convert
```

Convert the elements of a list to binary arrays, and sort by the length of the array:

```python
sort([0,10,3,5],by=convert,key=lambda t:len(t[-1]))
```




    [(10, [1, 0, 1, 0]), (5, [1, 0, 1]), (3, [1, 1]), (0, [0])]



By default, `convert` converts to a binary array. If we want to change the arguments of the map without yet evaluating it, we can use `pipe`:

```python
from sidis import pipe #like functools.partial, but also allows for typecasting of input and output data
```

Now let's convert to hex:

```python
sort([0.9,10.5,3.1,5.5],by=pipe(convert,to=hex,otype=int)) #convert the elements `otype` into integers, then hex 
```




    [(10.5, '0xa'), (5.5, '0x5'), (3.1, '0x3'), (0.9, '0x0')]



## Arbitrary access to data structures

We can access and change arbitrary datastructures with `get` and `give`:

```python
a=[1]
get(a,0) #get 0th level or attribute of a
```




    1



```python
[give(a,0,a[0]+1) for i in range(10)] #and can assign arbitrary objects without writing entire loops!
a
```




    [11]



and can apply this level of control to more complex datastructures:

```python
import networkx as nx
g=nx.DiGraph() #create a ring with a loop, 0->1->2->0->0
g.add_edges_from([(0,1),(1,2),(2,0)])
g.add_edges_from([(0,0)])
g.in_degree()
```




    InDegreeView({0: 2, 1: 1, 2: 1})



```python
from sidis import get
get(g,'in_degree',0) #get in-degree of node 0
```




    2



and use this to sort with more abstract methods:

```python
sort(g.nodes,by=g.in_degree)
```




    [(0, 2), (1, 1), (2, 1)]



```python
sort(g.nodes,by=g.edges,key=lambda t:len(list(t[-1])))
```




    [(0, OutEdgeDataView([(0, 1), (0, 0)])),
     (1, OutEdgeDataView([(1, 2)])),
     (2, OutEdgeDataView([(2, 0)]))]



or even give attributes to objects:

```python
from sidis import give
give(g,'nodes',0,newattr='for fun')
g.nodes[0]['newattr']
```




    'for fun'



```python
[give(g,'edges',e,weight=np.random.rand(1)) for e in g.edges]
sort(g.edges,'weight')
```




    [array([0.99698538]),
     array([0.90294296]),
     array([0.47634498]),
     array([0.1643804])]



## Arbitrary mapping

sidis also extends mapping using `maps`, which lets you pass in an object and a series of functions and evaluate those functions independently or sequentially over the input to the desired depth:

```python
f1=lambda t:t
f2=lambda t:t+1
f3=lambda t:t+2
maps(0,f1,f2,f3) #apply them individually
```




    [0, 1, 2]



```python
maps(0,f1,f2,f3,depth=-1) #apply them sequentially
```




    3



```python
maps([0,1],f1,f2,f3,depth=1) #apply f1 to 0, then return f2(f1(0)) and f2(f1(0)), then repeat for 1
```




    [[1, 2], [2, 3]]



## ... and more!

```python
from sidis import depth,flatten,unflatten,fill,Template,RNG
```

```python
depth([[0]])
```




    2



```python
depth({'a':0,'b':{'c':1,'d':3}})
```




    2



```python
flatten({'a':0,'b':{'c':1,'d':3}})
```




    {'a': 0, 'b,c': 1, 'b,d': 3}



```python
unflatten({'a': 0, 'b,c': 1, 'b,d': 3})
```




    {'a': 0, 'b': {'c': 1, 'd': 3}}



```python
fill([[1],[2,3]],fillwith=1000,mask=False)
```




    array([[   1, 1000],
           [   2,    3]])



```python
Template('''
fill out your _name
and provide {0} ZIP _iter, lambda t: 'embedded iterable functions!'
''',_name='name and information',_iter=range(1))
```




    fill out your name and information
    and provide embedded iterable functions! 



```python
rng=RNG(0) #globally stable
rng.random(0,1,shape=(2,2))
```




    array([[0.63696169, 0.26978671],
           [0.04097352, 0.01652764]])



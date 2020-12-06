学习笔记

***
is 底层使用的是 id。

**容器**序列有拷贝问题，非容器序列没有这种问题。

***

可变对象实际是**对象**的引用（起始内存地址），不可变的是**值**的引用。

命名元组，比较清晰的读懂。
同样可以通过位置（索引）引用。

运算符重载


类定义 __call__，则实例化可调用。比如：`instance()` 就完成了调用。

命名空间（作用域）

```py
x = 'Global'
def func2():
    x = 'Enclosing'

    def func3():
        x = 'Local'

        print (x)
    func3()
print(x)
func2()
```
直接执行 `func3()` 报错。`NameError: name 'func3' is not defined`.

```py
x = 'Global'
def func4():
    x = 'Enclosing'
    def func5():
        return x
    return func5

var = func4()
print( var() )
```
其中 `func5` 和 `x` 的作用域绑定在一起了。


LEGB 用于解决两个问题：
1. 同名不同作用域
2. 顺序查找问题

***
```
def func(*args, **kargs):
    print(f'args: {args}')
    print(f'kargs:{kargs}')

func(123, 'xz', name='xvalue')  # 传入关键字参数
func(123, 'xz', **{'abc': 123})  
func(123, 'xz', {'abc': 123})
```
结果：
```
args: (123, 'xz')
kargs:{'name': 'xvalue'}
args: (123, 'xz')
kargs:{'abc': 123}
args: (123, 'xz', {'abc': 123})
kargs:{}
```
字典只有使用两个 `**` 解包，才能传入 `**kargs`。
若是使用一个 `*` 解包，只能解包出 key，并将 key 传入 `*args`。
```
>>> func(123, 'xz', *{'abc': 123})
args: (123, 'xz', 'abc')
kargs:{}
```
`**grgs` 首先获取参数，剩下的才给 `*args`。

***
`map` 函数返回一个 map 对象，该对象可以看成迭代器。
使用 `list(map)` 之后，再使用 `list` 取出值，就变成了 `[]`，表明刚才已经迭代取完了。

```
def square(x):
  ...:     return x**2
  ...: 
  ...: m = map(square, range(10))
  ...: 
```
结果：
```
m
Out[6]: <map at 0x14ea24159b0>
next(m)
Out[7]: 0
next(m)
Out[8]: 1
list(m)
Out[9]: [4, 9, 16, 25, 36, 49, 64, 81]
list(m)
Out[10]: []
```
***
`partial` 冻结第一个参数，可以使用后面的形式：`functools.partial(add, 1)`。
冻结其他的参数，必须要使用**关键字**参数，如：`partial(int, base=2)`。

itertools --- 为高效循环而创建迭代器的函数。
functools --- 高阶函数和可调用对象上的操作。
***
return 返回值（基本数据类型），返回函数对象。

对于闭包，外部函数起到了初次定义的功能。这是**定义态**，而非**运行态**。

`nonlocal` 还不止将 L 作用域扩展的 G，还可以扩展到 E。
闭包里面的值，不会轻易释放。？？
闭包：函数和它函数外部相关联的自由变量，组合在一起叫闭包。
***
装饰器本身是一种**设计模式**，用来增强函数功能。在 Python 中被当成基础语法引入进来了。
是**定义态**，而非**运行态**。

装饰器套娃代码，注意外层和内层的语法糖是有**区别**的。
```py
def html(func):
    def decorator():
        return f'<html>{func()}</html>'
    return decorator

def body(func):
    def decorator():
        return f'<body>{func()}</body>'
    return decorator

@html
@body
def content():
    return 'hello world'
```
调用函数结果：
```
content()
Out[4]: '<html><body>hello world</body></html>'
```

装饰器可以分两种：
普通装饰器：
```py
def wrapper(func):
    def inner(*args,**kwargs):
        ret = func(*args,**kwargs)
        return ret
    return inner
```
使用 `@wrapper` 语法糖。

带参数的装饰器：在普通装饰器，外面再封装一层，最外面一层带参数。
```py
from functools import wraps
def outer(形参)
    def wrapper(func):
        @wraps(func)
        def inner(*args,**kwargs):
            ret = func(*args,**kwargs)
            return ret
        return inner
    return wrapper
```
装饰器用法：`@outer(实参)`。

`@wraps(func)`用于修正原函数的签名，名称等。
***
类做为装饰器。
装饰器用于类上面。
***
协议使用**魔术方法**实现。对象协议又叫鸭子类型。
动态类型：初始化没有类型，在运行的过程中改变类型。

自定义的类型，尽量模仿 Python 自带的类型。

`__str__` 给普通人看的，`__repr__` 给程序员看的。两者都在，正常输出调用 `__str__`，对象通信（程序）调用使用 `__repr__`。

强制指定类型对动态语言没有意义，因为会在运行过程中动态改变类型。

***
#### 迭代器
无穷迭代器：
`itertools.count(start=0, step=1)`
`cycle(itertools.cycle(iterable))`
`itertools.repeat(object[, times])`

迭代完所有可迭代对象的元素：`itertools.chain(*iterables)`，比如：
```
>>> chain('ABC', 'DEF')
A B C D E F
```

使用 `yeild from` 还可以继续迭代之后的对象：
比如实现 `chain` 可以使用：
```py
def chain(*iterables):
    for it in iterables:
        for element in it:
            yield element
```
使用 `yield from` 写更为方便：
```py
def chain(*iterables):
    for i in iterables:
        yield from i 
```

迭代器有两个注意点：
* 对原有字典进行插入操作后，字典迭代器会立即失效（即不能进行下面的操作了）。
`RuntimeError: dictionary changed size during iteration`。
* 尾插入操作不会损坏指向当前元素的List迭代器,列表会自动变长

***
#### 协程
协程也是提高 IO 密集型的工作效率。
Python 3.5 中 `await` 取代了 `yield from`。
使用使有两点需要注意：
1. 必须要放在函数中。
2. 必须使用 `async` 关键字修饰函数。
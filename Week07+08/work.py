from abc import ABCMeta, abstractmethod


# 单例
class Zoo:
    def __init__(self, name):
        self.name = name

    def add_animal(self, obj):
        species = type(obj).__name__
        if not hasattr(self, species):
            setattr(self, species, [])
        if id(obj) not in getattr(self, species):
            getattr(self, species).append(id(obj))
        else:
            raise Exception('不允许添加同一实例！')
        # 下面结果：'species': 'Cat'
        # self.species = species


# 不允许被实例化，所以只有类属性
# 因为要继承，不能使用 new 直接抛出异常
class Animal(metaclass=ABCMeta):

    species = None
    body_type = None
    character = None
    is_fierce = None

    @abstractmethod
    def pre_process(self, species, body_type, character):
        return body_type[0] in ['中', '大'] and species == '食肉' and character == '凶猛'


class Cat(Animal):

    sound = '喵'

    def pre_process(self, species, body_type, character):
        return super().pre_process(species, body_type, character)

    def __init__(self, name, species, body_type, character):
        self.is_pet = not self.pre_process(species, body_type, character)
        self.name = name


class Dog(Animal):

    sound = '汪'

    def pre_process(self, species, body_type, character):
        return super().pre_process(species, body_type, character)

    def __init__(self, name, species, body_type, character):
        self.is_pet = not self.pre_process(species, body_type, character)
        self.name = name


if __name__ == '__main__':
    # 1.
    # a = Animal()

    # 2.
    print(Animal.__dict__)

    # 3.
    print(Cat.sound)

    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    print(cat1.__dict__)

    dog = Dog('狼狗 1', '食肉', '大', '凶猛')
    print(dog.__dict__)

    # 4.
    z = Zoo('时间动物园')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    print(have_cat)

    cat2 = Cat('大花猫 2', '食肉', '中等', '温顺')
    z.add_animal(cat2)
    print(z.__dict__)

    z.add_animal(dog)
    print(z.__dict__)

    # 抛出自定义异常
    # z.add_animal(cat2)

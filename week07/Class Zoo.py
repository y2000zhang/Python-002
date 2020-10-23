from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, kind, size, temper):
        self.kind = kind
        self.size = size
        self.temper = temper

    def fierce(self):
        if self.kind == "食肉" and (self.size == "中等" or self.size == "大型") and self.temper == "凶猛":
            return False
        else:
            return True


def is_pet(self):
    if self.fierce():
        return "适合做宠物"
    else:
        return "不适合做宠物"


class Cat(Animal):
    sound = "喵"

    def __init__(self, name, kind, size, temper):
        self.name = name
        super().__init__(kind, size, temper)

    def is_pet(self):
        return is_pet(self)


class Dog(Animal):
    sound = "汪"

    def __init__(self, name, kind, size, temper):
        self.name = name
        super().__init__(kind, size, temper)

    def is_pet(self):
        return is_pet(self)


class Zoo(object):
    def __init__(self, name):
        self.name = name
        self.animals_list = []

    def add_animal(self, animal):
        if animal not in self.animals_list:
            setattr(self, animal.__class__.__name__, True)
            self.animals_list.append(animal)
        else:
            raise Exception("同一只动物不能被重复添加")


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小型', '温顺')
    dog1 = Dog('柴犬', '食肉', '中型', '温顺')
    dog2 = Dog('藏獒', '食肉', '大型', '凶猛')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    z.add_animal(dog1)
    z.add_animal(dog2)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    have_dog = hasattr(z, 'Dog')
    print("have-cat:", have_cat)
    print("pet-cat:", "%s" % cat1.name, cat1.is_pet())
    print("have-dog:", have_dog)
    print("pet-dog:", "%s" % dog1.name, dog1.is_pet())
    print("pet-dog:", "%s" % dog2.name, dog2.is_pet())
    z.add_animal(dog1)

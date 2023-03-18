import os

class MyAttributeClass(object):
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def __len__(self) -> int:
        return len(self.__dict__)

if __name__ == '__main__':
    MyAttributeClass
    fptr = open('test.txt', 'w')
    n = int(input())
    my_dict = {}
    keys = []
    for i in range(n):
        k, v = input().split(' ')
        keys.append(k)
        my_dict[k] = v
    class_object = MyAttributeClass(**my_dict)
    dir(class_object)
    for k, v in my_dict.items():
        assert my_dict[k] == class_object.__getattribute__(k)
    for i in keys:
        fptr.write(f"{i}: {class_object.__getattribute__(i)}\n")
    fptr.write(f"Count of attributes: {len(class_object)}\n")
    fptr.close()
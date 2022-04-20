my_list = []

price_list = [100, 200, 300]


class Fruit:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "Fruit ({0}, {1})".format(self.name, self.price)


for item in price_list:
    #print(4*item)
    my_fruit = {"price": 4*item, "name": "Pinapple"}
    my_list.append(my_fruit)

print(my_list)




while True:

    x = input()
    x = int(x)
    if x % 5 == 0:
        print(5)
    elif x % 3 == 0:
        print(3)
    elif x % 11 == 0:
        print(11)
    else:
        print("LOX")










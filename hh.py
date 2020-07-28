from product import product
from stock import stock
s = stock()
p1 = product('apple',100,2,1000001)
s.add(p1)
s.List_all()

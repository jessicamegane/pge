
import random
f = open("folds.txt","w")
for i in range(70):
    ll = random.sample(range(1, 507), 50)
    ll.sort()
    for value in ll:
        f.write(str(value) + " ")
    f.write('\n')
 

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from DbClass import DbClass
db= DbClass()
food_eaten= db.getFood_eaten()
print(food_eaten)
plot_list = []
for result in food_eaten:
    if result[1] =='kg':
        plot_list.append((int(float(result[0])*1000)))
    else: plot_list.append(int(result[0]))

print(plot_list)
lijst =[1,2,3,4]
plt.plot(lijst)

plt.show()

plt.savefig("/home/pi/Pictures/g.svg" )
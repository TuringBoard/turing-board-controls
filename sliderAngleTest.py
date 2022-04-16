# Sahaj Amatya
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
 
plt.subplots_adjust(bottom=0.35)

axis = plt.axes([0.20, 0.4, 0.65, 0.13])
 
angle = Slider(axis, 'Angle', 0, 90, 45)
  
def update(val):
    a = int(angle.val)
    print(a)

angle.on_changed(update)
 
plt.show()
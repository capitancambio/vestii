import Tkinter as tk
import VestiiInterface


class State(object):

    def __init__(self, vestii):
        self.currents = [0., 0.]
        self.polarities = [0., 0.]
        self.vestii = vestii

    def update_current_1(self, event):
        self.currents[0] = int(event)
        print "Updated currents", self.currents
        self.update_vestii()

    def update_current_2(self, event):
        self.currents[1] = int(event)
        print "Updated currents", self.currents
        self.update_vestii()

    def update_polarity_1(self, ):
        self.polarities[0] = (self.polarities[0] + 1) % 2
        print "Updated polarities", self.polarities
        self.update_vestii()

    def update_polarity_2(self):
        self.polarities[1] = (self.polarities[1] + 1) % 2
        print "Updated polarities", self.polarities
        self.update_vestii()

    def update_vestii(self):
        self.vestii.UpdateVestii(self.polarities, self.currents)

state = State(Vestii())
root = tk.Tk()

root.geometry("%dx%d" % (200, 200))
current_1 = tk.Scale(root, from_=0, to=255, command=state.update_current_1)
current_1.grid(row=0, column=0)
polarity_1 = tk.Checkbutton(root, text="Polarity 1",
                            command=state.update_polarity_1)
polarity_1.grid(row=1, column=0)

current_2 = tk.Scale(root, from_=0, to=255, command=state.update_current_2)
current_2.grid(row=0, column=1)
polarity_2 = tk.Checkbutton(root, text="Polarity 2",
                            command=state.update_polarity_2)
polarity_2.grid(row=1, column=1)

root.mainloop()

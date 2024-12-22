class Action:
    def __init__(self, car):
        self.car = car

    def drift(self):
        self.car.drift()
        
    def rotate_left(self):
        self.car.rotate(left=True)

    def rotate_right(self):
        self.car.rotate(right=True)

    def move_forward(self):
        self.car.move_forward()

    def move_backward(self):
        self.car.move_backward()

    def reduce_speed(self):
        self.car.reduce_speed()

    def reset(self):
        self.car.reset()



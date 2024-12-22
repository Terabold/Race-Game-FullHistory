class State:
    def __init__(self, car):
        self.car = car
        self.game_finished = False
        self.winner = None
        self.elapsed_time = 0
        self.waiting_for_restart = False  # New flag for restart state
    
    def update(self, elapsed_time):
        self.elapsed_time = elapsed_time

    def set_winner(self, elapsed_time):
        self.game_finished = True
        self.waiting_for_restart = True  # Set waiting state when lap is complete
        self.winner = f"Time: {elapsed_time:.2f} sec"
        
    def reset(self):
        self.game_finished = False
        self.waiting_for_restart = False
        self.winner = None
        self.elapsed_time = 0
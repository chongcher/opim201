class Winnower:

    max_input = 250
    cycle_time = 60
    output_ratio = 185.0/250

    def __init__(self):
        self.elapsed_time = 0
        self.current_input = 0

    def step(self):
        if self.current_input == 0:
            return 0
        elif self.elapsed_time + 1 == self.cycle_time:
            temp = self.current_input
            self.current_input = 0
            return temp * self.output_ratio
        else:
            self.elapsed_time += 1
            return -1

    def start_cycle(self, new_input):
        if self.current_input != 0:
            raise Exception('Cycle started while input is not 0')
        elif new_input <= 0:
            raise Exception('Cannot start cycle with no input!')
        else:
            self.current_input = new_input
            self.elapsed_time = 1

class ConcheAsIs:

    max_input = 1400
    cycle_time = 3000
    output_ratio = 1400.0/1400

    def __init__(self, max_input):
        self.elapsed_time = 0
        self.current_input = 0
        self.max_input = max_input

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

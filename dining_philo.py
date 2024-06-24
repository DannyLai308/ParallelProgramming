import sys
import random
import threading
import time

class fork:
    def __init__(self):
        self.is_Used = False

    def take_fork(self):
        if not self.is_Used:
            self.is_Used = True
            return True
        return False
        
    def put_fork_down(self):
        self.is_Used = False


class philosophers(threading.Thread):
    def __init__(self, philo_id, left_fork, right_fork):
        super().__init__()
        self.philo_id = philo_id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.random = random.Random()
        self.is_deadlock = False  
       

    # Main function to simulate the dining philosophers problem. Contains the main loop
    # where philosophers keeps altering between thinking and eating
    def simulate(self):
        while not self.is_deadlock:
            self.philo_think() # Starts the simulation with the philosopher thinking

            if self.left_fork.take_fork():
                # Taking left fork for a random length of time
                take_left_fork = self.random.randint(1, 100)
                time.sleep(take_left_fork/1000)
                print(f"Philosopher # {self.philo_id} taking left fork")

                # Taking right fork for a random length of time
                if self.right_fork.take_fork():
                    print(f"Philosopher # {self.philo_id} taking right fork")
                    take_right_fork = self.random.randint(1, 100)
                    time.sleep(take_right_fork/1000)
                    self.philo_eat()

                    # Putting down one fork at a time after eating, at a random length of time
                    putDown_left_fork = self.random.randint(1, 100)
                    time.sleep(putDown_left_fork/1000)
                    self.left_fork.put_fork_down()
                    print(f"Philosopher # {self.philo_id} putting down left fork")

                    putDown_right_fork = self.random.randint(1, 100)
                    time.sleep(putDown_right_fork/1000)
                    self.right_fork.put_fork_down()
                    print(f"Philosopher # {self.philo_id} putting down right fork")
                
                # If philosopher cannot take either left or right fork, it is a deadlock
                else:
                    print(f"Philosopher # {self.philo_id} couldn't take right fork")
                    self.is_deadlock = True
            else:
                print(f"Philosopher # {self.philo_id} couldn't take left fork")
                self.is_deadlock = True
            # Detect deadlock when the philosopher cannot eat due to not having both forks
            if  self.is_deadlock:
                print(f"Philosopher # {self.philo_id} reached deadlock")
    
    def philo_think(self):
        # The philosopher thinks for a random length of time
        think_time = self.random.randint(1, 100)
        print(f"Philosopher # {self.philo_id} is thinking for {think_time}ms")
        time.sleep(think_time/1000)

    def philo_eat(self):
        # The philosopher eats for a random length of time
        eat_time = self.random.randint(1, 100)
        print(f"Philosopher # {self.philo_id} is eating for {eat_time}ms")
        time.sleep(eat_time/1000)

    


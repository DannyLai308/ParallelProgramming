import sys
import random
import threading
import time

class Fork:
    def __init__(self):
        self.is_Used = False

    def take_fork(self):
        if not self.is_Used:
            self.is_Used = True
            return True
        return False
        
    def put_fork_down(self):
        self.is_Used = False


class Philosopher(threading.Thread):
    def __init__(self, philo_id, left_fork, right_fork):
        super().__init__()
        self.philo_id = philo_id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.random = random.Random()
        self.is_deadlock = False  
        self.has_eaten = False
        self.meals = 0
       

    # Main function to simulate the dining philosophers problem. Contains the main loop
    # where philosophers keeps altering between thinking and eating
    def run(self):
        while not self.is_deadlock:
            self.philo_think() # Starts the simulation with the philosopher thinking

            print(f"Philosopher # {self.philo_id} wants to eat")
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
                    self.meals += 1

                    # Putting down one fork at a time after eating, at a random length of time
                    putDown_left_fork = self.random.randint(1, 100)
                    time.sleep(putDown_left_fork/1000)
                    self.left_fork.put_fork_down()
                    print(f"Philosopher # {self.philo_id} putting down left fork")

                    putDown_right_fork = self.random.randint(1, 100)
                    time.sleep(putDown_right_fork/1000)
                    self.right_fork.put_fork_down()
                    print(f"Philosopher # {self.philo_id} putting down right fork")
                
                else:
                    print(f"Philosopher # {self.philo_id} couldn't take right fork")
                    self.has_eaten = False
                    # Put down left fork after failing to take right fork
                    self.left_fork.put_fork_down()
                    print(f"Philosopher # {self.philo_id} putting down left fork ")
                    
            else:
                self.has_eaten = False
                print(f"Philosopher # {self.philo_id} couldn't take left fork")

            # Detect deadlock 
            if  not self.is_deadlock and not self.left_fork.is_Used and not self.right_fork.is_Used and not self.has_eaten:
                self.is_deadlock = True
                print(f"Philosopher # {self.philo_id} reached deadlock")

    
    def philo_think(self):
        # The philosopher thinks for a random length of time
        think_time = self.random.randint(1, 100)
        print(f"Philosopher # {self.philo_id} is thinking for {think_time}ms")
        time.sleep(think_time/1000)

    def philo_eat(self):
        # The philosopher eats for a random length of time
        self.has_eaten = True
        eat_time = self.random.randint(1, 100)
        print(f"Philosopher # {self.philo_id} is eating for {eat_time}ms")
        time.sleep(eat_time/1000)

    
def dining_simulation(number_Of_philo):
    forks = [Fork() for _ in range(number_Of_philo)]
    philosophers = [Philosopher(index + 1, forks[index], forks[(index + 1) % number_Of_philo]) for index in range(number_Of_philo)]

    # Starts all threads for philosophers and waits for them to finish
    for philo in philosophers:
        philo.start()
    for philo in philosophers:
        philo.join()

    print("Deadlock occured for all philosophers")

    print("# of philosophers    | Percentage of meals               | Total number of meals before deadlock")
    total_meals = 0
    for philo in philosophers:
        total_meals += philo.meals
    print()
    print(f"{number_Of_philo}                   | ", end=(" "))
    for philo in philosophers:    
        meals_percentage = (philo.meals / total_meals) * 100 if total_meals > 0 else 0
        print(f"{meals_percentage:.1f}", end=", ")
    print(f"                        | {total_meals}")

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Error: Please specify the number of philosophers (at least 2)")
    #     exit(1)

    number_Of_philo = 3
    dining_simulation(number_Of_philo)
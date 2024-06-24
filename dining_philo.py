import threading
import random
import time
import sys

class Philosopher(threading.Thread):
  def __init__(self, philo_id, forks, terminate_event):
    super().__init__()
    self.philo_id = philo_id + 1 
    self.left_fork = forks[philo_id]
    self.right_fork = forks[(philo_id + 1) % len(forks)]
    self.terminate_event = terminate_event
    self.random = random.Random()
    self.meals = 0



  def run(self):
    while not self.terminate_event.is_set():
      # Thinking process
      self.philo_think()

      # Transitioning to taking forks to eat
      print(f"Philosopher # {self.philo_id} wants to eat")
   
      # Picking up left fork
      if not self.left_fork.acquire(timeout=0.6):  # Acquire left fork with timeout to wait for potential release of fork from neighbor philosopher
        print(f"Philosopher # {self.philo_id} couldn't pick up left fork, get back to thinking")
        continue  # Skip if can't get left fork within timeout

      time.sleep(random.randint(1, 100)/1000) # Random length of time to pick up left fork
      print(f"Philosopher # {self.philo_id} picked up left fork")

      if not self.right_fork.acquire(timeout=0.6):  # Acquire right fork with timeout to wait for potential release of fork from neighbor philosopher
        print(f"Philosopher # {self.philo_id} couldn't pick up right fork within timeout")
        #self.left_fork.release()  # Put down left fork if right fork is not available
        break  # Break out of loop if can't get right fork within timeout, since it means the neighbor philosopher is holding to the right fork

      time.sleep(random.randint(1, 100)/1000) # Random length of time to pick up right fork
      print(f"Philosopher # {self.philo_id} picked up right fork")

      # Eating process
      self.philo_eat()
      self.meals += 1

      # Putting down both forks after eating
      self.left_fork.release()
      time.sleep(random.randint(1, 100)/1000) # Random length of time to put down left fork
      print(f"Philosopher # {self.philo_id} put down left fork")

      self.right_fork.release()
      time.sleep(random.randint(1, 100)/1000) # Random length of time to put down right fork
      print(f"Philosopher # {self.philo_id} put down right fork")

    # Detect potential deadlock for current philosopher
    print(f"Philosopher # {self.philo_id} potentially reached deadlock.")

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
    

def dining_simulation(number_Of_philo):
  forks = [threading.Semaphore(1) for _ in range(number_Of_philo)]
  terminate_event = threading.Event()
  philosophers = [Philosopher(i, forks.copy(), terminate_event) for i in range(number_Of_philo)]

  # Start all philosopher threads
  for philo in philosophers:
    philo.start()
  for philo in philosophers:
    philo.join()

  print("Deadlock found! All philosophers potentially reached dead lock.")
  print("\n")
  print("# of philosophers    | Percentage of meals               | Total number of meals before deadlock")
  total_meals = 0
  for philo in philosophers:
    total_meals += philo.meals

  print(f"{number_Of_philo}                    | ", end=(" "))
  for philo in philosophers:    
    meals_percentage = (philo.meals / total_meals) * 100 if total_meals > 0 else 0
    print(f"{meals_percentage:.1f}", end=", ")
  print(f"                       | {total_meals}")

  terminate_event.set()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please specify the number of philosophers (at least 2)")
        exit(1)
    number_Of_philo = int(sys.argv[1])
    dining_simulation(number_Of_philo)

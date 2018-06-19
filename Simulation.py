import itertools
import random

import simpy

RANDOM_SEED = 42
TRUCK_TIME = 300
CAR_TIME = 150
TOLLBOOTH_SIZE = 10
T_INTER = [3, 30]        # Create a car every [min, max] seconds
SIM_TIME = 10000           # Simulation time in seconds

def car(name, env, tollbooth):
    """A car arrives at the tollbooth.

    It waits to be serviced. If all the booths are busy,
    it waits for the tollbooth to get empty.

    """
    # print('%s arriving at tollbooth at %.1f' % (name, env.now))
    with tollbooth.request() as req:
        start = env.now
        # Request one of the tollbooths
        yield req

        # The process takes some time
        yield env.timeout(CAR_TIME)

        print('%s finished service in %.1f seconds.' % (name,
                                                          env.now - start))
                                                        
def truck(name, env, tollbooth):
    """A truck arrives at the tollbooth.

    Same as car.

    """
    # print('%s arriving at tollbooth at %.1f' % (name, env.now))
    with tollbooth.request() as req:
        start = env.now
        # Request one of the tollbooths
        yield req

        # The process takes some time
        yield env.timeout(TRUCK_TIME)

        print('%s finished service in %.1f seconds.' % (name,
                                                          env.now - start))

def vehicle_generator(env, tollbooth):
    """Generate new vehicles that arrive at the tollbooth."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        c = car('Car %d' % i, env, tollbooth)
        t = truck('Truck %d' % i, env, tollbooth)        
        env.process(random.choice([c, t]))


# Setup and start the simulation
print('Tollbooth Servicing')
random.seed(RANDOM_SEED)

# Create environment and start process
env = simpy.Environment()
tollbooth = simpy.Resource(env, TOLLBOOTH_SIZE)
env.process(vehicle_generator(env, tollbooth))

# Execute!  
env.run(until=SIM_TIME)
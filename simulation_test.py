import random, sys

random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
from simulation import Simulation

if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Bed Rot"
    repro_num = 0.60
    mortality_rate = 0.20
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    initially_vaccinated = int(pop_size * 0.05)
    initially_infected = 5

    sim = Simulation(virus, pop_size, initially_vaccinated, initially_infected)

    sim.run()

    assert sim.virus == virus
    assert sim.pop_size == 1000
    assert sim.initially_infected == 5
    assert sim.initially_vaccinated == 50
    assert sum(sim.total_deaths) == 170
    assert sum(sim.total_vaccinations) == 830

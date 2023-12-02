import random, sys

# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.logger = Logger("output.txt")
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.population = self._create_population()

    def _create_population(self):
        # Create a list of people (Person instances), total number of people equal to the pop_size.
        # The number of infected people should be equal to the the initial_infected
        # Returns list of people
        population = []
        for i in range(0, self.pop_size):
            person = Person(i, False, virus)
            if i < self.initial_infected:  # infect x number of people
                person.infection = virus
            population.append(person)
        return population

    def _simulation_should_continue(self):
        # This method will return a boolean indicating if the simulation
        # should continue.
        # The simulation should not continue if all of the people are dead,
        # or if all of the living people have been vaccinated.
        death_count = 0
        vaccination_count = 0
        for person in self.population:
            if not person.is_alive:
                death_count += 1
            elif person.is_alive and person.is_vaccinated:
                vaccination_count += 1

        if death_count == self.pop_size or vaccination_count == self.pop_size:
            return False
        else:
            return True

    def run(self):
        # This method starts the simulation. It should track the number of
        # steps the simulation has run and check if the simulation should
        # continue at the end of each step.

        time_step_counter = 0
        should_continue = True

        self.logger.write_metadata(
            pop_size=self.pop_size,
            vacc_percentage=self.vacc_percentage,
            virus_name=self.virus.name,
            mortality_rate=self.virus.mortality_rate,
            basic_repro_num=self.virus.repro_rate,
        )

        while should_continue:
            time_step_counter += 1
            self.time_step()
            should_continue = self._simulation_should_continue()

        # TODO: When the simulation completes you should conclude this with
        # the logger. Send the final data to the logger.

    def time_step(self):
        # This method will simulate interactions between people, calulate
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other
        # people in the population
        for person in self.population:
            if person.infection:
                for i in range(0, 100):
                    self.interaction(person, random.choice(self.population))

    def interaction(self, infected_person, random_person):
        if random_person.is_vaccinated:
            pass
        elif random_person.infection != None:
            pass
        elif random_person.infection == None and not random_person.is_vaccinated:
            random_number = random.random()
            if random_number < self.virus.repro_rate:
                random_person.infection = self.virus
            else:
                pass
        # The possible cases you'll need to cover are listed below:
        # random_person is vaccinated:
        #     nothing happens to random person.
        # random_person is already infected:
        #     nothing happens to random person.
        # random_person is healthy, but unvaccinated:
        #     generate a random number between 0.0 and 1.0.  If that number is smaller
        #     than repro_rate, add that person to the newly infected array
        #     Simulation object's newly_infected array, so that their infected
        #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.

    # I actually dont really think this method is needed, I can just infect in the function above
    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        pass


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the imulation
    # virus = Virus(virus, pop_size, vacc_percentage, initial_infected)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()

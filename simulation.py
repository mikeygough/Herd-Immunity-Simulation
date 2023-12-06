import random, sys

random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, initially_vaccinated, initially_infected=1):
        self.logger = Logger("output.txt")
        self.virus = virus
        self.pop_size = pop_size
        self.initially_vaccinated = initially_vaccinated
        self.initially_infected = initially_infected
        self.population = self._create_population()
        self.step_counter = 0
        self.interaction_counter = 0
        self.newly_infected = set() # using a set for efficiency
        self.new_deaths = 0
        self.new_vaccinations = 0
        self.total_deaths = []
        self.total_vaccinations = [initially_vaccinated + initially_infected] # include starting vaccinations
        self.saved_by_vaccination = 0
    
    def _create_population(self):
        ''' create a list of people (Person instances) of length self.pop_size
        set number of infected people and number of vaccinated people equal to
        self.initially_infected and self.initially_vaccinated.
        return list of people. '''

        population = [] # -> local just for creation of population

        # generate people
        for i in range(0, self.pop_size):
            # id, NOT vaccinated, NOT infected, ALIVE
            person = Person(i, False)
            population.append(person)

        # randomly infect self.initially_infected people... once infected they are automatically vaccinated
        # note that these people will never die
        newly_infected = 0 # -> local just for creation of population
        while newly_infected < self.initially_infected:
            random_person = random.choice(population)
            # if not infected
            if not random_person.infection:
                # infect
                random_person.infection = self.virus
                # vaccinate
                random_person.is_vaccinated = True
                newly_infected += 1
    
        # randomly vaccinate self.initially_vaccinated people...
        newly_vaccinated = 0 # -> local just for creation of population
        while newly_vaccinated < self.initially_vaccinated:
            random_person = random.choice(population)
            # if not vaccinated
            if not random_person.is_vaccinated:
                # vaccinate
                random_person.is_vaccinated = True
                newly_vaccinated += 1

        # return population
        return population

    def _simulation_should_continue(self):
        ''' check if the simulation is complete. returns either true or false.
            simulation is deemed complete when the sum of deaths and living-vaccinated is equal to the population size. '''

        # simulation complete, people either survived or perished from virus
        if sum(self.total_deaths) + sum(self.total_vaccinations) == self.pop_size:
            return False
        else:
            return True

    def run(self):
        ''' start the simulation. keeps track of information and logs when necessary '''

        should_continue = True

        # initial data log
        self.logger.write_metadata(
            self.pop_size,
            self.virus.name,
            self.initially_infected,
            self.initially_vaccinated,
        )

        while should_continue:
            self.step_counter += 1
            self.time_step()
            should_continue = self._simulation_should_continue()

        # final data log
        self.logger.log_infection_survival(
            self.pop_size,
            self.initially_infected,
            self.initially_vaccinated,
            sum(self.total_deaths),
            sum(self.total_vaccinations),
            self.saved_by_vaccination
        )
        
    def time_step(self):
        ''' simulate interactions between people, then call interaction
        to determine vaccinations and infections. '''
        
        # people in the population
        number_of_interactions = 100
        living_people = [person for person in self.population if person.is_alive]
        living_infected_people = [person for person in living_people if person.infection]

        # run interactions...
        for person in living_infected_people:
            # perform number_of_interactions interactions
            completed_interactions = 0
            while completed_interactions < number_of_interactions:
                # get random living person
                random_person = random.choice(living_people)
                # interact
                self.interaction_counter += 1  # class -> keeps track of simulation interactions
                self.interaction(random_person)
                # update completed interactions
                completed_interactions += 1  # local -> ensures 100 number_of_interactions interactions per infected person
        
        # infect -> vaccinate / perish
        self._infect_newly_infected()
        
        self.logger.log_step(
            self.step_counter,
            self.new_deaths,
            self.new_vaccinations,
            sum(self.total_deaths),
            sum(self.total_vaccinations)
        )
        
        # reset new_deaths & new_vaccinations
        self.new_deaths = 0
        self.new_vaccinations = 0

    def interaction(self, random_person):
        ''' if random_person not infected and not vaccinates,
            determine if they should be infected. add to newly_infected set if not
            currently there. log interaction data. '''

        # set new_infection to False (for logging)
        new_infection = False
        
        # if already vaccinated
        if random_person.is_vaccinated:
            self.saved_by_vaccination += 1
        
        # if not infected and not vaccinated
        if not random_person.infection and not random_person.is_vaccinated:
            # determine if going to be infected
            random_number = random.random()
            if random_number < self.virus.repro_rate:
                # add to set
                self.newly_infected.add(random_person)
                # update new_infection (for logging)
                new_infection = True
                
        # log -- consumes a lot of resources
        # self.logger.log_interactions(
        #     self.step_counter,
        #     self.interaction_counter,
        #     new_infection,
        #     len(self.newly_infected)
        # )

    def _infect_newly_infected(self):
        ''' loop through population, update person's infection
            attribute if they were infected in the most recent time step.
            determine if they die from infection, update new_vaccinations and new_deaths count.
            reset newly_infected list. '''
        
        living_people = [person for person in self.population if person.is_alive]
        
        # add infections
        for person in living_people:
            if person in self.newly_infected:
                person.infection = self.virus
                # determine new deaths & vaccinations
                if person.did_survive_infection():
                    self.new_vaccinations += 1
                else:
                    self.new_deaths += 1

        # store per round vaccinations and deaths
        self.total_vaccinations.append(self.new_vaccinations)
        self.total_deaths.append(self.new_deaths)
        
        # reset newly_infected
        self.newly_infected = set()


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Bed Rot"
    repro_num = 0.60
    mortality_rate = 0.20
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 100000
    initially_vaccinated = int(pop_size * 0.05)
    initially_infected = 10

    sim = Simulation(virus, pop_size, initially_vaccinated, initially_infected)

    sim.run()

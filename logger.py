class Logger(object):
    def __init__(self, file_name):
        # The file_name passed should be the full file name of the file that the logs will be written to.
        self.file_name = file_name

    def write_metadata(
        self, pop_size, virus_name, initially_infected, initially_vaccinated
    ):
        formatted_string = f""" ===============
Population Size: {pop_size}
Virus Name: {virus_name}
Initially Infected: {initially_infected}
Initially Vaccinated: {initially_vaccinated}
 ===============
"""
        with open(self.file_name, "w") as f:
            f.write(formatted_string)

    def log_interactions(
        self,
        step_counter,
        interaction_counter,
        new_infection,
        newly_infected
    ):
        formatted_string = f"""
Step Counter: {step_counter}
Interaction Counter: {interaction_counter}
New Infection? {new_infection}
Newly Infected During this Round: {newly_infected}
 ===============
"""
        with open(self.file_name, "a") as f:
            f.write(formatted_string)    
    
    def log_infection_survival(
        self, pop_size, initially_infected, initially_vaccinated, total_deaths, total_vaccinations
    ):
        formatted_string = f"""
Population Size: {pop_size}
Initially Infected: {initially_infected}
Initially Vaccinated: {initially_vaccinated}
Total Simulation Deaths: {total_deaths}
Total Simulation Vaccinations: {total_vaccinations}
 ===============
"""
        with open(self.file_name, "a") as f:
            f.write(formatted_string)
            
        print(formatted_string)

    def log_step(self, step_counter, new_deaths, new_vaccinations, total_deaths, total_vaccinations):
        formatted_string = f"""
Step Counter: {step_counter}
New Deaths: {new_deaths}
New Vaccinations: {new_vaccinations}
Total Simulation Deaths: {total_deaths}
Total Simulation Vaccinations (Starting + New): {total_vaccinations}
 ===============
"""
        with open(self.file_name, "a") as f:
            f.write(formatted_string)
            
        print(formatted_string)

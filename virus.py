class Virus(object):
    # Properties and attributes of the virus used in Simulation.
    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


# Test this class
if __name__ == "__main__":
    # Test your virus class by making an instance and confirming
    # it has the attributes you defined
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3
    
    virus = Virus("Bed Rot", 0.60, 0.20)
    assert virus.name == "Bed Rot"
    assert virus.repro_rate == 0.60
    assert virus.mortality_rate == 0.20
    
    virus = Virus("Can't Swim Disease", 0.01, 0.01)
    assert virus.name == "Can't Swim Disease"
    assert virus.repro_rate == 0.01
    assert virus.mortality_rate == 0.01

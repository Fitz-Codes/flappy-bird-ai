import config
import player
import math
import species
import operator

class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
        self.size = size
        for i in range(0, self.size):
            self.players.append(player.Player())

    def update_live_players(self):
        for p in self.players:
            if p.alive:
                p.look()
                p.think()
                p.draw(config.window)
                p.update(config.ground)
    
    #Calls the functions that correlate to each step of the natural selection process
    def natural_selection(self):
        self.speciate()

        print("Calculate Fitness")
        self.calculate_fitness()

        print("Kill Extinct")
        self.kill_extinct_species()

        print("Sort by fitness")
        self.sort_species_by_fitness()

        print("Kill Stale")
        self.kill_stale_species()

        print("Children for next gen")
        self.next_gen()

    def speciate(self):
        for s in self.species:
            s.players = []
        
        for p in self.players:
            add_to_species = False
            for s in self.species:
                #If current player brain is simmiliar enough to be added to the current species s
                if s.similarity(p.brain):
                    s.add_to_species(p)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(p))

        #Species that attracted no players would crash
        self.species = [s for s in self.species if s.players]

    def calculate_fitness(self):
        for p in self.players:
            p.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        speciesBin = []
        for s in self.species:
            if len(s.players) == 0:
                speciesBin.append(s)
        for s in speciesBin:
            self.species.remove(s)

    def kill_stale_species(self):
        playerBin = []
        speciesBin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(speciesBin) + 1:
                    speciesBin.append(s)
                    for p in s.players:
                        playerBin.append(p)
                else:
                    s.staleness = 8
        for p in playerBin:
            self.players.remove(p)
        for s in speciesBin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter("benchmarkFitness"), reverse=True)

    def next_gen(self):
        children = []

        #Clone champion of each species into the new generation
        for s in self.species:
            children.append(s.champion.clone())

        #Fill open player slots with children
        children_per_species = (self.size - len(children)) // len(self.species)
        for s in self.species:
            for i in range(0, children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []

        for child in children:
            self.players.append(child)
        self.generation += 1


    #Return true if all players are dead
    def extinct(self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct
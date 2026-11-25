import numpy as np
from dataclasses import dataclass, field
import random
import matplotlib.pyplot as plt
import sys
import time
BANNER = r"""
        /\
       /  \
      | () |
      |    |
     /|    |\
    /_|____|_\
      /_||_\

  =========================
  ||    WELCOME ABOARD   ||
  =========================
"""
Fail1 = r"""  =========================
  ||    THE CREW HAS DIED  ||
  =========================
  """

Fail = r""" _______ _________ _______  _______ _________ _______  _          _______  _______ _________ _        _______  ______  
(       )\__   __/(  ____ \(  ____ \\__   __/(  ___  )( (    /|  (  ____ \(  ___  )\__   __/( \      (  ____ \(  __  \ 
| () () |   ) (   | (    \/| (    \/   ) (   | (   ) ||  \  ( |  | (    \/| (   ) |   ) (   | (      | (    \/| (  \  )
| || || |   | |   | (_____ | (_____    | |   | |   | ||   \ | |  | (__    | (___) |   | |   | |      | (__    | |   ) |
| |(_)| |   | |   (_____  )(_____  )   | |   | |   | || (\ \) |  |  __)   |  ___  |   | |   | |      |  __)   | |   | |
| |   | |   | |         ) |      ) |   | |   | |   | || | \   |  | (      | (   ) |   | |   | |      | (      | |   ) |
| )   ( |___) (___/\____) |/\____) |___) (___| (___) || )  \  |  | )      | )   ( |___) (___| (____/\| (____/\| (__/  )
|/     \|\_______/\_______)\_______)\_______/(_______)|/    )_)  |/       |/     \|\_______/(_______/(_______/(______/ 
"""



Timer1 = r"""   =========================
  ||    THREE  ||
  =========================
  """
Timer2 = r"""  =========================
  ||    TWO   ||
  =========================
"""
Timer3 = r"""
  =========================
  ||    ONE  ||
  =========================
"""
Launch = r"""
  =========================
  ||    LAUNCH!!   ||
  =========================
"""
Start = [Timer1, Timer2, Timer3, Launch]
@dataclass
class Person:

	age: int
	alive: bool = True
	sex: bool = field(default_factory=lambda: random.choice([True,False])) #True = male, fix later
	job: bool = False # only one job for now
	
	
	def age_one_year(self):
	
		self.age += 1






class Simulation:
	
	def __init__(self, population, voyage_time, min_start_age = 18, max_start_age = 45):
	
		self.people = []
		self.year = 0
		self.min_start_age = min_start_age
		self.max_start_age = max_start_age
		self.voyage_time = voyage_time
		self.population = population
		
		
		if population == 0:
			print("Cannot launch with no crew")
			sys.exit(1)
		if population == 1:
			print("Need at least one Male and one Female to launch")
			sys.exit(1)
		
		for _ in range(population):
			roll = random.random()
			if roll <= 0.1:            # only  10% of people will have this job to start
				start_age = random.randint(min_start_age, max_start_age) #only people of this age range qualify to board the ship at first
				new_person = Person(start_age, job = True)
			else:
				start_age = random.randint(min_start_age, max_start_age) #only people of this age range qualify to board the ship at first
				new_person = Person(start_age, job = False)
			self.people.append(new_person)
		
		self.ship = Ship(population)
		
			
					
				
				
				
		
	def living_people(self):
	
		living_people = []
		
		for person in self.people:
			if person.alive == True:
				living_people.append(person)
		return living_people
	
	
	def dead_people(self):
		dead_people = []
		for person in self.people:
			if person.alive == False:
				dead_people.append(person)
		return dead_people
		
				
		
		
	
	def death_check(self, hunger):
		
		
		# Gompertz–Makeham law of mortality
		alpha = 3E-5
		beta = 0.099
		lamb = hunger + 4E-4 #if lambda ever = 1, certain death for everyone
		
		
		
		
		deaths = 0
		for person in self.living_people():
			mortality_rate = alpha * (np.exp(beta * person.age)) + lamb #Death based on age, lambda is outside influence
			survival_chance = random.random()                         
			if mortality_rate >= survival_chance:
				person.alive = False
				deaths += 1
		return deaths
					
		
		
		
		
	def averages(self):
		
		age_count = 0
		death_age_count = 0
		
		for person in self.living_people():
			current_age = person.age
			age_count += current_age
			
		for person in self.dead_people():
			death_age = person.age
			death_age_count += death_age
				
			
		if len(self.living_people()) != 0:
			average_age = age_count/len(self.living_people())
		elif len(self.living_people()) == 0:
			average_age = None
		
		if len(self.dead_people()) != 0:	
			average_death_age = death_age_count/len(self.dead_people())
		elif len(self.dead_people()) == 0:
			average_death_age = None
			
			
		return average_age, average_death_age
	
	
	def sort_by_sex(self):   # this might be useful later, idk
		
		male = []
		female = [] 
		
		for person in self.people:
			if person.sex == True:
				male.append(person)
			elif person.sex == False:
				female.append(person)
		return male, female


	
	
	def birth_candidates(self):     #match people of similar ages
	
		male_parents = []
		female_parents = []	
			
		for person in self.living_people():
			if 18 <= person.age <= 50 and person.sex == True:
				male_parents.append(person)
			elif 18 <= person.age <= 50 and person.sex == False:
				female_parents.append(person)
		
		def person_age(person):
			age = person.age
			return age
			
			
			
		
		male_parents = sorted(male_parents, key=person_age)
		female_parents = sorted(female_parents, key=person_age)
		
		
		
		return male_parents, female_parents
	
	def birth_rate(self):	
		
		birth_rates = []
		
		for mom in self.birth_candidates()[1]:           # these birthrates add to about 2.1 about replacement rate with infant death into account
			if 18 <= mom.age <= 20:
				fertility_rate = 0.052
				birth_rates.append(fertility_rate)
			elif 20 < mom.age <= 28:
				fertility_rate = 0.111
				birth_rates.append(fertility_rate)
			elif 28 < mom.age <= 35:
				fertility_rate = 0.074
				birth_rates.append(fertility_rate)
			elif 35 < mom.age <= 45:
				fertility_rate = 0.053
				birth_rates.append(fertility_rate)
			elif 45 < mom.age <= 50:
				fertility_rate = 0.001
				birth_rates.append(fertility_rate)
		
			
		return birth_rates                  # I only want couples to be able to have kids, not random birth
	
	def birth_check(self):
	
		family_list = zip(self.birth_candidates()[0], self.birth_candidates()[1], self.birth_rate(), strict = False )
		
		family_rates = [item[2] for item in family_list]
		
		births = 0
		
		infant_death_chance = 0.4  #about average infant mortality rate for developed countries 
		
		for rate in family_rates:
			roll = random.random()
			if roll <= rate:
				births +=1
		
		for _ in range(births):
			roll = random.random()
			if (infant_death_chance/100) < roll:
				baby = Person(0)
			
			elif (infant_death_chance/100) >= roll:
				baby = Person(0, alive = False)
			self.people.append(baby)
		
		return births
		
		
		
	
	def step(self):
		
		
			
		
		self.year += 1
		
		for person in self.living_people():
			person.age_one_year()
		
		
		Year_births = self.birth_check()
		
		hunger = self.ship.food_consume(len(self.living_people())) 
		
		Year_deaths = self.death_check(hunger)
		
		
		
		return Year_births, Year_deaths
							
			
	def run(self):
	
		print(f"Crew: {self.population} ({len(self.sort_by_sex()[0])} Males, {len(self.sort_by_sex()[1])} Females) | Voyage: {self.voyage_time} years\n")
		population_over_time = []
		births = []
		deaths = []
		
		#time.sleep(2)
		
		for i in range(4):
			print(Start[i])
			#time.sleep(1)
		#time.sleep(1)
		
		for _ in range(self.voyage_time):
			year_births, year_deaths = self.step()
			births.append(year_births)
			living = self.living_people()
			living_count = len(living)
			population_over_time.append(living_count)
			death_count = len(self.dead_people())
			deaths.append(year_deaths)
			
			
			
			if self.averages()[1] == None: #ill figure out how I want to handle this case later
				pass
			elif self.averages()[1] != None:
				avg_dead = int(self.averages()[1])
			
			if self.averages()[0] == None: #ill figure out how I want to handle this case later
				pass
			elif self.averages()[0] != None:
				avg_living = int(self.averages()[0])
			
		
			if self.year % 1 == 0:
		
				print(f"{self.year} years after departure: There are {living_count} people living, and {death_count} have died")
				if self.averages()[1] == None:
					print("No one has died.")
				elif avg_dead != None:
					print(f"The average age is {avg_living}, the average age of death is {avg_dead}")
				print(f"{year_births} babies were born this year!\n")
				
			if len(living) == 0:
				print(Fail1)
				print(Fail)
				sys.exit(1)
			
			
		times = np.linspace(0, self.voyage_time,len(population_over_time))
		plt.plot(times, population_over_time)
		plt.ylabel("Crew Population")
		plt.xlabel("Years")
		plt.grid(True)                                      #I like graphs
		plt.show()
		plt.plot(times, births)
		plt.ylabel("Births")
		plt.xlabel("Years")
		plt.grid(True)
		plt.show()
		plt.plot(times, deaths)
		plt.ylabel("Deaths")
		plt.xlabel("Years")
		plt.grid(True)
		plt.show()
		


class Ship:
	def __init__(self, initial_crew):
	
		
		self.food = 100 * initial_crew # 100 food units per inital crew member 
	
	
	
	def farming(self, farmers):
		
		
		
		
		
	def food_consume(self, crew):
		
		food_needed = 20 * crew # the crew eats food at a rate of 20 food units per year to be healthy
		
		feed_index = self.food / food_needed # zero means no stock, high numbers mean people are eating well
		
		if feed_index > 1:          #people dont eat more than they need
			feed_index = 1  
		
		self.food -= food_needed * feed_index # people can only eat based on available food
		
		
		
		
		return 1 - feed_index	# a value of 0 adds nothing to the death probability 
		
	
		
		
	
		
		
		
		
	
		
		
		
		
		
		
		
		
		
		
		
		
	
			
if __name__ == '__main__':

	
	
	print(BANNER)
	Simulation1 = Simulation(1000, 100)
	Simulation1.run()			
		
		
			
			
		
		
		
	
		

	


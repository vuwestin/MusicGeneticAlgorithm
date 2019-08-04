#!/usr/bin/env python
import random
from mingus.midi import fluidsynth
from mingus.containers import Note, Bar, Track
import sys, time

def createInitialPopulation(n, q):
	#n is an integer for the size of the population
	#q is the amount of notes in the song
	#returns an array of integer arrays
	population = []
	for _ in range(0,n):
		organism = []
		for i in range(0,q):
			organism.append(random.randint(0,84))
			population.append(organism)
	return population

def calcFitness(lst, sol):
	#lst is a list of integers
	#sol is also a list of integers
	#returns an double from 0.0 to 1.0 where 1.0 is the highest possible fitness
	fitness = 0.0
	for i in range(0,len(lst)):
		if lst[i] == sol[i]:
			fitness += 1.0
	return fitness / len(sol)

def crossover(arr1, arr2):
	#arr1 and 2 are integer lists
	#returns an integer list
	result = []
	midpoint = random.randint(0, len(arr1))
	for i in range(len(arr1)):
		if i < midpoint:
			result.append(arr1[i])
		else:
			result.append(arr2[i])
	return result

def mutate(arr,rate):
	#arr is a list of integers
	#rate is a double from 0 to 1 that signifies the mutation rate
	for i in range(len(arr)):
		if(random.random() < rate):
			arr[i] = random.randint(0, 84)
	return arr

def findMostFit(pop, sol):
	#pop is a population which is an array of integer arrays
	#sol is a list of integers
	mostFit = pop[0]
	for x in pop:
		if calcFitness(x, sol) > calcFitness(mostFit, sol):
			mostFit = x
	return mostFit
	#returns a list of integers

def createNewPopulation(pop, sol, rate):
	#pop is a population which is an array of integer arrays
	#sol is a list of integers
	#rate is the mutation rate from 0 to 1
	newPopulation = []
	for _ in range(len(pop)):
		firstParentValid = False
		secondParentValid = False
		firstParent = 0
		secondParent = 0
		while (firstParentValid == False):
			firstParent = pop[random.randint(0, len(pop)-1)]
			if random.random() < calcFitness(firstParent, sol):
				firstParentValid = True
		while (secondParentValid == False):
			secondParent = pop[random.randint(0, len(pop)-1)]
			if random.random() < calcFitness(secondParent, sol):
				secondParentValid = True
		child = crossover(firstParent, secondParent)
		child = mutate(child, rate)
		newPopulation.append(child)
	return newPopulation

def playTrack(arr):
	fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2',"alsa")
	SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
	if not fluidsynth.init(SF2):
		print "Couldn't load soundfont", SF2
		sys.exit(1)
	t = Track()
	for note in arr:
		t + note
	fluidsynth.play_Track(t,1)
		



def main():
	fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2',"alsa")
	solution = [52,52,53,55,55,53,52,50,48,48,50,52,52,50,50]
	#testSol = [1,3,53,55,55,53,52,50,48,48,50,52,52,50,50]
	population = createInitialPopulation(250, len(solution))
	#t = Track()
	#for note in findMostFit(population,solution):
	#	t + note
	#fluidsynth.play_Track(t,1)
	generation = 1
	highestFitness = calcFitness(findMostFit(population, solution), solution)
	print("Generation: 1")
	print("Initial Highest Fitness: " + str(highestFitness))
	#print(calcFitness(testSol,solution))

	while highestFitness < 1:
		population = createNewPopulation(population, solution, .01)
		generation = generation + 1
		highestFitness = calcFitness(findMostFit(population, solution), solution)
		print("Generation: " + str(generation))
		print("Highest Fitness level: " + str(highestFitness))
		if generation % 10 == 0:
			print("hi")
			t = Track()
			for noteInt in findMostFit(population,solution):
				newNote = Note()
				newNote.from_int(noteInt)
				t + newNote
			fluidsynth.play_Track(t,1)
			#time.sleep(10)
	t = Track()
	for note in findMostFit(population,solution):
		t + note
	fluidsynth.play_Track(t,1)










if __name__ == '__main__':
	main()

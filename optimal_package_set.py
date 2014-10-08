'''
Austin White
austinw@csu.fullerton
10/7/2014

Lab 2
Optimal Package Set
'''

import sys, time

'''
Construct a simple class representing a Debian Package
that can be used to encapsulate the data that is read
from the specified file
'''
class DebianPackage(object):

	name  = None
	size  = None
	votes = None

	def __init__(self, n, v, s):
		self.name = n
		self.size = s
		self.votes = v

	def getName(self):
		return self.name

	def getSize(self):
		return self.size

	def getVotes(self):
		return self.votes

	def __str__(self):
		return '   ' + self.getName() + ' ' + str(self.getSize()) + ' ' + str(self.getVotes()) + 'kb'

'''
Use the subsets algorithm to construct a list
of all subsets of the list
'''
def subsets(packages):
	result = [[]]

	for x in packages:
		with_x = []
		for s in result:
			with_x.append(s + [x])
		result += with_x
	return result

'''
The Optimal Package Set algorithm. Constructed using
subroutines of other, simpler algorithms
'''
def optimalPackageSet(packages, W):
	best = None
	bestValue = 0

	allCandidates = subsets(packages)

	for candidate in allCandidates:
		if verifyOptimalPackageSet(W, candidate):
			if best == None or totalVotes(candidate) > bestValue:
				best = candidate
				bestValue = totalVotes(best)

	return best

'''
Calculate the total votes of a given candidate
of packages
'''
def totalVotes(candidate):
	totalVotes = 0

	for item in candidate:
		totalVotes += item.getVotes()

	return totalVotes

'''
Verify that the candidate is under the specified
value of W
'''
def verifyOptimalPackageSet(W, candidate):
	totalSize = 0

	for item in candidate:
		totalSize += item.getSize()

	return totalSize <= W

def printResults(bestPackageSet, startTime, endTime, n, w):
	print('----- n = ' + str(n) + ' W = ' + str(w))
	print('   −− Exhaustive search solution −−')

	totalSize = 0
	totalVotes = 0

	for packageSet in bestPackageSet:
		print(packageSet)
		totalSize += packageSet.getSize()
		totalVotes += packageSet.getVotes()

	print('   Total size = ' + str(totalSize) + 'kb, total votes = ' + str(totalVotes))

	print('   Elapsed time = ' + '%.2f' %  round(endTime - startTime, 2) + ' seconds')

def main():

	'''
	Use `python optimal_package_set.py [file] [lower bound] [upper bound] --scatter`
	to generate the scatter plot data
	'''
	if len(sys.argv) == 5 and '--scatter' in sys.argv:
		filename = sys.argv[1]

		lowerBound = int(sys.argv[2])
		upperBound = int(sys.argv[3]) + 1
		
		w = 2000

		for n in range(lowerBound, upperBound):
			f = open(filename, 'r')
			allPackages = []
			packageLengthVerification = None

			i = 0
			for line in f:

				if i > n:
					break
				
				# skip the first line
				if i is not 0:
					components = line.split(' ')
					package = DebianPackage(components[0], int(components[1]), int(components[2]))
					allPackages.append(package)
				else:
					packageLengthVerification = int(line)

				i = i + 1

			assert(len(allPackages) == n)
			
			start = time.perf_counter()
			
			# Algorithm
			bestPackageSet = optimalPackageSet(allPackages, w)

			end = time.perf_counter()
			
			# Display results...
			printResults(bestPackageSet, start, end, n, w)


	elif len(sys.argv) == 4:
		filename = sys.argv[1]
		
		n = int(sys.argv[2])
		w = int(sys.argv[3])

		f = open(filename, 'r')
		allPackages = []
		packageLengthVerification = None

		i = 0
		for line in f:

			if i > n:
				break
			
			# skip the first line
			if i is not 0:
				components = line.split(' ')
				package = DebianPackage(components[0], int(components[1]), int(components[2]))
				allPackages.append(package)
			else:
				packageLengthVerification = int(line)

			i = i + 1

		assert(len(allPackages) == n)
		
		start = time.perf_counter()
		
		# Algorithm
		bestPackageSet = optimalPackageSet(allPackages, w)

		end = time.perf_counter()
		
		# Display results...
		printResults(bestPackageSet, start, end, n, w)

	else:
		print('ERROR: incorrect number of arguments specified\n\n' +
			  'USAGE: \n\tpython3 <source code file> <text file> <n> <W> OR:' + 
			  '\n\tpython3 <source code file> <text file> <lower bound> <upper bound> --scatter')
		sys.exit(1)
	
	f.close()

if __name__ == '__main__':
	main()

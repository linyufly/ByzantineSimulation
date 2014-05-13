#!/usr/bin/python

from random import randint
import random
import sys

def PrintIndent(indent):
	for i in range(0, indent):
		sys.stdout.write('  ')

def OralMessage(generals, commander, M, initialValues, isFaulty, indent):
	generals = [general for general in generals if general != commander] 

	for i in range(0, len(generals)):
		PrintIndent(indent)
		print commander, '->', generals[i], ':', initialValues[i] if not isFaulty[commander] \
							else '%d (faulty)' % (initialValues[i])

	if M == 0:
		return list(initialValues)

	interaction = []
	for i in range(0, len(generals)):
		if isFaulty[generals[i]]:
			commands = [randint(0, 1) for idx in range(0, len(generals) - 1)]
		else:
			commands = [initialValues[i]] * (len(generals) - 1)

		result = OralMessage(generals, generals[i], M - 1, commands, isFaulty, indent + 1)

		result.insert(i, initialValues[i])
		interaction.append(result)

	result = []
	for i in range(0, len(generals)):
		votes = [interaction[idx][i] for idx in range(0, len(generals))]
		cntOfZeros = votes.count(0)
		cntOfOnes = votes.count(1)
		cntOfFaulties = votes.count(-1)
		beOne, beZero = cntOfOnes + cntOfFaulties > cntOfZeros, \
				cntOfZeros + cntOfFaulties >= cntOfOnes
		result.append(1 if beOne and not beZero else 0 if beZero and not beOne else -1)

	return result

def main(argv):
	print 'Oral Message'

	if len(argv) != 1:
		print 'Please specify the input file by: OralMessage.py <filename>'
		return

	fileName = argv[0]
	print 'Case file:', fileName
	reader = open(fileName)
	numOfGenerals, commander, M = line = map(int, reader.readline().split())
	print 'numOfGenerals:', numOfGenerals
	print 'commander:', commander
	print 'M:', M
	isFaulty = map(int, reader.readline().split())
	isFaulty = [True if value == 1 else False for value in isFaulty]
	for i in range(0, numOfGenerals):
		if isFaulty[i]:
			print 'General %d is faulty.' % (i)
	initialValues = map(int, reader.readline().split())
	for i in range(1, numOfGenerals):
		print 'General %d receives %s.' % (i, 'attack' if initialValues[i - 1] == 1 else 'retreat')

	random.seed()
		
	print 'Start simulation'
	result = OralMessage(range(0, numOfGenerals), commander, M, initialValues, isFaulty, 0)

	print 'Result'
	for i in range(0, len(result)):
		idx = i if i < commander else i + 1
		if not isFaulty[idx]:
			print 'General %d will %s.' % (idx, 'attack' if result[i] == 1 else \
							'retreat' if result[i] == 0 else 'attack or retreat')

if __name__ == '__main__':
	main(sys.argv[1 : ])

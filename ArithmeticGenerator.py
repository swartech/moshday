import time
import math
import random

random.seed(time.time())

output_file = open('questions.txt', 'w')

def random_question(lower, upper, operator):
	left = random.randint(lower, upper)
	right = random.randint(lower, upper)
	if operator == '/':
		while left % right != 0:
			left = random.randint(lower, upper + 9)
			right = random.randint(lower, upper)
	question = ''.join('%d %s %d' % (left, operator, right))
	answer = eval(question)
	
	if operator == '*':
		operator = 'x'
		question = ''.join('%d %s %d' % (left, operator, right))
	elif operator == '/':
		operator = '%'
		question = ''.join('%d %s %d' % (left, operator, right))
	
	answer1 = answer + (random.randint(-3, 3))
	while (answer1 == answer):
		answer1 = answer + (random.randint(-3, 3))
	answer2 = answer + (random.randint(-3, 3))
	while (answer2 == answer or answer2 == answer1):
		answer2 = answer + (random.randint(-3, 3))
		
	answers = [answer, answer1, answer2]
	random.shuffle([answer, answer1, answer2])
	
	return '%s\t%d\t%d\t%d\t%d\n' % (question, answer, answers[0], answers[1], answers[2])
	
def random_operator():
	rand = random.randint(0, 3)
	if rand == 0:
		return '+'
	elif rand == 1:
		return '-'
	elif rand == 2:
		return '*'
	elif rand == 3:
		return '/'

number_of_questions = 20
lower = 1
upper = 12

questions = set()

while len(questions) < number_of_questions:
	questions.add(random_question(lower, upper, random_operator()))

for i in questions:
	output_file.write(i)
output_file.close()

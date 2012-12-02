import time
import math
import random

random.seed(time.time())

maths = open('maths.txt', 'w')
science = open('science.txt', 'w')
english = open('english.txt', 'w')
full_english = open('full_english.txt', 'r')
full_science = open('full_science.txt', 'r')

def random_maths(lower, upper, operator):
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

number_of_questions = 10
lower = 1
upper = 12

maths_questions = set()
science_questions = set()
english_questions = set()

while len(maths_questions) < number_of_questions:
	maths_questions.add(random_maths(lower, upper, random_operator()))

science_questions = random.sample(full_science.readlines(), number_of_questions)

#while len(english_questions) < number_of_questions:
	#english_questions.add(random_english())

for i in maths_questions:
	maths.write(i)
	
for i in science_questions:
	science.write(i)
maths.close()
science.close()
english.close()
full_english.close()

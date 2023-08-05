class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age

	def say_hi(self):
		print("Hi! My name is {}. I am {} years old.".format(self.name, self.age))
		return

	def is_adult(self):
		if self.age < 18:
			return False
		return True

	def can_drink(self):
		if self.age < 21:
			return False
		return True
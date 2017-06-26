class Employee:
	def __init__(self, f_name, l_name, pay):
		self.first_name = f_name
		self.last_name = l_name
		self.full_name = '{} {}'.format(self.first_name, self.last_name)
		self.pay = pay
		self.email = '{}{}@company.com'.format(self.first_name.capitalize, self.last_name.capitalize)
		self.raise_amount = 1.04

	def apply_raise(self):
		self.pay *= self.raise_amount

class Developer(Employee):
	def __init__(self, f_name, l_name, pay):
		super().__init__(f_name, l_name, pay)
		self.raise_amount = 1.1

person1 = Developer('John', 'Smith', 70000)
print(person1.pay)
person1.apply_raise()
print(person1.pay)
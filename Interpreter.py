import time

class Program:
	def __init__(self, characters):
		self.dict = {}
		self.List = compoundStat(characters, self.dict).funcn()
	
	def runn(self):
		t1 = time.time()
		for i in range(len(self.List)):
			self.List[i].runn(self.dict)
		t2 = time.time()
		self.t = t2-t1
  
	def __str__(self):
		return str(self.dict)
  
	def duration(self):
		return self.t


  
class Statements:
	def __init__(self, stat, dict):
		self.i = stat.find(';')
		self.State = stat[0:self.i]
		stat = stat[self.i+1:]
		self.rem = stat
	def funcn(self):
		return self.State, self.rem
	def runn(self, dict):
		self.States = Assignment(self.State, dict)

class whileStat:
	def __init__(self, stat, dict):
		self.flag = 0
		for i in range(1,len(stat)):
			self.word = stat[i:]
			if self.word.startswith("while"):
				self.flag = self.flag + 1
			if self.word.startswith("done"):
				if self.flag == 0:
					break
				else:
					self.flag = self.flag -1
		self.State =stat[0:i]
		stat = stat[i+4:]
		self.rem = stat
	
	def funcn(self):
		return self.State, self.rem
	
	def comp(self, dict):
		i = self.State.find("do")
		self.cond = self.State[5:i]
		head = self.State[i+2:]
		self.variant = compoundStat(head, dict).funcn()
	def runn(self, dict):
		self.comp(dict)
		self.cond = self.cond.replace(" ","")
		self.cond = condition(self.cond, dict)
		while self.cond.cond_evaluate(dict):
			for i in range(len(self.variant)):
				self.variant[i].runn(dict)
		

class ifStat:
	def __init__(self, stat, dict):
		self.flag = 0
		for i in range(1,len(stat)):
			self.word = stat[i:]
			if self.word.startswith("if"):
				self.flag = self.flag + 1
			if self.word.startswith("fi"):
				if self.flag == 0:
					break
				else:
					self.flag = self.flag-1
		self.State =stat[0:i]
		stat = stat[i+2:]
		self.rem = stat
	
	def funcn(self):
		return self.State, self.rem

	def comp(self, dict):
		for i in range(len(self.State)):
			word = str(self.State[i:])
			if word.startswith("then"):
				break
		self.flag = 0
		head = self.State[2:i]
		print(head)
		self.cond = condition(head, dict)
		self.State = self.State[i+4:]
		for i in range(len(self.State)):
			self.word = self.State[i:]
			if self.word.startswith("if"):
				self.flag = self.flag+1
			elif self.word.startswith("fi"):
				self.flag = self.flag - 1
			elif self.word.startswith("else"):
				if self.flag == 0:
		  			break
		if i != len(self.State) - 1:
			self.thenstat = str(self.State[0:i])
			self.elstat = str(self.State[i+4:])
		else:
			self.thenstat = str(self.State[0:])
			self.elstat = ""
	
	def runn(self, dict):
		self.comp(dict)
		self.thenstats = compoundStat(self.thenstat, dict).funcn()
		self.elstats = compoundStat(self.elstat, dict).funcn()
		if self.cond.cond_evaluate(dict):
			for i in range(len(self.thenstats)):
				self.thenstats[i].runn(dict)
		else:
			for i in range(len(self.elstats)):
				self.elstats[i].runn(dict)
		
	
class func:
	def __init__(self, characters, dict):
		i = characters.find("end")
		self.State = characters[0:i]
		self.rem = characters[i+3:]
  
	def funcn(self):
		return self.rem
	  
	def comp(self, dict):
		i = self.State.find("begin")
		word = self.State[i+5:].split("return")
		self.funct = Program(word[0])
		self.word = word[1].replace(" ", "").replace(";", "")
		self.State = self.State[0:i] 
		self.State = self.State.replace(" ", "")
		i = self.State.find("(")
		j = self.State.find(")")
		self.name = self.State[0:i]
		self.variabs = self.State[i+1:j].split(",")
		print(self.variabs)
	def runn(self, dict, calls):
		self.comp(dict)
		i = calls.find("(")
		calls = calls.replace(" ", "")
		calls = calls[i+1:-1].split(",")
		if len(calls) != len(self.variabs):
			raise Exception("Variable Mismatch")
		for i in range(len(calls)):
			self.funct.dict[self.variabs[i]] = dict[calls[i]]
		self.funct.runn()
		return expression(self.word, self.funct.dict).evaluate(self.funct.dict)


class printstat:
	def __init__(self, stat, dict):
		i = stat.find(';')
		self.State = stat[0:i]
		self.rem = stat[i+1:]
	def funcn(self):
		return self.State, self.rem
	
	def runn(self, dict):
		word = self.State[0:]
		if word.startswith("println"):
			word = self.State[7:]
			if '"' in word:
				word = word.strip(" ")
				print(word[1:-1])
			else:
				word = word.strip(" ")
				print(dict[word])
		else:
			word = self.State[5:]
			if '"' in word:
				word = word.strip(" ")
				print(word[1:-1]),
			else:
				word = word.strip(" ")
				print(dict[word]),


class compoundStat:
	def __init__(self, stat, dict):
		self.L = []
		stat = stat.rstrip()
		while len(stat) >0:
			stat = stat.lstrip()
			if stat.startswith('while'):
				temps = whileStat(stat, dict)
				temp, stat = temps.funcn()
				self.L += [temps]
			elif stat.startswith('if'):
				temps = ifStat(stat, dict)
				temp, stat = temps.funcn()
				self.L += [temps]
			elif stat.startswith("function"):
				temps = func(stat, dict)
				i = stat.find("(")
				word = stat[0:i].replace("function", "").strip(" ")
				dict[word] = temps
				stat = temps.funcn()	    
			elif stat.startswith('print'):
				temps = printstat(stat, dict)
				temp, stat = temps.funcn()
				self.L += [temps]
			else:	
				temps = Statements(stat, dict)
				temp, stat = temps.funcn()
				self.L += [temps]
		
	def funcn(self):
		return self.L

	def __str__(self):
		return str(self.L)
	


class expression:
	def __init__(self, characters, dict):
		self.characters = characters
	
	def evaluate(self, dict):
		self.characters = self.characters.replace(" ","").replace("\n", "")
		if '+' in self.characters:
			self.left, self.right = self.characters.split('+')
			self.left = expression(self.left, dict)
			self.right=expression(self.right, dict)
			self.left=self.left.evaluate(dict)
			self.right=self.right.evaluate(dict)
			return self.left+self.right
		elif '-' in self.characters:
			self.left, self.right = self.characters.split('-')
			self.left = expression(self.left, dict)
			self.right=expression(self.right, dict)
			self.left=self.left.evaluate(dict)
			self.right=self.right.evaluate(dict)
			return self.left-self.right
		elif '*' in self.characters:
			self.left, self.right = self.characters.split('*')
			self.left = expression(self.left, dict)
			self.right=expression(self.right, dict)
			self.left=self.left.evaluate(dict)
			self.right=self.right.evaluate(dict)
			return self.left*self.right
		elif '/' in self.characters:
			self.left, self.right = self.characters.split('/')
			self.left = expression(self.left, dict)
			self.right=expression(self.right, dict)
			self.left=self.left.evaluate(dict)
			self.right=self.right.evaluate(dict)
			if self.right == 0:
				raise Exception("Division by 0")
			return self.left/self.right
		elif self.characters.replace(".", "").isdigit():
			return float(self.characters)
		elif self.characters.lstrip("-").replace(".","").isdigit():
			lp = -int(self.characters.replace("-", ""))
			return lp
		elif "(" in self.characters:
			self.characters = self.characters.split("(")
			return dict[self.characters[0]].runn(dict,self.characters[1])
		else:
			return dict[self.characters]


	  
	  
class Assignment:
	def __init__(self, characters, dict):
		characters = characters.replace(" ","")
		self.left, self.right = characters.split(":=")
		self.right = expression(self.right, dict)
		dict[self.left] = self.right.evaluate(dict)


class condition:
	def __init__(self, characters, dict):
		self.characters = characters

	def cond_evaluate(self, dict):
		if "<=" in self.characters:
			self.left, self.right = self.characters.split("<=")
			self.left = expression(self.left, dict)
			self.right = expression(self.right, dict)
			self.left = self.left.evaluate(dict)
			self.right = self.right.evaluate(dict)
			if self.left <= self.right:
				return True
			else:
				return False
		elif ">=" in self.characters:
			self.left, self.right = self.characters.split(">=")
			self.left = expression(self.left,dict)
			self.right = expression(self.right,dict)
			self.left = self.left.evaluate(dict)
			self.right = self.right.evaluate(dict)
			if self.left >= self.right:
				return True
			else:
				return False
		elif "=" in self.characters:
			self.left, self.right = self.characters.split("=")
			self.left = expression(self.left, dict)
			self.right = expression(self.right, dict)
			self.left = self.left.evaluate(dict)
			self.right = self.right.evaluate(dict)
			if self.left == self.right:
				return True
			else:
				return False
		elif "!=" in self.characters:
			self.left, self.right = self.characters.split("!=")
			self.left = expression(self.left,dict)
			self.right = expression(self.right, dict)
			self.left = self.left.evaluate(dict)
			self.right = self.right.evaluate(dict)
			if self.left != self.right:
				return True
			else:
				return False
		elif "<" in self.characters:
			self.left, self.right = self.characters.split("<")
			self.left = expression(self.left, dict)
			self.right = expression(self.right, dict)
			self.left = self.left.evaluate(dict)
			self.right = self.right.evaluate(dict)
			if self.left < self.right:
				return True
			else:
				return False
		elif ">" in self.characters:
			self.left, self.right = self.characters.split(">")
			self.left = expression(self.left, dict)
			self.right = expression(self.right, dict)
			self.left = self.left.evaluate(dict)
			self.right = self.right.evaluate(dict)
			if self.left > self.right:
				return True
			else:
				return False


F = open("test4.txt", "r")	
num = F.read()
F.close()
numb = Program(num)
numb.runn()
print(numb)
print("Time required to run",numb.t)

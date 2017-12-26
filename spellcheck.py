import re, collections, sys
from misspell import Misspell
class SpellCheck:

	alphabet = 'abcdefghijklmnopqrstuvwxyz'

	def __init__(self, path):
		self.dictPath = path

	def words(self, text): 
		return re.findall('[a-z]+', text.lower()) 

	def train(self, words):
		occurences = {}
		for l in self.alphabet:
			occurences[l] = collections.defaultdict(lambda: 1)
		for w in words:
			occurences[w[0]][w] += 1 #Incrementing occurence of word
		return occurences

	def edits1(self, word):
		splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes = [a + b[1:] for a, b in splits if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
		replaces = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
		inserts = [a + c + b     for a, b in splits for c in self.alphabet]
		return set(deletes + transposes + replaces + inserts)

	def known_edits2(self, word, wDict):
		return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in wDict)

	def known(self, word, wDict): 
		return set(w for w in word if w in wDict)

	def correct(self, word, wDict):
		candidates = self.known([word], wDict[word[0]]) or self.known(self.edits1(word), wDict[word[0]]) or self.known_edits2(word, wDict[word[0]]) or [word] 
		return max(candidates, key=wDict.get) # returning the element of the set with the highest probability of being the correct word

	

	def run(self, option):
		lWords = self.words(file(self.dictPath).read())
		try:
			if option == '0':
				lWords = self.train(lWords)
				while True:
					word = raw_input('>')
					if not word.isalpha():
						continue
					spellchk = self.correct(word.lower(), lWords)
					if spellchk == word and spellchk not in lWords[word[0]]:
						print 'NO SUGGESTION'
					else:
						print spellchk
					print #'\n'
			elif option == '1':
				misspell = Misspell(lWords)
				lWords = self.train(lWords)
				while True:
					word = misspell.genWord()
					print 'Incorrect -', word
					spellchk = self.correct(word, lWords)
					if spellchk == word and spellchk not in lWords[word[0]]:
						print 'NO SUGGESTION'
					else:
						print 'Correct   -',spellchk
					print #'\n'
					raw_input('<enter>\n') 
		except KeyboardInterrupt: 
			
			'exit'
		except EOFError:
			'exit'

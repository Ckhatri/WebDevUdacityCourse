import webapp2
import validation

#found at udacitychirag.appspot.com/rot

form = """
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea type = "text" name="text" style="height: 100px; width: 400px;">%(text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

alphabet_dict = {'a':'n',
                'b':'o',
                'c':'p',
                'd':'q',
                'e':'r',
                'f':'s',
                'g':'t',
                'h':'u',
                'i':'v',
                'j':'w',
                'k':'x',
                'l':'y',
                'm':'z',
                'n':'a',
                'o':'b',
                'p':'c',
                'q':'d',
                'r':'e',
                's':'f',
                't':'g',
                'u':'h',
                'v':'i',
                'w':'j',
                'x':'k',
                'y':'l',
                'z':'m',}

#goes through whatever was inputted and applies the cypher to it
def rotCipher(currentText):
		cipherText = ""
		for letter in currentText:
			currentLetter = letter
			if currentLetter.isalpha():
				#done to preserve ase
				if currentLetter.isupper():
					lowerCaseVer = currentLetter.lower()
					lowerCaseVerCipher = alphabet_dict[lowerCaseVer]
					upperCase = lowerCaseVerCipher.upper()
					cipherText += upperCase
				else:
					cipherText += alphabet_dict[currentLetter]
			else:
				cipherText += currentLetter
		return cipherText


class Rot13(webapp2.RequestHandler):
	#write out something into the text box, usually it'll be the returned cypher'd text.
	def write_form(self, text="Hello enter anything!"):
		self.response.out.write(form % {"text" : validation.escape_html(text)})

	def get(self):
		self.write_form()

	#get the text and cypher it
	def post(self):
		user_text = self.request.get('text')
		newCipher = rotCipher(user_text)
		self.write_form(newCipher)

app = webapp2.WSGIApplication([('/rot', Rot13)], debug=True)

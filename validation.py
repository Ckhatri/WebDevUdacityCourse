import cgi
import re

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

#just testing pythons string substition
given_string = "I think %s is a perfectly normal thing to do in public."
given_string2 = "I think %s and %s are perfectly normal things to do in public."
given_string3 = "I'm %(nickname)s. My real name is %(name)s, but my friends call me %(nickname)s."
          
def valid_month(month):
     if month:
          newMonth = month.capitalize()
          if newMonth in months:
               return newMonth
def valid_day(day):
     if day and day.isdigit():
          intDay = int(day)
          if (intDay >= 1 and intDay <= 31):
               return intDay

def valid_year(year):
     if year and year.isdigit():
          intYear = int(year)
          if (intYear >= 1900 and intYear <= 2020):
               return intYear

def sub1(s):
     return given_string % s

def sub2(s1, s2):
     return given_string2 % (s1, s2)

def sub_m(name, nickname):
     return given_string3 % {'name': name, 'nickname': nickname}

#method to escape from html if it's inputted
def escape_html(s):
     return cgi.escape(s, quote = True)

#check to see if the information given is valid uses regular expressions.
def valid_username(username):
     if USER_RE.match(username):
          return True

def valid_password(password):
     if PASS_RE.match(password):
          return True

def verifyPass(pass1, pass2):
     return pass1 == pass2

def valid_email(email):
     if EMAIL_RE.match(email):
          return True

import webapp2
import validation

#found at udacitychirag.appspot.com/signup
#html form that the page shows at first, has certain values to be filled in such as username, email and the errors. By default these will be blank and will only change if prompted by a failed submit.
form = """
<!DOCTYPE html>

<html>
    <head>
        <title>Sign Up</title>
        <style type="text/css">
            .label {text-align: right}
            .error {color: red}
        </style>

    </head>

    <body>
        <h2>Signup</h2>
        <form method="post">
            <table>
                <tr>
                    <td class="label">
                        Username
                    </td>
                    <td>
                        <input type="text" name="username" value="%(username)s">
                    </td>
                    <td class="error">
                    %(error_username)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        Password
                    </td>
                    <td>
                        <input type="password" name="password" value="">
                    </td>
                    <td class="error">
                    %(error_password)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        Verify Password
                    </td>
                    <td>
                        <input type="password" name="verify" value="">
                    </td>
                    <td class="error">
                    %(error_verify)s  
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        Email (optional)
                    </td>
                    <td>
                        <input type="text" name="email" value="%(email)s">
                    </td>
                    <td class="error">
                    %(error_email)s 
                    </td>
                </tr>
            </table>

            <input type="submit">
        </form>
    </body>

</html>
"""
import random
import string
import hashlib

rainbowTables = {}
def make_salt():
        return ''.join(random.choice(string.letters) for x in xrange(5))

# Implement the function valid_pw() that returns True if a user's password 
# matches its hash. You will need to modify make_pw_hash.

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
        salt = h.split('|')[1]
        return h == make_pw_hash(name, pw, salt)

class SignUp(webapp2.RequestHandler):
        def write_form(self, username = "", password = "", verify = "", email = "", error_username = "", error_password = "", error_verify = "", error_email = ""):
            self.response.out.write(form % {"username": username, "password": password, "verify": verify, "email": email, "error_username": error_username, "error_password": error_password, "error_verify": error_verify, "error_email":error_email})
        def get(self):
            self.write_form()
        def post(self):
            #get all the information
            have_error = False
            user_username = self.request.get('username')
            user_password = self.request.get('password')
            user_passVerify = self.request.get('verify')
            user_email = self.request.get('email')

            #check to see if everything is valid
            validUser = validation.valid_username(user_username)
            validPass = validation.valid_password(user_password)
            validVerify = validation.verifyPass(user_password, user_passVerify)
            validEmail = validation.valid_email(user_email)

            #what should be shown if there is an error
            usernameToInput = ""
            passwordToInput = ""
            verifyToInput = ""
            emailToInput = ""
            errorUser = ""
            errorPass = ""
            errorVerify = ""
            errorEmail = ""

            #if there is an error with a user, tell them, else you can show that same username because it is valid even if there are other issues such as with email
            if not validUser:
                errorUser = "That is not a valid username."
                have_error = True
            else:
                usernameToInput = user_username

            #if theres an error with the password tell them, note do not save anything because it is a password
            if not validPass:
                errorPass = "That is not a valid password."
                have_error = True
             #if theres an error with the password not matching tell them, note do not save anything because it is a password
            if not validVerify:
                errorVerify = "Passwords do not match."
                have_error = True
            #if theres an error with the email tell them, if there isn't save it and show if there is an issue with anything else.
            if not validEmail:
                errorEmail = "That is not a valid email"
                have_error = True
            else:
                emailToInput = user_email
            user_id_cookie = self.request.cookies.get('user_id')
            if user_id_cookie:
                if user_username in rainbowTables.keys():
                    errorUser = "User already exists!"
                    self.write_form(usernameToInput, passwordToInput, verifyToInput, emailToInput, errorUser, errorPass, errorVerify, errorEmail)
            elif not have_error:
                hashsling = make_pw_hash(user_username, user_password)
                self.response.headers.add_header('Set-Cookie', 'user_id=%s' % hashsling)
                rainbowTables.update({user_username: hashsling})
                self.redirect('/welcome')
            elif have_error:
                self.write_form(usernameToInput, passwordToInput, verifyToInput, emailToInput, errorUser, errorPass, errorVerify, errorEmail)
            #else redirect to welcome page
            else:
                self.redirect('/welcome')



#posts a simple welcome, gets the username through the redirect and then says welcome username
class Welcome(webapp2.RequestHandler):
    def get(self):
        welcoming = "Welcome, "
        user_id_cookie = self.request.cookies.get('user_id')
        for username in rainbowTables:
            if rainbowTables[username] == user_id_cookie:
                welcoming += username
                welcoming += "!"
        self.response.out.write(welcoming)

app = webapp2.WSGIApplication([('/signup', SignUp), ('/welcome', Welcome)], debug = True)

import os
import webapp2
import jinja2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jina_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def blog_key(name):
    return db.Key.from_path('blogs', name)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		t = jina_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Post(db.Model):
	title = db.StringProperty(required = True)
	post = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True, required = True)

class Blog(Handler):
	#shows the ten most recent posts.
	def render_front(self, posts = ""):
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC limit 10")
		self.render("blog.html", posts=posts)

	def get(self):
		self.render_front()

class NewPost(Handler):
	def render_format(self, title="", post="", error=""):
		self.render("newblog.html", title = title, post=post, error=error)

	def get(self):
		self.render_format()

	def post(self):
		title = self.request.get('title')
		post = self.request.get("post")

		#if successfully created a new post redirect to a new url with the id being after /
		if title and post:
			p = Post(title = title, post = post)
			p.put()
			self.redirect('/blog/%s' % str(p.key().id()))

		#else error show them the same page again
		else:
			error = "We need both a title and something to post"
			self.render_format(title = title, post = post, error = error)

class successNewPost(Handler):

	#after successfully posting, show them the success page based on the id given.
	def get(self, post_id):
		key = db.Key.from_path('Post', int(post_id))
		post = db.get(key)

		self.render("successnewpost.html", post = post)



app = webapp2.WSGIApplication([('/blog', Blog), ('/blog/([0-9]+)', successNewPost), ('/blog/newpost', NewPost), ], debug=True)

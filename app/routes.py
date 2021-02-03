from app import app

@app.route('/')
@app.route('/index')
def index():
	return "Тут будет лобби"


@app.route('/register')
def register_req():
	return "А тут регистрация"


@app.route('/authorization')
def authorization_req():
	return "А тут регистрация"


@app.route('/auction')
def auction_req():
	return "Страничка с аукционами"


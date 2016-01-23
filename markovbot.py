from flask import Flask
from flask_slack import Slack
from slacker import Slacker
import markovify
from datetime import datetime
import re
import json
import os

#get api configuration file
confLoc = os.path.join(os.path.dirname(__file__), 'api.conf')
with open(confLoc) as conf_file:
	apiconf = json.load(conf_file)

app = Flask(__name__);
slack = Slack(app);
slacker = Slacker(apiconf['slack']['api-key'])

def getCorpora(user):
	username = user['name']
	search = slacker.search.messages(query="from:@"+username, count=100)
	corpora = ''
	if(search.body['ok']):
		for m in search.body['messages']['matches']:
			corpora += m['text']+'\n'

	return corpora
		

app.add_url_rule('/', view_func=slack.dispatch)
teamid = apiconf['slack']['teamid']
tok = apiconf['slack']['token']

@slack.command('marcovbot', token=tok,
		team_id=teamid, methods=['POST'])
@slack.command('markovbot', token=tok,
		team_id=teamid, methods=['POST'])
@slack.command('Markovbot', token=tok,
		team_id=teamid, methods=['POST'])
@slack.command('MarkovBot', token=tok,
		team_id=teamid, methods=['POST'])
def markov(**kwargs):
	starttime = datetime.now()
	user_id = re.search('<@(.*)>', kwargs.get('text')).group(1)
	user = slacker.users.info(user=user_id).body['user']
	corp = getCorpora(user)
	if(corp == ''):
		return slack.response("No messages found for user " + user)

	text_model = markovify.Text(corp)
	resp = ''
	for i in range(3):
		sentence = text_model.make_sentence(tries=100)
		if(sentence):
			resp += sentence + " "
	endtime = datetime.now()
	deltatime = endtime - starttime
	return slack.response(resp + "\n[Generated in " 
		+ "{0:.2f}".format(deltatime.total_seconds() * 1000) + " milliseconds.]")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=2109, debug=True)

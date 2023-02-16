import openai
import config
openai.api_key = config.OPENAI_API_KEY

def openAIQuery(query,temp,chars,engine):
	"Queries the OpenAI Api, providing the query,temperature and characters"
	response = openai.Completion.create(
		engine=engine,
		prompt=query,
		temperature=float(temp),
		max_tokens=int(chars),
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)

	if 'choices' in response:
		if len(response['choices']) > 0:
			answer = response['choices'][0]['text']
		else:
			answer = 'Opps sorry, you beat the AI this time'
	else:
		answer = 'Opps sorry, you beat the AI this time'
	return answer
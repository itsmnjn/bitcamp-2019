import sys
# Imports the Google Cloud client library
from google.cloud import translate
from googleapiclient.discovery import build

# Instantiates a client
translate_client = translate.Client()

def result():
	# The text to translate
	text = sys.argv[1]
	# The target language
	target = sys.argv[2]

	# Translates some text into Russian
	translation = translate_client.translate(
		text,
		target_language=target)
	return(translation['translatedText'])
if __name__=='__main__':
	print(result())
	
import sys
# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()


def translate(text, target):
    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)
    return(translation['translatedText'])


if __name__ == '__main__':
    # The text to translate
    text = sys.argv[1]
    # The target language
    target = sys.argv[2]
    print(translate(text, target))

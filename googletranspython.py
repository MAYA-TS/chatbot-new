import six
from google.cloud import translate_v2 as translate
import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "chatbot-324803-1209b8da248f.json"

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\356286\\Desktop\\chatbotfinal\\mafil-aidujv-25a0238a560c.json"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\grep\\Desktop\\flaskProject\\mafil-aidujv-25a0238a560c.json"
translator = translate.Client()
def googletransfn(text,tar_len="en"):

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translator.translate(text, target_language=tar_len)

    return result["translatedText"]

from flask import Flask, render_template
import sys
from datetime import datetime
import os
import json
import zeep
from sqlalchemy.orm import sessionmaker, session
from flask_cors import CORS
from googletranspython import googletransfn
from flask import Flask, make_response, jsonify, request
from complaintnextaction import complaintnextaction
from cards import cardsnextaction
from sessionChecking import chatSessionService, saveMetaData, sessionmakerfun
from nextActionService import nextAction
from otherVerticlesNextActionService import otherVerticalnextAction
from NlpController import get_response_from_dialogflow, create_response_from_nlp
from Models import ChatLogs, SessionData, ChatContexts, GlInquiry, Branchs, OvInquiry,CBInquiry,Complaints

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C://App//flaskProject//mafil-aidujv-aidujv-25a0238a560c.json"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\grep\\Desktop\\flaskProject\\mafil-aidujv-25a0238a560c.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\356286\\Desktop\\chatbotfinal\\mafil-aidujv-25a0238a560c.json"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\356286\\PycharmProjects\\chatbot\\mafil-aidujv-25a0238a560c.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "chatbot-324803-1209b8da248f.json"

wsdl = "https://online.manappuram.com/custbot/custbot.asmx?WSDL"
client = zeep.Client(wsdl=wsdl)

# session = sessionmakerfun()

project_id = 'chatbot-324803'
language_code = 'en-US'

app = Flask(__name__)


CORS(app)


@app.route("/")
def index():
    return render_template('index.html')



@app.route('/api/processInput', methods=['GET', 'POST'])
def process_input():
    try:

        # print(session)

        if request.method=='POST':
            details = request.form
            input_data = details['inputData']
            session_id = details['sessionid']
            matadata1 = details['metaData']
        elif request.method=='GET':
            print(request)
            input_data = request.args.get('inputData')
            session_id = request.args.get('sessionid')
            print(session_id)
            matadata1 = request.args.get('metaData')
        # print(input_data)
        mdata = json.loads(matadata1)

        complaints=Complaints()
        gl_enquiry = GlInquiry()
        chat_logs = ChatLogs()
        session_data = SessionData()
        cb_inquiry=CBInquiry()
        chat_logs.CL_SESSION_ID = session_id
        # CL_ORG_INPUT_DATA = input_data;
        chat_logs.CL_INPUT_DATA = input_data
        chat_logs.CL_ORG_INPUT_DATA = input_data
        chat_logs.CL_TIMESTAMP = datetime.now()
        chat_logs.CL_CREATED_DATE = datetime.now()
        chat_logs.VERSION = 0
        # session_data = chatSessionService(chat_logs.CL_SESSION_ID)
        # session_id=''
        try:
            if session_id!='':
                session_data = chatSessionService(session_id)
            else:
                session_id = request.args.get('sessionid')
                session_data = chatSessionService(session_id)
        except:
            chat_response = dict(responseType="Text", responseText="", responseAction="", suggestions=[], branches=[],
                                 pledges=[])
            chat_response["responseType"] = 'Text'
            chat_response[
                'responseText'] = "Apologies for the inconvience, please elaborate your concern by calling -18004202233, they can assist you better"
            chat_response["responseText2"]=''
            # session_data.SD_NEXT_ACTION = None


        saveMetaData(session_data, mdata)
        # lan_name_of_input = googletransfn(input_data)
        #
        # #print(lan_name_of_input.src)Sorry! I didn't get it. Please try again.
        # if lan_name_of_input.src != 'en':
        #     input_data_tran = googletransfn(input_data,'en')
        #
        #
        #     input_data = input_data_tran.text

        chat_logs.CL_INPUT_DATA = input_data




        if (chat_logs.CL_ORG_INPUT_DATA != "VGFrZSBtZSBob21l") and (session_data.SD_NEXT_ACTION != None) :
            if (chat_logs.CL_ORG_INPUT_DATA=="Other verticals enquiry") or (chat_logs.CL_ORG_INPUT_DATA== "Start the flow again for other verticals") or (chat_logs.CL_ORG_INPUT_DATA=="Continue the flow for other verticals") or (chat_logs.CL_ORG_INPUT_DATA=="Apply gold loan") or (chat_logs.CL_ORG_INPUT_DATA=='Switch to Gold Loan') or (chat_logs.CL_ORG_INPUT_DATA=='Start the flow again for gold loan') or (chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan') or (chat_logs.CL_ORG_INPUT_DATA=='Switch to other loan'):
                chat_response=cardsnextaction(chat_logs,session_data)
            elif str(session_data.SD_NEXT_ACTION).startswith('other'):
                chat_response = otherVerticalnextAction(chat_logs, session_data)
            # elif str(session_data.SD_NEXT_ACTION).startswith('complaint'):

            #     chat_response = complaintnextaction(chat_logs,session_data)
            else:
                chat_response = nextAction(chat_logs, session_data,cb_inquiry)
        else:
            response = get_response_from_dialogflow(project_id, session_id, input_data, language_code)
            if response =='Apologies for the inconvience, please elaborate your concern by calling -18004202233, they can assist you better':
                chat_response = dict(responseType="Text", responseText="", responseAction="", suggestions=[],suggestions2=[],                                     branches=[],
                                     pledges=[])
                chat_response["responseType"] = 'Text'
                chat_response[
                    'responseText'] = response
                chat_response["responseText2"]=''


            else:

                chat_logs.CL_OUTPUT_DATA = response.query_result.fulfillment_text
                chat_logs.CL_ACTION = session_data.SD_NEXT_ACTION
                chat_logs.CL_TIMESTAMP = datetime.now()
                chat_logs.CL_INTENT_ID = response.query_result.intent.name
                chat_logs.CL_INTENT_NAME = response.query_result.intent.display_name
                if chat_logs.CL_INTENT_NAME == 'welcome_intent':
                    session = sessionmakerfun()
                    session.add(chat_logs)
                    try:
                        session.commit()

                    except:
                        session.rollback()
                else:
                    session = sessionmakerfun()
                    session.add(chat_logs)
                # print(response.query_result.intent)
                if len(str(response.query_result.intent)) != 0:
                    chat_response = create_response_from_nlp(chat_logs, session_data)
                else:
                    chat_response = create_response_from_nlp(chat_logs, session_data)
            session = sessionmakerfun()
            session.add(chat_logs)
            try:
                session.commit()
            except:
                session.rollback()
        return chat_response
    except :
        print(sys.exc_info())
        print("Exception is " , sys.exc_info()[0])
        session.rollback()
    # except:
    #     session_id = request.args.get('sessionid')
    #     session_id = ''
    #     matadata1 = request.args.get('metaData')

    #     mdata = json.loads(matadata1)
    #     session_data = chatSessionService(session_id)
    #     saveMetaData(session_data,mdata)
    #     chat_response = dict(responseType="Text", responseText="", responseAction="", suggestions=[], branches=[],
    #                          pledges=[])
    #     chat_response["responseType"] = 'Text'
    #     chat_response['responseText'] = "Apologies for the inconvience, please elaborate your concern by calling -18004202233, they can assit you better"
    #     session_data.SD_NEXT_ACTION = None
    #     session = sessionmakerfun()
    #     session.add(session_data)
    #     try:
    #         session.commit()
    #     except:
    #         session.rollback()


if __name__ == '__main__':
    app.run()


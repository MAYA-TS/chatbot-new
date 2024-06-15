from datetime import datetime
# from sqlalchemy.orm import sessionmaker, session
import dialogflow_v2 as dialogflow
from sqlalchemy import select, create_engine, table
from sqlalchemy import MetaData
import math, random
import requests
from Models import SessionData, ChatLanguages, Branchs, GlInquiry, FAQS, FAQResponses, OvInquiry,Complaints
from otherVerticallist import verticalList
import zeep
import json
from sessionChecking import chatSessionService, saveMetaData,sessionmakerfun
from suggestionService import suggestion_array_fun,suggestion_array_fun2
from branch import branch_details_pincode, branch_details_loc
from googletranspython import googletransfn
from ssid import create_UUID
from glvertical import goldverticalList
from complaintlist import yesorno
# session = sessionmakerfun()

wsdl = "https://online.manappuram.com/custbot/custbot.asmx?WSDL"
client = zeep.Client(wsdl=wsdl)

def get_response_from_dialogflow(project_id, session_id, input_data, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    # print("1")
    # session = sessionmakerfun()
    try:
        session_client = dialogflow.SessionsClient()
        # print("2")
        session = session_client.session_path(project_id, session_id)
        # print("3")
        text_input = dialogflow.types.TextInput(
            text=input_data, language_code=language_code)
        # print("4")
        query_input = dialogflow.types.QueryInput(text=text_input)
        # print("5")
        # print("query input",query_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        # print("6")
        # print(response)
        # print('r')
    except:

        response = "Apologies for the inconvience, please elaborate your concern by calling -18004202233, they can assit you better"
        # session_data.SD_NEXT_ACTION = None

    return response


def create_response_from_nlp(chat_logs, session_data):
    # chatSessionService(session_data.SD_SESSION_ID)

    # print("reached response section")
    session = sessionmakerfun()
    chat_lang = session.query(ChatLanguages).filter(ChatLanguages.CG_ID_PK == session_data.CG_ID_FK).all();

    chat_d = ChatLanguages()

    if len(chat_lang) == 0:

        chat_d.CG_ID_PK = 1
    else:

        chat_d = chat_lang[0]
    suggestion_array = []

    chat_response = dict(responseType="Text", responseText="", responseAction="", suggestions=[], branches=[], pledges=[])

    chat_response["responseType"] = 'Text'
    output_data_tran = googletransfn(chat_logs.CL_ORG_INPUT_DATA)


    # org_lang = output_data_tran.src

    # if chat_d.CG_LANG_CODE != 'en':
    #     output_data_tran1 = translator.translate(chat_logs.CL_OUTPUT_DATA, dest=chat_d.CG_LANG_CODE)
    #
    #     output_data = output_data_tran1.text
    output_data=chat_logs.CL_OUTPUT_DATA

    chat_response["responseText"] = output_data
    chat_response["responseText2"]=''

    chat_response["responseAction"] = chat_logs.CL_INTENT_NAME

    # try:
    if chat_logs.CL_INPUT_DATA == 'Pledge Details':

        chat_response["responseText"] = googletransfn(
            'Please provide your registered mobile number for authentication',
            chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        chat_response["responseAction"] = ''
        session_data.SD_NEXT_ACTION = "customer_pledge_details_api"
        session = sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
    elif chat_logs.CL_INPUT_DATA == "Call Back":

        session_data.SD_NEXT_ACTION = "customer_call_back_method"
        session = sessionmakerfun()

        session.add(session_data);
        try:
            session.commit()
        except:
            session.rollback()
        suggestion_array = suggestion_array_fun(chat_d)
        # chat_response["suggestions"] = suggestion_array

        chat_response["responseText"] = "Please enter your number"
        chat_response["responseText2"]=''

    elif chat_logs.CL_INPUT_DATA == "Pay Gold Loan Interest":

        session_data.SD_NEXT_ACTION = None
        session = sessionmakerfun()

        session.add(session_data);
        try:
            session.commit()
        except:
            session.rollback()
        suggestion_array = suggestion_array_fun(chat_d)
        chat_response["suggestions"] = suggestion_array

        chat_response["responseText"] = "To pay your gold loan interest click here  :<br>" + "<a  href = 'https://online.manappuram.com/eservice.aspx' target='_blank'>Online Payment</a>"
        chat_response["responseText2"]=''



    elif chat_logs.CL_INTENT_NAME == "welcome_intent":

        chat_response["responseType"] = 'Text'

        suggestion_array = []

        suggestion_array = suggestion_array_fun(chat_d)

        suggestion_array2=suggestion_array_fun2(chat_d)

        # print(suggestion_array)
        chat_response["suggestions"] = suggestion_array

        chat_response["suggestions2"] = suggestion_array2

        chat_response["responseText"] = googletransfn("Welcome Mira",chat_d.CG_LANG_CODE)

        chat_response["responseText2"] = googletransfn("Say hello to a world where every conversation feels natural, engaging, and smarter. Always ready to elevate your chats to a whole new level",chat_d.CG_LANG_CODE)

        session_data.SD_NEXT_ACTION = None

        session = sessionmakerfun()
        session.add(session_data)

        try:
            session.commit()
        except:
            # print("error")
            session.rollback()
            session = sessionmakerfun()
            session.add(session_data)
            session.commit()

    elif str(chat_logs.CL_INTENT_NAME).startswith('FAQ'):

        try:
            faq_master = FAQS()
            faq_res = FAQResponses()
            session = sessionmakerfun()
            faq_result = session.query(FAQS).filter(FAQS.FQ_INTENT_NAME == chat_logs.CL_INTENT_NAME).all();

            faq_master = faq_result[0]
            if faq_master.FQ_INTEGRATION_FLAG == 1:
                if faq_master.FQ_INTEGRATION_METHOD == "getLTV":
                    with client.settings(raw_response=True):
                        res = client.service.getLTV()
                        a = res.content.decode("utf-8")
                        b = json.loads(a.split('<')[0])
                        chat_response["responseText"] = "Today's LTV is  " + str(b.get("lnd_rate"))+" per gram"
                        chat_response["responseText2"]=''

            elif faq_master.FQ_INTEGRATION_FLAG == 0:
                faq_res_result = session.query(FAQResponses).filter((FAQResponses.FQ_ID_FK == faq_master.FQ_ID_PK) and
                                                                (FAQResponses.CG_ID_FK == 1)).all();
                faq_res = faq_res_result[0]
                chat_response["responseText"] = googletransfn(str(faq_res.FR_RESPONSE),
                                                                 chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
        except:
            chat_response["responseText"] = googletransfn('Could not find an answer for that. Please try again.', chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
        session_data.SD_NEXT_ACTION = None
        session = sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()

    elif chat_logs.CL_INTENT_NAME == "apply_gl":

        if chat_logs.CL_INPUT_DATA == 'xyz':

            chat_response["responseText"] = googletransfn(
                'Please provide your registered mobile number for authentication',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            session_data.SD_NEXT_ACTION = "customer_pledge_details_api"
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()

        else:
            chat_response["responseText"] = googletransfn(
                'Select the type of gold loan you are looking for',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            chat_response['suggestions'] = goldverticalList()

            gl_enquiry = GlInquiry()
            gl_enquiry.SD_ID_FK = session_data.SD_ID_PK
            gl_enquiry.GL_IS_MOBILE_VERIFIED = 0
            gl_enquiry.GL_IS_BRANCH_CONFIRMED = 0
            gl_enquiry.GL_CREATED_DATE = datetime.now()
            gl_enquiry.GL_LOAN_AMOUNT=0
            # other_enquiry.TB_ID_FK = 0
            gl_enquiry.VERSION = 0
            session_data.SD_TRAN_TYPE = 'GL'
            session_data.SD_TRAN_ID = gl_enquiry.GL_ID_PK
            session_data.SD_NEXT_ACTION = "gold_Enter loan amount"
            session = sessionmakerfun()

            session.add(gl_enquiry);
            session.commit()
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            session.commit()

            # gl_enquiry = GlInquiry()

            # gl_enquiry.SD_ID_FK = session_data.SD_ID_PK
            # gl_enquiry.GL_IS_MOBILE_VERIFIED = 0
            # gl_enquiry.GL_IS_BRANCH_CONFIRMED = 0
            # gl_enquiry.GL_LOAN_AMOUNT = 0
            # gl_enquiry.GL_CREATED_DATE = datetime.now()
            # gl_enquiry.version = 0
            # # gl_enquiry.TB_ID_FK = 0
            # #gl_enquiry.VERSION = 0
            # session_data.SD_TRAN_TYPE = 'GL'
            # session_data.SD_TRAN_ID = gl_enquiry.GL_ID_PK
            # chat_response["responseText"] = googletransfn('Please provide the loan amount you wish to avail',
            #                                                      chat_d.CG_LANG_CODE)
            # chat_response["responseAction"] = 'Enter loan amount'
            # session_data.SD_NEXT_ACTION = "get_full_name"
            # session = sessionmakerfun()
            # session.add(session_data)
            # session.commit()
            # session = sessionmakerfun()
            # session.add(gl_enquiry)
            # session.commit()

    elif chat_logs.CL_INTENT_NAME == "change_language":

        suggestion_array = []
        session = sessionmakerfun()
        chat_lang = session.query(ChatLanguages).all();
        n = len(chat_lang)
        for i in range(0, n):
            ch_lang_data = chat_lang[i]
            reg_text=googletransfn(ch_lang_data.CG_LANG_NAME_EN,ch_lang_data.CG_LANG_CODE)
            # if ch_lang_data.CG_LANG_NAME_EN == 'Hindi':
            # 	suggestion = dict(suggestionText='हिन्दी',suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
            # else:
            # 	suggestion = dict(suggestionText=reg_text,suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
            if ch_lang_data.CG_LANG_NAME_EN == 'Hindi':
                suggestion=dict(suggestionText='हिन्दी',suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
            else:
                suggestion=dict(suggestionText=reg_text,suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
            suggestion_array.append(suggestion)
        chat_response['suggestions'] = suggestion_array
        session_data.SD_NEXT_ACTION = "gold_Set_language"
        chat_response["responseText"] = googletransfn('Please select the desired language.',
                                                         chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(session_data)

        try:
            session.commit()
        except:
            session.rollback()
    # elif chat_logs.CL_INTENT_NAME == "Pay Gold Loan Interest":
    #     session_data.SD_NEXT_ACTION = None
    #     session.add(session_data);
    #     try:
    #         session.commit()
    #     except:
    #         session.rollback()
    #
    #     chat_response[
    #         "responseText"] = " Pay Your Gold loan interest at  :<br>" + "<a  href = 'https://www.manappuram.com/branchlocator/' target='_blank'>https://www.manappuram.com/branchlocator/<br>feedback.html</a>"



    elif chat_logs.CL_INTENT_NAME == "nearest_branch":
        session_data.SD_NEXT_ACTION = None
        session = sessionmakerfun()
        session.add(session_data);
        try:
            session.commit()
        except:
            session.rollback()

        chat_response["responseText"] = " Locate Your nearest branch at  :<br>" + "<a  href = 'https://www.manappuram.com/branchlocator/' target='_blank'>LocateBranch<br></a>"
        chat_response["responseText2"]=''
        suggestion_array = suggestion_array_fun(chat_d)
        chat_response["suggestions"] = suggestion_array
        # LATITUDE = session_data.SD_LATITUDE
        # LONGITUDE = session_data.SD_LONGITUDE
        #
        # suggestion_array = branch_details_loc(LATITUDE, LONGITUDE)
        # session_data.SD_NEXT_ACTION = None
        # session.add(session_data);
        # try:
        #     session.commit()
        # except:
        #     session.rollback()
        # chat_response["responseText"] = googletransfn('Nearest Branches', chat_d.CG_LANG_CODE)
        #
        # chat_response["branches"] = suggestion_array

    elif chat_logs.CL_INTENT_NAME == "default_fallback":
        # print("type", chat_logs.CL_INTENT_NAME)
        if chat_logs.CL_INPUT_DATA == "VGFrZSBtZSBob21l":

            suggestion_array = []
            suggestion_array = suggestion_array_fun(chat_d)
            session_data.SD_NEXT_ACTION = None
            session = sessionmakerfun()
            session_data.SD_SESSION_ID=create_UUID()
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()

            chat_response["responseText"] = googletransfn("Hi, I am Mira. How can i help you today?",
                                                                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["suggestions"] = suggestion_array
        elif chat_logs.CL_INPUT_DATA == "Report an issue":
            
            # suggestion_array = suggestion_array_fun(chat_d)
            chat_response["suggestions"] = yesorno()

            chat_response["responseText"] = "Customers can register"+"<a  href = 'https://www.manappuram.com/feedback' target='_blank'>Complaint</a>"+" / Feedback options are available by calling 18004202233"
            chat_response["responseText2"]=''

            # session_data.SD_NEXT_ACTION = "complaint_product"
            # complaints=Complaints()
            # complaints.SD_ID_FK= session_data.SD_ID_PK
            # complaints.COMPLAINT_DATE=datetime.now()
            # session_data.SD_TRAN_TYPE = 'CL'
            # session_data.SD_TRAN_ID = complaints.CL_ID_PK
            # session = sessionmakerfun()
            # session.add(complaints);
            # try:
            #     session.commit()
            # except:
            #     session.rollback()
            session_data.SD_NEXT_ACTION=None
            suggestion_array = suggestion_array_fun(chat_d)
            chat_response["suggestions"] = suggestion_array
            
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            try:
                session.commit()
            except:
                session.rollback()
            
            
        elif chat_logs.CL_INPUT_DATA == "voiceOptionSelectedVOS":

            session_data.SD_NEXT_ACTION = None
            session = sessionmakerfun()

            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()

            chat_response["responseText"] = "Your voice is not clear.Please try again."
            chat_response["responseText2"]=''

        elif chat_logs.CL_INPUT_DATA == "Other verticals enquiry":
            # print("into other vertcal")
            chat_response["responseText"] = googletransfn(
                'Select the vertical you are looking for',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            chat_response['suggestions'] = verticalList()

            other_enquiry = OvInquiry()
            other_enquiry.SD_ID_FK = session_data.SD_ID_PK
            other_enquiry.OV_IS_MOBILE_VERIFIED = 0
            other_enquiry.OV_CREATED_DATE = datetime.now()
            # other_enquiry.TB_ID_FK = 0
            other_enquiry.VERSION = 0
            session_data.SD_TRAN_TYPE = 'OV'
            session_data.SD_TRAN_ID = other_enquiry.OV_ID_PK
            session_data.SD_NEXT_ACTION = "other_vertical_list"
            session = sessionmakerfun()

            session.add(other_enquiry);
            session.commit()
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            session.commit()
            # except:
            #     session.rollback()




    # except :
    #     chat_response["responseText"] = googletransfn("Apologies for the inconvience, please elaborate your concern by calling -18004202233, they can assit you better.",
    #                                                          chat_d.CG_LANG_CODE)
    #     session_data.SD_NEXT_ACTION = None
    #     session.add(session_data);
    #     try:
    #         session.commit()
    #     except:
    #         session.rollback()



    return chat_response






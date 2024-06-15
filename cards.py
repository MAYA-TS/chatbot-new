from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker, session
from sessionChecking import chatSessionService, saveMetaData,sessionmakerfun
from Models import SessionData, ChatLanguages, Branchs, GlInquiry, FAQS, FAQResponses,CBInquiry,Complaints,OvInquiry
from otpService import generateOTP
from complaintlist import card_selection_other_same,card_selection_other,card_selection_gold_same,card_selection_gold
from otherVerticallist import verticalList
from glvertical import goldverticalList
from nextActionService import nextAction
from otherVerticlesNextActionService import otherVerticalnextAction
import zeep
import json
import requests
import re
from suggestionService import suggestion_array_fun
from branch import branch_details_pincode, branch_details_loc
from googletranspython import googletransfn
from ssid import create_UUID

def cardsnextaction(chat_logs,session_data):
    cb_inquiry=CBInquiry()
    suggestion_array = []
    branches_array = []
    chat_response = dict(responseType="Text", responseText="", responseAction="", suggestions=[], branches=[],
                         pledges=[])
    chat_response["responseType"] = 'Text'
    session = sessionmakerfun()
    chat_lang = session.query(ChatLanguages).filter(ChatLanguages.CG_ID_PK == session_data.CG_ID_FK).all();
    try:
        chat_d = chat_lang[0]
        session_data.CG_ID_FK = chat_d.CG_ID_PK
        chat_response["responseType"] = 'Text'
        # translator.translate('Language changed to ' + str(chat_d.CG_LANG_NAME_EN),  chat_d.CG_LANG_CODE)
        chat_response["responseText"] = googletransfn('PLease try again in ' + str(chat_d.CG_LANG_NAME_EN),
                                                             chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        chat_response["responseAction"] = ''
    except:
        session_data.CG_ID_FK = 1

    if (chat_logs.CL_ORG_INPUT_DATA == 'Other verticals enquiry') and (session_data.SD_NEXT_ACTION).startswith('other'):
        # session = sessionmakerfun()
        # session_data.SD_NEXT_ACTION = 'other_cards_confirmation'
        # session=sessionmakerfun()
        # session.add(session_data);
        # try:
        #     session.commit()
        # except:
        #     session.rollback()
        chat_response["suggestions"] = card_selection_other_same()
        chat_response["responseText"] = googletransfn('Do you need to start from beggining or continue?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
    elif chat_logs.CL_ORG_INPUT_DATA == 'Start the flow again for other verticals':
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
    elif chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for other verticals' :
        chat_response=otherVerticalnextAction(chat_logs,session_data)
    elif (chat_logs.CL_ORG_INPUT_DATA=='Apply gold loan') and (session_data.SD_NEXT_ACTION).startswith('other'):
        chat_response["suggestions"] = card_selection_other()
        chat_response["responseText"] = googletransfn('Do you need to start from beggining or continue?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
    elif chat_logs.CL_ORG_INPUT_DATA=='Switch to Gold Loan':
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
    elif (chat_logs.CL_ORG_INPUT_DATA=='Apply gold loan') and (session_data.SD_NEXT_ACTION).startswith('gold'):
        chat_response["suggestions"] = card_selection_gold_same()
        chat_response["responseText"] = googletransfn('Do you need to start from beggining or continue?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''

    elif chat_logs.CL_ORG_INPUT_DATA=='Start the flow again for gold loan':
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
    elif chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan':
        chat_response=nextAction(chat_logs, session_data,cb_inquiry)
    elif chat_logs.CL_ORG_INPUT_DATA=='Other verticals enquiry' and (session_data.SD_NEXT_ACTION).startswith('gold'):
        
        chat_response["suggestions"] = card_selection_gold()
        chat_response["responseText"] = googletransfn('Do you need to start from beggining or continue?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
    elif chat_logs.CL_ORG_INPUT_DATA=='Switch to other loan':
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


    return chat_response

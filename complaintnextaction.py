from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker, session
from sessionChecking import chatSessionService, saveMetaData,sessionmakerfun
from Models import SessionData, ChatLanguages, Branchs, GlInquiry, FAQS, FAQResponses,CBInquiry,Complaints
from otpService import generateOTP
from complaintlist import category,feedback,manappuram_detail,service_rating
import zeep
import json
import requests
import re
from suggestionService import suggestion_array_fun
from branch import branch_details_pincode, branch_details_loc
from googletranspython import googletransfn
from ssid import create_UUID

def complaintnextaction(chat_logs,session_data):
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
        chat_response["responseText"] = googletransfn('PLease try again ' + str(chat_d.CG_LANG_NAME_EN),
                                                             chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        chat_response["responseAction"] = ''
    except:
        session_data.CG_ID_FK = 1

    if session_data.SD_NEXT_ACTION == 'complaint_product':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.CUSTOMER_YN=chat_logs.CL_ORG_INPUT_DATA
        session_data.SD_NEXT_ACTION = 'complaint_product_category'
        session=sessionmakerfun()
        session.add(session_data);
        try:
            session.commit()
        except:
            session.rollback()
        chat_response["suggestions"] = category()
        chat_response["responseText"] = googletransfn('Please select the product category',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION == 'complaint_product_category':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.PRODUCT_CATEGORY=chat_logs.CL_ORG_INPUT_DATA
        session_data.SD_NEXT_ACTION = 'complaint_branch_name'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        chat_response["responseType"]='text'
        chat_response["responseText"] = googletransfn('Please specify the name of the branch visited',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_branch_name':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.BRANCH_NAME=chat_logs.CL_ORG_INPUT_DATA
        session_data.SD_NEXT_ACTION = 'complaint_staff_dtl'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        chat_response["suggestions"] = feedback()
        chat_response["responseText"] = googletransfn('Were the staffs ready to help?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_staff_dtl':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.STAFF_DTL=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_overall_service'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        chat_response["suggestions"] = feedback()
        chat_response["responseText"] = googletransfn('Are you happy with the overall service provided by Manappuram Finance Limited?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_overall_service':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.OVERALL_SERVICE=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_mprm_dtl'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        chat_response["suggestions"] = manappuram_detail()
        chat_response["responseText"] = googletransfn('How did you hear about Manappuram Finance Limited?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_mprm_dtl':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.MPRM_DTL=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_service_rtng'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        chat_response["suggestions"] = service_rating()
        chat_response["responseText"] = googletransfn('How would you rate our service?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_service_rtng':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.SRVC_RTNG=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_feedback'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        # chat_response["suggestions"] = service_rating()
        chat_response["responseText"] = googletransfn('Please type in a short feedback',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()
    
    elif session_data.SD_NEXT_ACTION =='complaint_feedback':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.FEEDBACK=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_suggestions'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        # chat_response["suggestions"] = service_rating()
        chat_response["responseText"] = googletransfn('Type in a few improvement suggestions',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()
    
    elif session_data.SD_NEXT_ACTION =='complaint_suggestions':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.SUGGESTIONS=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_name'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        # chat_response["suggestions"] = service_rating()
        chat_response["responseText"] = googletransfn('Kindly provide your name',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_name':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.CUST_NAME=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_phone'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        # chat_response["suggestions"] = service_rating()
        chat_response["responseText"] = googletransfn('Kindly provide your phone number?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_phone':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.CUST_PHONE=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_email'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        # chat_response["suggestions"] = service_rating()
        chat_response["responseText"] = googletransfn('Kindly provide your email address?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_email':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.CUST_EMAIL=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = 'complaint_address'
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        # chat_response["suggestions"] = service_rating()
        chat_response["responseText"] = googletransfn('Kindly provide your residential address?',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION =='complaint_address':
        session = sessionmakerfun()
        result1 = session.query(Complaints).filter(Complaints.SD_ID_FK == session_data.SD_ID_PK).all()
        last_row = len(result1)
        if last_row ==0:
            last_row=1
        complaints = result1[last_row-1]
        complaints.CUST_ADDRESS=chat_logs.CL_ORG_INPUT_DATA    
        session_data.SD_NEXT_ACTION = None
        session_data.SD_SESSION_ID=create_UUID()
        session=sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
        # chat_response["suggestions"] = service_rating()
        chat_response["responseText"] = googletransfn('We have received your feedback.A customer care Executive will contact you shortly.',
                                                                chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        chat_response["responseAction"] = ''
        suggestion_array = suggestion_array_fun(chat_d)
        chat_response["suggestions"] = suggestion_array


        session = sessionmakerfun()
        session.add(complaints)
        try:
            session.commit()
        except:
            session.rollback()




    return chat_response
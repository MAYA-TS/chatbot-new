from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker, session
from sessionChecking import chatSessionService, saveMetaData,sessionmakerfun
from Models import SessionData, ChatLanguages, Branchs, GlInquiry, FAQS, FAQResponses,CBInquiry
from otpService import generateOTP
from glvertical import goldverticalList
import zeep
import json
import requests
import re
from suggestionService import suggestion_array_fun
from branch import branch_details_pincode, branch_details_loc
from googletranspython import googletransfn
from ssid import create_UUID

wsdl = "https://online.manappuram.com/custbot/custbot.asmx?WSDL"
client = zeep.Client(wsdl=wsdl)
# session = sessionmakerfun()
def nextAction(chat_logs, session_data,cb_inquiry):
    # print("into nextAction loop")
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

    if session_data.SD_NEXT_ACTION == 'gold_get_full_name':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan':
            # session = sessionmakerfun()
            # result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            # last_row = len(result1)
            # if last_row ==0:
            #     last_row=1
            # gl_enquiry = result1[last_row-1]
            # gl_enquiry.GL_TYPE=chat_logs.CL_ORG_INPUT_DATA
            # gl_enquiry.SD_ID_FK = session_data.SD_ID_PK
            # gl_enquiry.GL_IS_MOBILE_VERIFIED = 0
            # gl_enquiry.GL_IS_BRANCH_CONFIRMED = 0
            # gl_enquiry.GL_LOAN_AMOUNT = 0
            # gl_enquiry.GL_CREATED_DATE = datetime.now()
            # gl_enquiry.version = 0
            # gl_enquiry.TB_ID_FK = 0
            #gl_enquiry.VERSION = 0
            session_data.SD_TRAN_TYPE = 'GL'
            # session_data.SD_TRAN_ID = gl_enquiry.GL_ID_PK
            if chat_logs.CL_ORG_INPUT_DATA=='Door Step Gold Loan':
                chat_response["responseText"] = googletransfn('We offer service for you to avail gold loans at your door step ! The advantages of this service include: <br> 👉Convenience <br> 👉Quick Processing <br>👉Free Insurance Coverage <br>To apply for DSGL,Please provide the loan amount you wish to avail',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
            elif chat_logs.CL_ORG_INPUT_DATA=='Online Gold Loan':
                chat_response["responseText"] = googletransfn('👉Safelock your Gold Ornaments at your nearest Manappuram Branch <br> 👉Register for Online Gold Loan services and link your savings bank account <br> 👉Get the loan amount credited to your bank account anytime using our mobile app or website <br> To apply for OGL,Please provide the loan amount you wish to avail',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
            else:
                chat_response["responseText"] = googletransfn('Please provide the loan amount you wish to avail',
                                                            chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
            chat_response["responseAction"] = 'Enter loan amount'
            session_data.SD_NEXT_ACTION = "gold_get_full_name"
            session = sessionmakerfun()
            session.add(session_data)
            session.commit()
            # session = sessionmakerfun()
            # session.add(gl_enquiry)
            # session.commit()
        else:
            session = sessionmakerfun()
            result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            last_row = len(result1)
            if last_row ==0:
                last_row=1
            gl_enquiry = result1[last_row-1]
            try:
                if int(chat_logs.CL_ORG_INPUT_DATA) > 0:
                    gl_enquiry.GL_LOAN_AMOUNT = chat_logs.CL_ORG_INPUT_DATA
                    session_data.SD_NEXT_ACTION = "gold_Enter Phone number"
                    session = sessionmakerfun()
                    session.add(session_data);
                    try:
                        session.commit()
                    except:
                        session.rollback()
                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = googletransfn('Please provide your full name',
                                                                        chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''
                    session = sessionmakerfun()
                    session.add(gl_enquiry)
                    try:
                        session.commit()
                    except:
                        session.rollback()

                else:
                    session_data.SD_NEXT_ACTION = "gold_get_full_name"
                    session = sessionmakerfun()
                    session.add(session_data);
                    try:
                        session.commit()
                    except:
                        session.rollback()
                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = googletransfn('Please enter valid loan amount',
                                                                        chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''
                    session = sessionmakerfun()

                    session.add(session_data)
                    try:
                        session.commit()
                    except:
                        session.rollback()
            except ValueError:
                session_data.SD_NEXT_ACTION = "gold_get_full_name"
                session = sessionmakerfun()

                session.add(session_data);
                try:
                    session.commit()
                except:
                    session.rollback()
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('Please enter valid loan amount',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                session = sessionmakerfun()

                session.add(session_data)
                try:
                    session.commit()
                except:
                    session.rollback()
    
    elif session_data.SD_NEXT_ACTION == 'gold_Enter loan amount' :
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan':
            session_data.SD_NEXT_ACTION = "gold_Enter loan amount"
            session = sessionmakerfun()
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()
            chat_response["responseText"] = googletransfn(
                'Select the type of gold loan you are looking for',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            chat_response['suggestions'] = goldverticalList()
            

            # gl_enquiry = GlInquiry()
            # gl_enquiry.SD_ID_FK = session_data.SD_ID_PK
            # gl_enquiry.GL_IS_MOBILE_VERIFIED = 0
            # gl_enquiry.GL_IS_BRANCH_CONFIRMED = 0
            # gl_enquiry.GL_CREATED_DATE = datetime.now()
            # gl_enquiry.GL_LOAN_AMOUNT=0
            # # other_enquiry.TB_ID_FK = 0
            # gl_enquiry.VERSION = 0
            # session_data.SD_TRAN_TYPE = 'GL'
            # session_data.SD_TRAN_ID = gl_enquiry.GL_ID_PK
            # session_data.SD_NEXT_ACTION = "Enter loan amount"
            # session = sessionmakerfun()

            # session.add(gl_enquiry);
            # session.commit()
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            session.commit()
        else:
            # gl_enquiry = GlInquiry()
            session = sessionmakerfun()
            result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            last_row = len(result1)
            if last_row ==0:
                last_row=1
            gl_enquiry = result1[last_row-1]
            gl_enquiry.GL_TYPE=chat_logs.CL_ORG_INPUT_DATA
            gl_enquiry.SD_ID_FK = session_data.SD_ID_PK
            gl_enquiry.GL_IS_MOBILE_VERIFIED = 0
            gl_enquiry.GL_IS_BRANCH_CONFIRMED = 0
            gl_enquiry.GL_LOAN_AMOUNT = 0
            gl_enquiry.GL_CREATED_DATE = datetime.now()
            gl_enquiry.version = 0
            # gl_enquiry.TB_ID_FK = 0
            #gl_enquiry.VERSION = 0
            session_data.SD_TRAN_TYPE = 'GL'
            session_data.SD_TRAN_ID = gl_enquiry.GL_ID_PK
            if chat_logs.CL_ORG_INPUT_DATA=='Door Step Gold Loan':
                chat_response["responseText"] = googletransfn('<p>We offer service for you to avail gold loans at your door step ! The advantages of this service include: <br> 👉Convenience <br> 👉Quick Processing <br>👉Free Insurance Coverage <br>To apply for DSGL,Please provide the loan amount you wish to avail</p>',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                chat_response["responseAction"] = 'Enter loan amount'
                session_data.SD_NEXT_ACTION = "gold_get_full_name"
                session = sessionmakerfun()
                session.add(session_data)
                session.commit()
                session = sessionmakerfun()
                session.add(gl_enquiry)
                session.commit()
            elif chat_logs.CL_ORG_INPUT_DATA=='Online Gold Loan':
                chat_response["responseText"] = googletransfn('<p>👉Safelock your Gold Ornaments at your nearest Manappuram Branch <br> 👉Register for Online Gold Loan services and link your savings bank account <br> 👉Get the loan amount credited to your bank account anytime using our mobile app or website <br> To apply for OGL,Please provide the loan amount you wish to avail</p>',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                chat_response["responseAction"] = 'Enter loan amount'
                session_data.SD_NEXT_ACTION = "gold_get_full_name"
                session = sessionmakerfun()
                session.add(session_data)
                session.commit()
                session = sessionmakerfun()
                session.add(gl_enquiry)
                session.commit()
            elif chat_logs.CL_ORG_INPUT_DATA=='Gold Loan':
                chat_response["responseText"] = googletransfn('Please provide the loan amount you wish to avail',
                                                            chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                chat_response["responseAction"] = 'Enter loan amount'
                session_data.SD_NEXT_ACTION = "gold_get_full_name"
                session = sessionmakerfun()
                session.add(session_data)
                session.commit()
                session = sessionmakerfun()
                session.add(gl_enquiry)
                session.commit()
            else:
                session_data.SD_NEXT_ACTION = "gold_Enter loan amount"
                session = sessionmakerfun()
                session.add(session_data);
                try:
                    session.commit()
                except:
                    session.rollback()
                chat_response["responseText"] = googletransfn(
                    'Select the type of gold loan you are looking for',
                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''

                chat_response['suggestions'] = goldverticalList()

    elif session_data.SD_NEXT_ACTION == 'gold_Enter Phone number':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan':
            session_data.SD_NEXT_ACTION = "gold_Enter Phone number"
            session = sessionmakerfun()
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn('Please provide your full name',
                                                                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
        else:
            session = sessionmakerfun()
            result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            last_row = len(result1)
            if last_row == 0:
                last_row = 1
            gl_enquiry = result1[last_row - 1]
            if re.search("^[A-z][A-z|\.|\s]+$", chat_logs.CL_ORG_INPUT_DATA)!=None:

                gl_enquiry.GL_CUSTOMER_NAME = chat_logs.CL_ORG_INPUT_DATA
                session = sessionmakerfun()
                session.add(gl_enquiry)
                try:
                    session.commit()
                except:
                    session.rollback()

                session_data.SD_NEXT_ACTION = "gold_Enter OTP"
                session = sessionmakerfun()

                session.add(session_data);
                try:
                    session.commit()
                except:
                    session.rollback()
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    'Please provide your 10 digit mobile number for authentication',  chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
            else:
                session_data.SD_NEXT_ACTION = "gold_Enter Phone number"
                session = sessionmakerfun()
                session.add(session_data);
                try:
                    session.commit()
                except:
                    session.rollback()
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('Please enter correct name',
                                                            chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                session = sessionmakerfun()

                session.add(session_data)
                try:
                    session.commit()
                except:
                    session.rollback()

    elif session_data.SD_NEXT_ACTION == 'gold_Enter OTP':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan':
            session_data.SD_NEXT_ACTION = "gold_Enter OTP"
            session = sessionmakerfun()

            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn(
                'Please provide your 10 digit mobile number for authentication',  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

        else:
            if (len(chat_logs.CL_ORG_INPUT_DATA) == 10)and(re.compile("[5-9][0-9]{9}").match(chat_logs.CL_ORG_INPUT_DATA)):

                session = sessionmakerfun()
                result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
                last_row = len(result1)
                if last_row == 0:
                    last_row = 1
                gl_enquiry = result1[last_row - 1]
                gl_enquiry.GL_MOBILE_NO = chat_logs.CL_ORG_INPUT_DATA
                OTP = generateOTP()
                gl_enquiry.GL_MOBILE_OTP = OTP
                r = requests.get("http://bankalerts.sinfini.com/api/web2sms.php?workingkey=A2bbf78715947e342f970537bfd8bd62d&sender=MAFILD&to=" + str(gl_enquiry.GL_MOBILE_NO) + "&message= Dear user, your one time password is " + str(OTP) + ". Manappuram&type=xml")
                session = sessionmakerfun()
                session.add(gl_enquiry)
                try:
                    session.commit()
                except:
                    session.rollback()
                session_data.SD_NEXT_ACTION = "gold_Enter email ID"
                session = sessionmakerfun()
                session.add(session_data)
                try:
                    session.commit()
                except:
                    session.rollback()
                chat_response["responseType"] = 'Text'
                suggestion_array = []
                suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                                suggestionInput="Resend OTP")
                suggestion_array.append(suggestions)

                suggestions = dict(suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                                suggestionInput="Change Phone Number")
                suggestion_array.append(suggestions)
                chat_response['suggestions'] = suggestion_array
                chat_response["responseText"] = googletransfn(
                    'Great! Please enter the valid OTP sent to your mobile number.',
                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                chat_response["responseType"] = 'Text'

            else:
                chat_response["responseText"] = googletransfn(
                    'Please enter valid mobile number.',
                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                session_data.SD_NEXT_ACTION = 'gold_Enter OTP'
                session = sessionmakerfun()
                session.add(session_data)
                try:
                    session.commit()
                except:
                    session.rollback()

    elif session_data.SD_NEXT_ACTION == 'gold_Enter email ID':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan':
            chat_response["responseText"] = googletransfn(
                'Please enter valid mobile number.',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            session_data.SD_NEXT_ACTION = 'gold_Enter OTP'
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()
        else:

            if chat_logs.CL_INPUT_DATA == 'Resend OTP':
                session = sessionmakerfun()
                result2 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
                last_row = len(result2)
                if last_row == 0:
                    last_row = 1
                gl_enquiry = result2[last_row - 1]
                OTP = generateOTP()
                gl_enquiry.GL_MOBILE_OTP = OTP
                r = requests.get(
                    "http://bankalerts.sinfini.com/api/web2sms.php?workingkey=A2bbf78715947e342f970537bfd8bd62d&sender=MAFILD&to=" + str(
                        gl_enquiry.GL_MOBILE_NO) + "&message= Dear user, your one time password is " + str(OTP) + ". Manappuram&type=xml")
                session = sessionmakerfun()
                session.add(gl_enquiry)
                try:
                    session.commit()

                except:
                    session.rollback()
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    'Please enter the valid OTP sent to your mobile number',
                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                suggestion_array = []
                suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                                suggestionInput="Resend OTP")
                suggestion_array.append(suggestions)

                suggestions = dict(
                    suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                    suggestionInput="Change Phone Number")
                suggestion_array.append(suggestions)
                chat_response['suggestions'] = suggestion_array
                session_data.SD_NEXT_ACTION = 'gold_Enter email ID'
                session = sessionmakerfun()
                session.add(session_data)
                try:
                    session.commit()

                except:
                    session.rollback()

            elif chat_logs.CL_INPUT_DATA == "Change Phone Number":
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    'Please provide your 10 digit mobile number for authentication',  chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                session_data.SD_NEXT_ACTION = 'gold_Enter OTP'
                session = sessionmakerfun()
                session.add(session_data)
                session.commit()

            else:
                try:
                    session = sessionmakerfun()
                    result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
                    last_row = len(result1)
                    if last_row == 0:
                        last_row = 1
                    gl_enquiry = result1[last_row - 1]
                    if gl_enquiry.GL_MOBILE_OTP ==  int(chat_logs.CL_ORG_INPUT_DATA):
                        chat_response["responseType"] = 'Text'
                        chat_response["responseText"] = googletransfn(
                            'Your mobile authentication process is complete.Please provide the language that you prefer for call back',
                            chat_d.CG_LANG_CODE)
                        chat_response["responseText2"]=''
                        chat_response["responseAction"] = ''
                        suggestion_array = []
                        # suggestions = dict(
                        #     suggestionText=googletransfn("I don't have an Email",  chat_d.CG_LANG_CODE),
                        #     suggestionInput="Skip email")
                        # suggestion_array.append(suggestions)

                        chat_lang = session.query(ChatLanguages).all();
                        n = len(chat_lang)
                        for i in range(0, n - 1):
                            ch_lang_data = chat_lang[i]
                            print(ch_lang_data.CG_LANG_CODE)
                            reg_text = googletransfn(ch_lang_data.CG_LANG_NAME_EN,  ch_lang_data.CG_LANG_CODE)
                            # suggestion = dict(suggestionText=reg_text,suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
                            if ch_lang_data.CG_LANG_NAME_EN == 'Hindi':
                                suggestion = dict(suggestionText='हिन्दी', suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
                            else:
                                suggestion = dict(suggestionText=reg_text, suggestionInput=ch_lang_data.CG_LANG_NAME_EN)

                            suggestion_array.append(suggestion)





                    ##suggestion = dict(suggestionText=ch_lang_data.CG_LANG_NAME,
                            ##                  suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
                            ##suggestion_array.append(suggestion)
                #	 suggestions = dict(
                        #   suggestionText=googletransfn("English", chat_d.CG_LANG_CODE),
                        #   suggestionInput="English")
                    # suggestion_array.append(suggestions)
                    # suggestions = dict(
                    #     suggestionText=googletransfn("Malayalam", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Malayalam")
                    # suggestion_array.append(suggestions)

                    # suggestions = dict(
                    #     suggestionText=googletransfn("Tamil", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Tamil")
                    # suggestion_array.append(suggestions)
                    # suggestions = dict(
                    #     suggestionText=googletransfn("Kannada", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Kannada")
                        #suggestion_array.append(suggestions)
                    # suggestions = dict(
                    #     suggestionText=googletransfn("Telugu", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Telugu")
                    # suggestion_array.append(suggestions)
                    # suggestions = dict(
                    #     suggestionText=googletransfn("Hindi.", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Hindi.")
                    # suggestion_array.append(suggestions)
                    # suggestions = dict(
                    #     suggestionText=googletransfn("Marathi", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Marathi")
                    # suggestion_array.append(suggestions)
                    # suggestions = dict(
                    #     suggestionText=googletransfn("Odiya", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Odiya")
                    # suggestion_array.append(suggestions)

                    # suggestions = dict(
                    #     suggestionText=googletransfn("Bengali", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Bengali")
                    # suggestion_array.append(suggestions)

                    # suggestions = dict(
                    #     suggestionText=googletransfn("Assamese", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Assamese")
                    # suggestion_array.append(suggestions)

                    # suggestions = dict(
                    #     suggestionText=googletransfn("Punjabi", chat_d.CG_LANG_CODE),
                    #     suggestionInput="Punjabi")
                    # suggestion_array.append(suggestions)

                        chat_response['suggestions'] = suggestion_array
                        session_data.SD_NEXT_ACTION = 'gold_Enter location or nearest branch'
                        gl_enquiry.GL_IS_MOBILE_VERIFIED = 1
                        session = sessionmakerfun()
                        session.add(gl_enquiry)
                        try:
                            session.commit()
                        except:
                            session.rollback()
                        session = sessionmakerfun()
                        session.add(session_data)
                        try:
                            session.commit()
                        except:
                            session.rollback()
                    else:
                        chat_response["responseType"] = 'Text'
                        chat_response["responseText"] = googletransfn('Invalid OTP. Please re enter',  chat_d.CG_LANG_CODE)
                        chat_response["responseText2"]=''
                        suggestion_array = []
                        suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                                        suggestionInput="Resend OTP")
                        suggestion_array.append(suggestions)

                        suggestions = dict(
                            suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                            suggestionInput="Change Phone Number")
                        suggestion_array.append(suggestions)
                        chat_response['suggestions'] = suggestion_array
                        session_data.SD_NEXT_ACTION = 'gold_Enter email ID'
                        session = sessionmakerfun()
                        session.add(session_data)
                        try:
                            session.commit()
                        except:
                            session.rollback()
                except:
                    session_data.SD_NEXT_ACTION = "gold_Enter email ID"
                    session = sessionmakerfun()

                    session.add(session_data);
                    try:
                        session.commit()
                    except:
                        session.rollback()
                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = googletransfn('Please enter valid OTP',
                                                                        chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''
                    session = sessionmakerfun()

                    session.add(session_data)
                    try:
                        session.commit()
                    except:
                        session.rollback()

    elif session_data.SD_NEXT_ACTION == 'gold_Enter location or nearest branch':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan':
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn(
                'Your mobile authentication process is complete.Please provide the language that you prefer for call back',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            suggestion_array = []
            # suggestions = dict(
            #     suggestionText=googletransfn("I don't have an Email",  chat_d.CG_LANG_CODE),
            #     suggestionInput="Skip email")
            # suggestion_array.append(suggestions)

            chat_lang = session.query(ChatLanguages).all();
            n = len(chat_lang)
            for i in range(0, n - 1):
                ch_lang_data = chat_lang[i]
                print(ch_lang_data.CG_LANG_CODE)
                reg_text = googletransfn(ch_lang_data.CG_LANG_NAME_EN,  ch_lang_data.CG_LANG_CODE)
                # suggestion = dict(suggestionText=reg_text,suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
                if ch_lang_data.CG_LANG_NAME_EN == 'Hindi':
                    suggestion = dict(suggestionText='हिन्दी', suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
                else:
                    suggestion = dict(suggestionText=reg_text, suggestionInput=ch_lang_data.CG_LANG_NAME_EN)

                suggestion_array.append(suggestion)

            chat_response['suggestions'] = suggestion_array
            session_data.SD_NEXT_ACTION = 'gold_Enter location or nearest branch'
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()

        else:

            if chat_logs.CL_INPUT_DATA == 'Skip email':
                session_data.SD_NEXT_ACTION = "gold_selection_of_branch"
                session = sessionmakerfun()
                session.add(session_data);
                try:
                    session.commit()
                except:
                    session.rollback()
                suggestion_array = []
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('How do you want select the branch?',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''

                suggestions = dict(suggestionText=googletransfn("PIN CODE",  chat_d.CG_LANG_CODE),
                                suggestionInput="Search using Pincode")
                suggestion_array.append(suggestions)

                # suggestions = dict(suggestionText=googletransfn("LOCATION",  chat_d.CG_LANG_CODE),
                #                    suggestionInput="Search using Location")
                # suggestion_array.append(suggestions)
                chat_response['suggestions'] = suggestion_array

                # try:
                #     session.commit()
                # except:
                #     session.rollback()
            elif chat_logs.CL_ORG_INPUT_DATA in['English','Malayalam','Tamil','Kannada','Telugu','Hindi']:
                # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                # if re.search(regex, chat_logs.CL_ORG_INPUT_DATA):
                session = sessionmakerfun()
                result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
                session_data.SD_NEXT_ACTION = 'gold_selection_of_branch'
                last_row = len(result1)
                if last_row == 0:
                    last_row = 1
                gl_enquiry = result1[last_row - 1]
                gl_enquiry.GL_EMAIL_ID = chat_logs.CL_ORG_INPUT_DATA
                session = sessionmakerfun()
                session.add(gl_enquiry)
                try:
                    session.commit()
                except:
                    session.rollback()
                session = sessionmakerfun()
                session.add(session_data)
                try:
                    session.commit()
                except:
                    session.rollback()
                suggestion_array = []
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('How do you want select the branch?',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''

                suggestions = dict(suggestionText=googletransfn("PIN CODE",  chat_d.CG_LANG_CODE),
                                suggestionInput="Search using Pincode")
                suggestion_array.append(suggestions)
                chat_response['suggestions'] = suggestion_array
            else:
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    'Please provide the language that you prefer for call back',
                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                suggestion_array = []
                # suggestions = dict(
                #     suggestionText=googletransfn("I don't have an Email",  chat_d.CG_LANG_CODE),
                #     suggestionInput="Skip email")
                # suggestion_array.append(suggestions)

                chat_lang = session.query(ChatLanguages).all();
                n = len(chat_lang)
                for i in range(0, n - 1):
                    ch_lang_data = chat_lang[i]
                    print(ch_lang_data.CG_LANG_CODE)
                    reg_text = googletransfn(ch_lang_data.CG_LANG_NAME_EN,  ch_lang_data.CG_LANG_CODE)
                    # suggestion = dict(suggestionText=reg_text,suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
                    if ch_lang_data.CG_LANG_NAME_EN == 'Hindi':
                        suggestion = dict(suggestionText='हिन्दी', suggestionInput=ch_lang_data.CG_LANG_NAME_EN)
                    else:
                        suggestion = dict(suggestionText=reg_text, suggestionInput=ch_lang_data.CG_LANG_NAME_EN)

                    suggestion_array.append(suggestion)

                chat_response['suggestions'] = suggestion_array
                session_data.SD_NEXT_ACTION = 'gold_Enter location or nearest branch'
                session = sessionmakerfun()
                session.add(session_data)
                try:
                    session.commit()
                except:
                    session.rollback()
                    

    elif session_data.SD_NEXT_ACTION == 'gold_selection_of_branch':

        if chat_logs.CL_INPUT_DATA == 'Search using Pincode':
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn("Please enter your pincode",  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            session_data.SD_NEXT_ACTION = 'gold_pin_code_action'

        elif chat_logs.CL_INPUT_DATA == "Search using Location":
            LATITUDE = session_data.SD_LATITUDE
            LONGITUDE = session_data.SD_LONGITUDE


            suggestion_array=branch_details_loc(LATITUDE,LONGITUDE)

            chat_response["responseType"] = 'Text'

            chat_response["responseText"] = googletransfn('Nearest Branches',  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["branches"] = suggestion_array
            session_data.SD_NEXT_ACTION = 'gold_Final_in_gl'
        else:
            suggestion_array = []
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn('How do you want select the branch?',
                                                                  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            suggestions = dict(suggestionText=googletransfn("PIN CODE",  chat_d.CG_LANG_CODE),
                               suggestionInput="Search using Pincode")
            suggestion_array.append(suggestions)
            #
            # suggestions = dict(suggestionText=googletransfn("LOCATION",  chat_d.CG_LANG_CODE),
            #                    suggestionInput="Search using Location")
            # suggestion_array.append(suggestions)
            chat_response['suggestions'] = suggestion_array
            session_data.SD_NEXT_ACTION = 'gold_selection_of_branch'
        session = sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()

    elif session_data.SD_NEXT_ACTION == 'gold_pin_code_action':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for gold loan':
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn("Please enter your pincode",  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            session_data.SD_NEXT_ACTION = 'gold_pin_code_action'
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()
        else:
            if (re.compile("^[0-9]").match(chat_logs.CL_ORG_INPUT_DATA)) and (len(chat_logs.CL_ORG_INPUT_DATA)==6):
                suggestion_array = branch_details_pincode(chat_logs.CL_ORG_INPUT_DATA)
                # print(suggestion_array)
                chat_response["suggestions"] = suggestion_array

                if len(suggestion_array) != 0:
                    session_data.SD_NEXT_ACTION = 'gold_Final_in_gl'
                    chat_response["responseText"] = googletransfn("Nearest Branches",  chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''

                else:
                    suggestion_array = []
                    session_data.SD_NEXT_ACTION = 'gold_selection_of_branch'
                    suggestions = dict(suggestionText=googletransfn("PIN CODE",  chat_d.CG_LANG_CODE),
                                    suggestionInput="Search using Pincode")
                    suggestion_array.append(suggestions)

                    # suggestions = dict(suggestionText=googletransfn("LOCATION",  chat_d.CG_LANG_CODE),
                    #                    suggestionInput="Search using Location")
                    # suggestion_array.append(suggestions)
                    chat_response['suggestions'] = suggestion_array
                    chat_response["responseText"] = googletransfn('Could not found any branch on this location. How do you want select the branch?',
                                                                        chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                session = sessionmakerfun()
                session.add(session_data);
                session.commit()

            else:
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn("Please enter your pincode",  chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                session_data.SD_NEXT_ACTION = 'gold_pin_code_action'


    elif session_data.SD_NEXT_ACTION == 'gold_Final_in_gl':
        try:

            # if type(int(chat_logs.CL_ORG_INPUT_DATA)) == int:
            if type(str(chat_logs.CL_ORG_INPUT_DATA)) == str:
                session = sessionmakerfun()
                # branchess = session.query(Branchs).filter(Branchs.TB_BRANCH_CODE == chat_logs.CL_ORG_INPUT_DATA).all();
                branchess = session.query(Branchs).filter(Branchs.TB_BRANCH_NAME == chat_logs.CL_ORG_INPUT_DATA).all();
                n = len(branchess)
                bran = branchess[0]
                if n != 0:
                    session = sessionmakerfun()
                    result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
                    last_row = len(result1)
                    if last_row == 0:
                        last_row = 1
                    gl_enquiry = result1[last_row - 1]
                    # gl_enquiry.TB_ID_FK = chat_logs.CL_ORG_INPUT_DATA
                    gl_enquiry.TB_ID_FK = bran.TB_BRANCH_CODE

                    session_data.SD_NEXT_ACTION = 'gold_new_gl_confirm'
                    session = sessionmakerfun()
                    session.add(session_data);
                    try:
                        session.commit()

                    except:
                        session.rollback()
                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = str(googletransfn('You have selected ', chat_d.CG_LANG_CODE)) + " "+str(bran.TB_BRANCH_NAME)+" "+str(googletransfn(' branch. Please confirm the branch',
                                                                          chat_d.CG_LANG_CODE))
                    chat_response["responseText2"]=''
                    # chat_response["responseAction"] = ''
                    suggestion_array = []
                    suggestions = dict(suggestionText=googletransfn("Confirm",  chat_d.CG_LANG_CODE),
                                       suggestionInput="ok")
                    suggestion_array.append(suggestions)

                    suggestions = dict(
                        suggestionText=googletransfn("Reselect Branch",  chat_d.CG_LANG_CODE),
                        suggestionInput="reselect")
                    suggestion_array.append(suggestions)
                    chat_response['suggestions'] = suggestion_array
                    session = sessionmakerfun()
                    session.add(gl_enquiry)
                    try:
                        session.commit()

                    except:
                        session.rollback()
                else:
                    session_data.SD_NEXT_ACTION = "gold_selection_of_branch"
                    session = sessionmakerfun()
                    session.add(session_data);
                    try:
                        session.commit()

                    except:
                        session.rollback()
                    suggestion_array = []
                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = googletransfn(
                        'Sorry, Please try again. How do you want select the branch?',
                         chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''

                    suggestions = dict(suggestionText=googletransfn("PIN CODE",  chat_d.CG_LANG_CODE),
                                       suggestionInput="Search using Pincode")
                    suggestion_array.append(suggestions)

                    # suggestions = dict(suggestionText=googletransfn("LOCATION",  chat_d.CG_LANG_CODE),
                    #                    suggestionInput="Search using Location")
                    # suggestion_array.append(suggestions)
                    chat_response['suggestions'] = suggestion_array
                    session = sessionmakerfun()
                    session.add(session_data)
                    try:
                        session.commit()

                    except:
                        session.rollback()
        except:
            session_data.SD_NEXT_ACTION = "gold_selection_of_branch"
            session = sessionmakerfun()
            session.add(session_data);
            try:
                session.commit()

            except:
                session.rollback()

            suggestion_array = []
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn('Sorry, Please try again. How do you want select the branch?',
                                                                  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            suggestions = dict(suggestionText=googletransfn("PIN CODE",  chat_d.CG_LANG_CODE),
                               suggestionInput="Search using Pincode")
            suggestion_array.append(suggestions)

            # suggestions = dict(suggestionText=googletransfn("LOCATION",  chat_d.CG_LANG_CODE),
            #                    suggestionInput="Search using Location")
            # suggestion_array.append(suggestions)
            chat_response['suggestions'] = suggestion_array

            session_data.SD_NEXT_ACTION = 'gold_Enter location or nearest branch'
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()

            except:
                session.rollback()

    elif session_data.SD_NEXT_ACTION == 'gold_new_gl_confirm':
        if chat_logs.CL_ORG_INPUT_DATA == "ok":
            session = sessionmakerfun()
            result1 = session.query(GlInquiry).filter(GlInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            last_row = len(result1)
            if last_row == 0:
                last_row = 1
            gl_enquiry = result1[last_row - 1]
            gl_enquiry.GL_IS_BRANCH_CONFIRMED = 1
            mobileNO = gl_enquiry.GL_MOBILE_NO
            customerName = gl_enquiry.GL_CUSTOMER_NAME
            branchCode = gl_enquiry.TB_ID_FK
            with client.settings(raw_response=True):
                res = client.service.GetLMSData(mobileNO,customerName,branchCode)
                a = res.content.decode("utf-8")
                b = json.loads(a.split('<')[0])
                if b.get("status") == "111":
                    leadId = b.get("leadID")
                else:
                    leadId = ''
                gl_enquiry.LEAD_ID = leadId
            gl_enquiry.GL_CREATED_DATE=datetime.now();
            session = sessionmakerfun()
            session.add(gl_enquiry)
            try:
                session.commit()
            except:
                session.rollback()
            session_data.SD_NEXT_ACTION = None
            session = sessionmakerfun()
            session_data.SD_SESSION_ID=create_UUID()
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn(
                "Thanks for your interest in Manappuram. One of our executive will contact you shortly.",
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            suggestion_array = suggestion_array_fun(chat_d)
            chat_response["suggestions"] = suggestion_array

        elif chat_logs.CL_ORG_INPUT_DATA == "reselect":
            session_data.SD_NEXT_ACTION = "gold_selection_of_branch"
            session = sessionmakerfun()
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()
            suggestion_array = []
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn('How do you want select the branch?',
                                                                  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            suggestions = dict(suggestionText=googletransfn("PIN CODE",  chat_d.CG_LANG_CODE),
                               suggestionInput="Search using Pincode")
            suggestion_array.append(suggestions)

            # suggestions = dict(suggestionText=googletransfn("LOCATION",  chat_d.CG_LANG_CODE),
            #                    suggestionInput="Search using Location")
            # suggestion_array.append(suggestions)
            chat_response['suggestions'] = suggestion_array
        else:
            session_data.SD_NEXT_ACTION = 'gold_new_gl_confirm'
            session.add(session_data);

            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn('Please confirm the branch',
                                                                  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            suggestion_array = []
            suggestions = dict(suggestionText=googletransfn("Confirm",  chat_d.CG_LANG_CODE),
                               suggestionInput="ok")
            suggestion_array.append(suggestions)

            suggestions = dict(
                suggestionText=googletransfn("Reselect Branch",  chat_d.CG_LANG_CODE),
                suggestionInput="reselect")
            suggestion_array.append(suggestions)
            chat_response['suggestions'] = suggestion_array

    elif session_data.SD_NEXT_ACTION == 'gold_Set_language':
        # print("into set language")
        session_data.SD_NEXT_ACTION = None
        session = sessionmakerfun()
        chat_lang = session.query(ChatLanguages).filter(ChatLanguages.CG_LANG_NAME_EN == chat_logs.CL_INPUT_DATA).all();
        try:
            chat_d = chat_lang[0]
            session_data.CG_ID_FK = chat_d.CG_ID_PK
            chat_response["responseType"] = 'Text'
            # googletransfn('Language changed to ' + str(chat_d.CG_LANG_NAME_EN),  chat_d.CG_LANG_CODE)
            chat_response["responseText"] = googletransfn('Language changed to ' + str(chat_d.CG_LANG_NAME_EN),
                                                                  chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
        except:
            session_data.CG_ID_FK = 1
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = 'Language changed to English'
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
        suggestion_array = suggestion_array_fun(chat_d)
        chat_response["suggestions"] = suggestion_array
        # print("After changing language", session_data.CG_ID_FK)
        session = sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()
    elif session_data.SD_NEXT_ACTION == 'gold_customer_pledge_details_api':
        # if len(chat_logs.CL_ORG_INPUT_DATA) == 10:
        if (len(chat_logs.CL_ORG_INPUT_DATA) == 10)and(re.compile("[5-9][0-9]{9}").match(chat_logs.CL_ORG_INPUT_DATA)):

            session_data.SD_MOBILE_NO = chat_logs.CL_ORG_INPUT_DATA
            OTP = generateOTP()
            session_data.SD_MOB_OTP = OTP
            r = requests.get(
               "http://bankalerts.sinfini.com/api/web2sms.php?workingkey=A2bbf78715947e342f970537bfd8bd62d&sender=MAFILD&to=" + str(
                   session_data.SD_MOBILE_NO) + "&message= Dear user, your one time password is " + str(OTP) + ". Manappuram&type=xml")
            session = sessionmakerfun()
            session.add(session_data)
            session.commit()
            session_data.SD_NEXT_ACTION = "gold_customer_pledge_details_api_otp_ver"
            session = sessionmakerfun()
            session.add(session_data);
            session.commit()
            chat_response["responseType"] = 'Text'
            suggestion_array = []
            suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                               suggestionInput="Resend OTP")
            suggestion_array.append(suggestions)

            suggestions = dict(
                suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                suggestionInput="Change Phone Number")
            suggestion_array.append(suggestions)
            chat_response['suggestions'] = suggestion_array
            chat_response["responseText"] = googletransfn(
                'Great! Please enter the OTP sent to your mobile number.',
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
        else:
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn(
                'Please enter a valid mobile number.',
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            session_data.SD_NEXT_ACTION = 'gold_customer_pledge_details_api'
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()

    elif session_data.SD_NEXT_ACTION == 'gold_customer_pledge_details_api_otp_ver':

        if chat_logs.CL_INPUT_DATA == 'Resend OTP':
            OTP = generateOTP()
            session_data.SD_MOB_OTP = OTP
            r = requests.get(
               "http://bankalerts.sinfini.com/api/web2sms.php?workingkey=A2bbf78715947e342f970537bfd8bd62d&sender=MAFILD&to=" + str(
                   session_data.SD_MOBILE_NO) + "&message= Dear user, your one time password is " + str(OTP) + ". Manappuram&type=xml")

            chat_response["responseType"] = 'Text'
            suggestion_array = []
            suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                               suggestionInput="Resend OTP")
            suggestion_array.append(suggestions)

            suggestions = dict(
                suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                suggestionInput="Change Phone Number")
            suggestion_array.append(suggestions)
            chat_response['suggestions'] = suggestion_array
            chat_response["responseText"] = googletransfn(
                'Please enter the OTP sent to your mobile number.',
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            session_data.SD_NEXT_ACTION = 'gold_customer_pledge_details_api_otp_ver'
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()

        elif chat_logs.CL_INPUT_DATA == "Change Phone Number":

            chat_response["responseText"] = googletransfn(
                'Please provide your 10 digit mobile number for authentication',
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            session_data.SD_NEXT_ACTION = "gold_customer_pledge_details_api"
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()

        else:
            # print(session_data.SD_MOB_OTP)
            session_data.SD_CUSTOMER_NAME = chat_logs.CL_INPUT_DATA;
            session_data.SD_IS_MOBILE_VERIFIED = 0;

            try:

                if session_data.SD_MOB_OTP == chat_logs.CL_INPUT_DATA:
                    chat_response["responseText"] = googletransfn(
                        'PLedge Details',
                         chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''
                    session_data.SD_NEXT_ACTION = None
                    # mobileNO = 7780700259
                    # print(type(mobileNO))
                    # print(type(int(session_data.SD_MOBILE_NO)))
                    suggestion_array = []
                    with client.settings(raw_response=True):
                        # print("mobile no", session_data.SD_MOBILE_NO)
                        res = client.service.GetPledges(session_data.SD_MOBILE_NO)
                        # res = client.service.GetPledges(mobileNO)
                        # print(res)
                        a = res.content.decode("utf-8")
                        # print(a)
                        b = json.loads(a.split('<')[0])
                        # print(b)
                        if b.get("status") == "111":
                            for i in b.get('pledgelst'):
                                with client.settings(raw_response=True):
                                    res1 = client.service.GetPledgeDetails(i.get('pledgeNo'))
                                    aa = res1.content.decode("utf-8")
                                    bb = json.loads(aa.split('<')[0])
                                    # print(bb)
                                    if bb.get("status") == "111":
                                        pledges = dict(pledgeCd=bb.get('pldgno'),
                                                       totalAmount=bb.get('toatalstlmt'),
                                                       dueDate=bb.get('duedt'),
                                                       renewalDate=bb.get('renewaldt'),
                                                       action=""
                                                       )
                                        suggestion_array.append(pledges)
                            chat_response['pledges'] = suggestion_array
                            chat_response["responseText"] = googletransfn(
                                'Pledge details found with this phone number are ',
                                 chat_d.CG_LANG_CODE)
                            chat_response["responseText2"]=''
                            # print(chat_response['pledges'])

                        else:
                            chat_response["responseText"] = googletransfn(
                                'No pledge details found with this phone number',
                                 chat_d.CG_LANG_CODE)
                            chat_response["responseText2"]=''
                            chat_response["responseAction"] = ''
                            suggestion_array = suggestion_array_fun(chat_d)
                            chat_response["suggestions"] = suggestion_array
                            session_data.SD_NEXT_ACTION = None
                            session = sessionmakerfun()
                            session_data.SD_SESSION_ID=create_UUID()
                            session.add(session_data)
                            session.commit()
                            # session.commit()

                else:
                    suggestion_array = []
                    suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                                       suggestionInput="Resend OTP")
                    suggestion_array.append(suggestions)

                    suggestions = dict(
                        suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                        suggestionInput="Change Phone Number")
                    suggestion_array.append(suggestions)
                    chat_response['suggestions'] = suggestion_array
                    chat_response["responseText"] = googletransfn(
                        'Invalid OTP, Please retry',
                         chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    session_data.SD_NEXT_ACTION = 'gold_customer_pledge_details_api_otp_ver'
                    session = sessionmakerfun()
                    session.add(session_data)
                    session.commit()
            except:
                suggestion_array = []
                suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                                   suggestionInput="Resend OTP")
                suggestion_array.append(suggestions)

                suggestions = dict(
                    suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                    suggestionInput="Change Phone Number")
                suggestion_array.append(suggestions)
                chat_response['suggestions'] = suggestion_array
                chat_response["responseText"] = googletransfn(
                    'Invalid OTP, Please retry',
                     chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                session_data.SD_NEXT_ACTION = 'gold_customer_pledge_details_api_otp_ver'
                session = sessionmakerfun()
                session.add(session_data)
                session.commit()
    elif session_data.SD_NEXT_ACTION == 'gold_customer_call_back_method':
        session=sessionmakerfun()
        cb_inquiry.SD_ID_FK=session_data.SD_ID_PK
        cb_inquiry.CB_CREATED_DATE=datetime.now()
        cb_inquiry.CB_IS_MOBILE_VERIFIED='0'
        session.add(cb_inquiry)
        session.commit()
        # if len(chat_logs.CL_ORG_INPUT_DATA) == 10:
        if (len(chat_logs.CL_ORG_INPUT_DATA) == 10)and(re.compile("[5-9][0-9]{9}").match(chat_logs.CL_ORG_INPUT_DATA)):

            session_data.SD_MOBILE_NO = chat_logs.CL_ORG_INPUT_DATA
            OTP = generateOTP()
            result1 = session.query(CBInquiry).filter(CBInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            last_row = len(result1)
            if last_row == 0:
                last_row = 1
            cb_inquiry = result1[last_row - 1]
            cb_inquiry.CB_MOBILE_OTP=OTP
            cb_inquiry.CB_MOBILE_NUMBER=chat_logs.CL_ORG_INPUT_DATA
            session=sessionmakerfun()
            session.add(cb_inquiry)
            session.commit
            session_data.SD_MOB_OTP = OTP
            r = requests.get(
               "http://bankalerts.sinfini.com/api/web2sms.php?workingkey=A2bbf78715947e342f970537bfd8bd62d&sender=MAFILD&to=" + str(
                   session_data.SD_MOBILE_NO) + "&message= Dear user, your one time password is " + str(OTP) + ". Manappuram&type=xml")
            session = sessionmakerfun()
            session.add(session_data)
            session_data.SD_NEXT_ACTION = "gold_customer_call_back_method_otp_veri"
            session = sessionmakerfun()
            session.add(session_data);
            session.commit()
            chat_response["responseType"] = 'Text'
            suggestion_array = []
            suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                               suggestionInput="Resend OTP")
            suggestion_array.append(suggestions)

            suggestions = dict(
                suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                suggestionInput="Change Phone Number")
            suggestion_array.append(suggestions)
            chat_response['suggestions'] = suggestion_array
            chat_response["responseText"] = googletransfn(
                'Great! Please enter the OTP sent to your mobile number.',
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
        else:
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn(
                'Please enter a valid mobile number.',
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            session_data.SD_NEXT_ACTION = 'gold_customer_call_back_method'
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()

    elif session_data.SD_NEXT_ACTION == 'gold_customer_call_back_method_otp_veri':

        if chat_logs.CL_INPUT_DATA == 'Resend OTP':
            OTP = generateOTP()
            session_data.SD_MOB_OTP = OTP
            session = sessionmakerfun()
            result1 = session.query(CBInquiry).filter(CBInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            last_row = len(result1)
            if last_row == 0:
                last_row = 1
            cb_inquiry = result1[last_row - 1]
            cb_inquiry.CB_MOBILE_OTP=OTP
            session.add(cb_inquiry)
            session.commit()
            r = requests.get(
               "http://bankalerts.sinfini.com/api/web2sms.php?workingkey=A2bbf78715947e342f970537bfd8bd62d&sender=MAFILD&to=" + str(
                   session_data.SD_MOBILE_NO) + "&message= Dear user, your one time password is " + str(OTP) + ". Manappuram&type=xml")

            chat_response["responseType"] = 'Text'
            suggestion_array = []
            suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                               suggestionInput="Resend OTP")
            suggestion_array.append(suggestions)

            suggestions = dict(
                suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                suggestionInput="Change Phone Number")
            suggestion_array.append(suggestions)
            chat_response['suggestions'] = suggestion_array
            chat_response["responseText"] = googletransfn(
                'Please enter the OTP sent to your mobile number.',
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            session_data.SD_NEXT_ACTION = 'gold_customer_call_back_method_otp_veri'
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()

        elif chat_logs.CL_INPUT_DATA == "Change Phone Number":

            chat_response["responseText"] = googletransfn(
                'Please provide your 10 digit mobile number for authentication',
                 chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            session_data.SD_NEXT_ACTION = "gold_customer_call_back_method"
            session = sessionmakerfun()
            session.add(session_data)
            try:
                session.commit()
            except:
                session.rollback()

        else:
            # print(session_data.SD_MOB_OTP)
            session_data.SD_CUSTOMER_NAME = chat_logs.CL_INPUT_DATA;

            try:

                if session_data.SD_MOB_OTP == chat_logs.CL_INPUT_DATA:
                    session = sessionmakerfun()
                    result1 = session.query(CBInquiry).filter(CBInquiry.SD_ID_FK == session_data.SD_ID_PK).all() 
                    last_row = len(result1)
                    if last_row == 0:
                        last_row = 1
                    cb_inquiry = result1[last_row - 1]
                    cb_inquiry.CB_IS_MOBILE_VERIFIED='1'
                    session.add(cb_inquiry)
                    session.commit()
                    # r = requests.get("http://api-voice.solutionsinfini.com/v1?api_key=A3ecea9e7447b6df41333df907c807932&method=dial.click2call&format=xml&caller=" + session_data.SD_MOBILE_NO + "&receiver=ivr:6023")

                    chat_response["responseText"] = googletransfn('Great!!! Thanks for your interest in Manappuram. One of our executive will contact you shortly.',chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    suggestion_array = suggestion_array_fun(chat_d)
                    chat_response["suggestions"] = suggestion_array
                    # print(r.content)
                    chat_response["responseAction"] = ''
                    session_data.SD_NEXT_ACTION = None
                    session=sessionmakerfun()
                    session_data.SD_SESSION_ID=create_UUID()
                    session.add(session_data)
                    session.commit()

                else:
                    suggestion_array = []
                    suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                                       suggestionInput="Resend OTP")
                    suggestion_array.append(suggestions)

                    suggestions = dict(
                        suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                        suggestionInput="Change Phone Number")
                    suggestion_array.append(suggestions)
                    chat_response['suggestions'] = suggestion_array
                    chat_response["responseText"] = googletransfn(
                        'Invalid OTP, Please retry',
                         chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    session_data.SD_NEXT_ACTION = 'gold_customer_call_back_method_otp_veri'
                    cb_inquiry.CB_IS_MOBILE_VERIFIED='0'
                    session = sessionmakerfun()
                    session.add(session_data)
                    session.commit()
            except:
                suggestion_array = []
                suggestions = dict(suggestionText=googletransfn("Resend OTP",  chat_d.CG_LANG_CODE),
                                   suggestionInput="Resend OTP")
                suggestion_array.append(suggestions)

                suggestions = dict(
                    suggestionText=googletransfn("Change Phone Number",  chat_d.CG_LANG_CODE),
                    suggestionInput="Change Phone Number")
                suggestion_array.append(suggestions)
                chat_response['suggestions'] = suggestion_array
                chat_response["responseText"] = googletransfn(
                    'Invalid OTP, Please retry',
                     chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                session_data.SD_NEXT_ACTION = 'gold_customer_call_back_method_otp_veri'
                session = sessionmakerfun()
                session.add(session_data)
                session.commit()






    # session.commit()
    return chat_response




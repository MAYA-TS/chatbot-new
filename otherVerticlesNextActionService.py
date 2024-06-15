
from sqlalchemy.orm import sessionmaker, session
from sessionChecking import chatSessionService, saveMetaData,sessionmakerfun
from Models import SessionData, ChatLanguages, Branchs, GlInquiry, FAQS, FAQResponses, OvInquiry
from otpService import generateOTP
import zeep
import json
import requests
import re
from otherVerticallist import verticalList
from googletranspython import googletransfn
from suggestionService import suggestion_array_fun
from ssid import create_UUID
from vehiclelist import vehicleList
from datetime import datetime
wsdl = "https://online.manappuram.com/custbot/custbot.asmx?WSDL"
client = zeep.Client(wsdl=wsdl)
# session = sessionmakerfun()
def otherVerticalnextAction(chat_logs, session_data):
    #print("into otherverticalnextAction loop")
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
        # googletransfn('Language changed to ' + str(chat_d.CG_LANG_NAME_EN), chat_d.CG_LANG_CODE)
        chat_response["responseText"] = googletransfn('PLease try again ' + str(chat_d.CG_LANG_NAME_EN),
                                                             chat_d.CG_LANG_CODE)
        chat_response["responseText2"]=''
        chat_response["responseAction"] = ''
    except:
        session_data.CG_ID_FK = 1

    if session_data.SD_NEXT_ACTION == 'other_get_full_name':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for other verticals':
            chat_response["responseText"] = googletransfn(
                'Select the vertical you are looking for',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            chat_response['suggestions'] = verticalList()
            session_data.SD_NEXT_ACTION = "other_vertical_list"
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            session.commit()
            # except:
            #     session.rollback()
        else:
        #print("reached here")
            session = sessionmakerfun()

            result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()

            last_row1 = len(result1)
            if last_row1 == 0:
                last_row1 = 1
            other_enquiry = result1[last_row1 - 1]
            print(other_enquiry.SD_ID_FK)
            print(other_enquiry.OV_ID_PK)
            # try:
            if len(chat_logs.CL_ORG_INPUT_DATA) != 0:

                #print(len(chat_logs.CL_ORG_INPUT_DATA))
                #print("into first stage", chat_logs.CL_ORG_INPUT_DATA)
                other_enquiry.OV_VERTICAL_NAME = chat_logs.CL_ORG_INPUT_DATA
                session_data.SD_NEXT_ACTION = "other Enter Phone number"

                # session.commit()
                #print(session_data.SD_NEXT_ACTION)

                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('Please provide your full name',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                #print(other_enquiry.OV_VERTICAL_NAME)
                session = sessionmakerfun()

                session.add(other_enquiry);
                session.commit()
                session = sessionmakerfun()
                session.add(session_data);
                # try:
                session.commit()
                # except:
                #     session.rollback()

            else:
                session_data.SD_NEXT_ACTION = "other_get_full_name"
                session = sessionmakerfun()

                session.add(session_data);

                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('Please select correct vertical',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                try:
                    session.commit()
                except:
                    session.rollback()
            # except ValueError:
            #     session_data.SD_NEXT_ACTION = "other_get_full_name"
            #     session.add(session_data);
            #
            #     chat_response["responseType"] = 'Text'
            #     chat_response["responseText"] = googletransfn('Please select correct vertical',
            #                                                          chat_d.CG_LANG_CODE)
            #     chat_response["responseAction"] = ''
            #
            #     try:
            #         session.commit()
            #     except:
            #         session.rollback()
    elif session_data.SD_NEXT_ACTION == 'other_vertical_list':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for other verticals':
            chat_response["responseText"] = googletransfn(
                'Select the vertical you are looking for',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            chat_response['suggestions'] = verticalList()
            session_data.SD_NEXT_ACTION = "other_vertical_list"
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            session.commit()
            # except:
            #     session.rollback()
        else:
            session = sessionmakerfun()

            result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()

            last_row1 = len(result1)
            if last_row1 == 0:
                last_row1 = 1
            other_enquiry = result1[last_row1 - 1]
            if len(chat_logs.CL_ORG_INPUT_DATA) != 0:
                if chat_logs.CL_ORG_INPUT_DATA == 'Vehicle loan':

                    chat_response["responseText"] = googletransfn(
                    'Select the vertical you are looking for',
                    chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''

                    chat_response['suggestions'] = vehicleList()

                    # other_enquiry = OvInquiry()
                    other_enquiry.SD_ID_FK = session_data.SD_ID_PK
                    other_enquiry.OV_IS_MOBILE_VERIFIED = 0
                    other_enquiry.OV_CREATED_DATE = datetime.now()
                    # other_enquiry.TB_ID_FK = 0
                    other_enquiry.VERSION = 0
                    session_data.SD_TRAN_TYPE = 'OV'
                    session_data.SD_TRAN_ID = other_enquiry.OV_ID_PK
                    session_data.SD_NEXT_ACTION = "other_get_full_name"
                    session = sessionmakerfun()

                    session.add(other_enquiry);
                    session.commit()
                    session = sessionmakerfun()

                    session.add(session_data);
                    # try:
                    session.commit()
                # except:
                #     session.rollback()
                elif chat_logs.CL_ORG_INPUT_DATA == 'Other Services':
                    session_data.SD_NEXT_ACTION = None
                    session = sessionmakerfun()

                    session.add(session_data);
                    try:
                        session.commit()
                    except:
                        session.rollback()
                    suggestion_array = suggestion_array_fun(chat_d)
                    chat_response["suggestions"] = suggestion_array

                    chat_response["responseText"] = "To avail other services :<br>" + "<a  href = 'https://www.manappuram.com/other-services' target='_blank'>Other Services</a>"
                    chat_response["responseText2"]=''
                elif chat_logs.CL_ORG_INPUT_DATA == 'Forex & Money Transfer':
                    other_enquiry.OV_VERTICAL_NAME = chat_logs.CL_ORG_INPUT_DATA
                    session_data.SD_NEXT_ACTION ='other forex customer name'
                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = googletransfn('Please provide the amount to transfer or receive',
                                                                chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''
                    session = sessionmakerfun()
                    session.add(other_enquiry);
                    session.commit()
                    session = sessionmakerfun()
                    session.add(session_data);
                    session.commit()
                else:
                    other_enquiry.OV_VERTICAL_NAME = chat_logs.CL_ORG_INPUT_DATA
                    session_data.SD_NEXT_ACTION = "other Enter Phone number"

                    # session.commit()
                    #print(session_data.SD_NEXT_ACTION)

                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = googletransfn('Please provide your full name',
                                                                        chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''
                    #print(other_enquiry.OV_VERTICAL_NAME)
                    session = sessionmakerfun()

                    session.add(other_enquiry);
                    session.commit()
                    session = sessionmakerfun()
                    session.add(session_data);
                    # try:
                    session.commit()


            else:
                session_data.SD_NEXT_ACTION = "other_get_full_name"
                session = sessionmakerfun()

                session.add(session_data);

                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('Please select correct vertical',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                try:
                    session.commit()
                except:
                    session.rollback()

    elif session_data.SD_NEXT_ACTION == 'other forex customer name':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for other verticals':
            chat_response["responseText"] = googletransfn(
                'Select the vertical you are looking for',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            chat_response['suggestions'] = verticalList()
            session_data.SD_NEXT_ACTION = "other_vertical_list"
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            session.commit()
        else:
        #print("reached here")
            session = sessionmakerfun()

            result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()

            last_row1 = len(result1)
            if last_row1 == 0:
                last_row1 = 1
            other_enquiry = result1[last_row1 - 1]
            print(other_enquiry.SD_ID_FK)
            print(other_enquiry.OV_ID_PK)
            # try:
            if len(chat_logs.CL_ORG_INPUT_DATA) != 0:

                #print(len(chat_logs.CL_ORG_INPUT_DATA))
                #print("into first stage", chat_logs.CL_ORG_INPUT_DATA)
                other_enquiry.FOREX_AMT = chat_logs.CL_ORG_INPUT_DATA
                session_data.SD_NEXT_ACTION = "other Enter Pin Code"

                # session.commit()
                #print(session_data.SD_NEXT_ACTION)

                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('Please provide your pincode',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                #print(other_enquiry.OV_VERTICAL_NAME)
                session = sessionmakerfun()

                session.add(other_enquiry);
                session.commit()
                session = sessionmakerfun()
                session.add(session_data);
                # try:
                session.commit()
                # except:
                #     session.rollback()
    elif session_data.SD_NEXT_ACTION == 'other Enter Pin Code':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for other verticals':
            if len(chat_logs.CL_ORG_INPUT_DATA) != 0:

                #print(len(chat_logs.CL_ORG_INPUT_DATA))
                #print("into first stage", chat_logs.CL_ORG_INPUT_DATA)
                session_data.SD_NEXT_ACTION = "other Enter Pin Code"

                # session.commit()
                #print(session_data.SD_NEXT_ACTION)

                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('Please provide your pincode',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                #print(other_enquiry.OV_VERTICAL_NAME)
                session = sessionmakerfun()
                session.add(session_data);
                # try:
                session.commit()
        #print("reached here")
        else:
            session = sessionmakerfun()

            result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()

            last_row1 = len(result1)
            if last_row1 == 0:
                last_row1 = 1
            other_enquiry = result1[last_row1 - 1]
            print(other_enquiry.SD_ID_FK)
            print(other_enquiry.OV_ID_PK)
            # try:
            if len(chat_logs.CL_ORG_INPUT_DATA) != 0:

                #print(len(chat_logs.CL_ORG_INPUT_DATA))
                #print("into first stage", chat_logs.CL_ORG_INPUT_DATA)
                other_enquiry.PINCODE = chat_logs.CL_ORG_INPUT_DATA
                session_data.SD_NEXT_ACTION = "other Enter Phone number"

                # session.commit()
                #print(session_data.SD_NEXT_ACTION)

                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn('Please provide your name',
                                                                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                #print(other_enquiry.OV_VERTICAL_NAME)
                session = sessionmakerfun()

                session.add(other_enquiry);
                session.commit()
                session = sessionmakerfun()
                session.add(session_data);
                # try:
                session.commit()
                # except:
                #     session.rollback()
    
    elif session_data.SD_NEXT_ACTION == 'other Enter Phone number':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for other verticals':
            chat_response["responseText"] = googletransfn(
                'Select the vertical you are looking for',
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''

            chat_response['suggestions'] = verticalList()
            session_data.SD_NEXT_ACTION = "other_vertical_list"
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            session.commit()
        else:
            session = sessionmakerfun()
            result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            # print(len(result1))
            last_row1 = len(result1)
            if last_row1 == 0:
                last_row1 = 1
            other_enquiry = result1[last_row1 - 1]
            if re.search("^[A-z][A-z|\.|\s]+$", chat_logs.CL_ORG_INPUT_DATA)!=None:

                other_enquiry.OV_CUSTOMER_NAME = chat_logs.CL_ORG_INPUT_DATA
                session = sessionmakerfun()
                session.add(other_enquiry);
                session.commit()
                session_data.SD_NEXT_ACTION = "other Enter OTP"
                session = sessionmakerfun()

                session.add(session_data);
                # try:
                session.commit()
                # except:
                #     session.rollback()        chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    'Please provide your 10 digit mobile number for authentication', chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                # print("seconded ending")
            else:
                session_data.SD_NEXT_ACTION = "Enter Phone number"
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


    elif session_data.SD_NEXT_ACTION == 'other Enter OTP':
        #if len(chat_logs.CL_ORG_INPUT_DATA) == 10:
        if (len(chat_logs.CL_ORG_INPUT_DATA) == 10)and(re.compile("[5-9][0-9]{9}").match(chat_logs.CL_ORG_INPUT_DATA)):

            session = sessionmakerfun()
            result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            last_row1 = len(result1)
            if last_row1 == 0:
                last_row1 = 1
            other_enquiry = result1[last_row1 - 1]
            other_enquiry.OV_MOBILE_NO = chat_logs.CL_ORG_INPUT_DATA
            OTP = generateOTP()
            other_enquiry.OV_MOBILE_OTP = OTP
            r = requests.get("http://bankalerts.sinfini.com/api/web2sms.php?workingkey=A2bbf78715947e342f970537bfd8bd62d&sender=MAFILD&to=" + str(other_enquiry.OV_MOBILE_NO) + "&message= Dear user, your one time password is " + str(OTP) + ". Manappuram&type=xml")
            session = sessionmakerfun()
            session.add(other_enquiry);
            try:
                session.commit()
            except:
                session.rollback()
            session_data.SD_NEXT_ACTION = "other Enter email ID"
            session = sessionmakerfun()
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()
            chat_response["responseType"] = 'Text'
            suggestion_array = []
            suggestions = dict(suggestionText=googletransfn("Resend OTP", chat_d.CG_LANG_CODE),
                               suggestionInput="Resend OTP")
            suggestion_array.append(suggestions)

            suggestions = dict(suggestionText=googletransfn("Change Phone Number", chat_d.CG_LANG_CODE),
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
            session_data.SD_NEXT_ACTION = 'other Enter OTP'
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()

    elif session_data.SD_NEXT_ACTION == 'other Enter email ID':
        if chat_logs.CL_ORG_INPUT_DATA=='Continue the flow for other verticals':
            session_data.SD_NEXT_ACTION = "other Enter OTP"
            session = sessionmakerfun()

            session.add(session_data);
            # try:
            session.commit()
            # except:
            #     session.rollback()        chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn(
                'Please provide your 10 digit mobile number for authentication', chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
        else:
            if chat_logs.CL_INPUT_DATA == 'Resend OTP':
                session = sessionmakerfun()
                result2 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
                last_row1 = len(result2)
                if last_row1 == 0:
                    last_row1 = 1
                other_enquiry = result2[last_row1 - 1]
                OTP = generateOTP()
                other_enquiry.OV_MOBILE_OTP = OTP
                r = requests.get(
                    "http://bankalerts.sinfini.com/api/web2sms.php?workingkey=A2bbf78715947e342f970537bfd8bd62d&sender=MAFILD&to=" + str(
                        other_enquiry.OV_MOBILE_NO) + "&message= Dear user, your one time password is " + str(OTP) + ". Manappuram&type=xml")
                session.add(other_enquiry);
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    'Please enter the valid OTP sent to your mobile number',
                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                suggestion_array = []
                suggestions = dict(suggestionText=googletransfn("Resend OTP", chat_d.CG_LANG_CODE),
                                suggestionInput="Resend OTP")
                suggestion_array.append(suggestions)

                suggestions = dict(
                    suggestionText=googletransfn("Change Phone Number", chat_d.CG_LANG_CODE),
                    suggestionInput="Change Phone Number")
                suggestion_array.append(suggestions)
                chat_response['suggestions'] = suggestion_array
                session_data.SD_NEXT_ACTION = 'other Enter email ID'
                session = sessionmakerfun()
                session.add(session_data);
                try:
                    session.commit()
                except:
                    session.rollback()

            elif chat_logs.CL_INPUT_DATA == "Change Phone Number":
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    'Please provide your 10 digit mobile number for authentication', chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                session_data.SD_NEXT_ACTION = 'other Enter OTP'
                session = sessionmakerfun()
                session.add(session_data);
                session.commit()

            else:
                session = sessionmakerfun()
                result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
                last_row1 = len(result1)
                if last_row1 == 0:
                    last_row1 = 1
                other_enquiry = result1[last_row1 - 1]
                if other_enquiry.OV_MOBILE_OTP ==  int(chat_logs.CL_ORG_INPUT_DATA):
                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = googletransfn(
                        'Your mobile authentication process is complete. Please provide your email id also',
                        chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    chat_response["responseAction"] = ''
                    suggestion_array = []
                    suggestions = dict(
                        suggestionText=googletransfn("I don't have an Email", chat_d.CG_LANG_CODE),
                        suggestionInput="Skip email")
                    suggestion_array.append(suggestions)

                    chat_response['suggestions'] = suggestion_array
                    session_data.SD_NEXT_ACTION = 'other Enter location or nearest branch'
                    other_enquiry.OV_IS_MOBILE_VERIFIED = 1
                    session = sessionmakerfun()
                    session.add(other_enquiry)
                    try:
                        session.commit()
                    except:
                        session.rollback()
                    session = sessionmakerfun()
                    session.add(session_data);
                    try:
                        session.commit()
                    except:
                        session.rollback()
                else:
                    chat_response["responseType"] = 'Text'
                    chat_response["responseText"] = googletransfn('Invalid OTP. Please re enter', chat_d.CG_LANG_CODE)
                    chat_response["responseText2"]=''
                    suggestion_array = []
                    suggestions = dict(suggestionText=googletransfn("Resend OTP", chat_d.CG_LANG_CODE),
                                    suggestionInput="Resend OTP")
                    suggestion_array.append(suggestions)

                    suggestions = dict(
                        suggestionText=googletransfn("Change Phone Number", chat_d.CG_LANG_CODE),
                        suggestionInput="Change Phone Number")
                    suggestion_array.append(suggestions)
                    chat_response['suggestions'] = suggestion_array
                    session_data.SD_NEXT_ACTION = 'other Enter email ID'
                    session = sessionmakerfun()
                    session.add(session_data);
                    try:
                        session.commit()
                    except:
                        session.rollback()

    elif session_data.SD_NEXT_ACTION ==  'other Enter location or nearest branch':

        if chat_logs.CL_INPUT_DATA == 'Skip email':
            session = sessionmakerfun()
            result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
            last_row1 = len(result1)
            if last_row1 == 0:
                last_row1 = 1
            other_enquiry = result1[last_row1 - 1]
            session_data.SD_NEXT_ACTION = None
            mobileNO = other_enquiry.OV_MOBILE_NO
            customerName = other_enquiry.OV_CUSTOMER_NAME
            verticalName = other_enquiry.OV_VERTICAL_NAME
            # with client.settings(raw_response=True):
            #     res = client.service.GetLMSData(mobileNO, customerName, verticalName)
            #     a = res.content.decode("utf-8")
            #     b = json.loads(a.split('<')[0])
            #     if b.get("status") == "111":
            #         leadId = b.get("leadID")
            #     else:
            #         leadId = ''
            #     other_enquiry.LEAD_ID = leadId
            session = sessionmakerfun()
            session.add(other_enquiry);
            try:
                session.commit()
            except:
                session.rollback()
            session_data.SD_NEXT_ACTION = None
            session = sessionmakerfun()
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()
            chat_response["responseType"] = 'Text'
            chat_response["responseText"] = googletransfn(
                "Thanks for your interest. One of our executive will contact you shortly.",
                chat_d.CG_LANG_CODE)
            chat_response["responseText2"]=''
            chat_response["responseAction"] = ''
            suggestion_array = suggestion_array_fun(chat_d)
            chat_response["suggestions"] = suggestion_array
            session = sessionmakerfun()
            session_data.SD_SESSION_ID=create_UUID()
            print(session_data.SD_SESSION_ID)
            session.add(session_data);
            try:
                session.commit()
            except:
                session.rollback()
        else:
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if re.search(regex, chat_logs.CL_ORG_INPUT_DATA):
                session = sessionmakerfun()
                result1 = session.query(OvInquiry).filter(OvInquiry.SD_ID_FK == session_data.SD_ID_PK).all()
                session_data.SD_NEXT_ACTION = None
                last_row1 = len(result1)
                if last_row1 == 0:
                    last_row1 = 1
                other_enquiry = result1[last_row1 - 1]
                other_enquiry.OV_EMAIL_ID = chat_logs.CL_ORG_INPUT_DATA
                mobileNO = other_enquiry.OV_MOBILE_NO
                customerName = other_enquiry.OV_CUSTOMER_NAME
                verticalName = other_enquiry.OV_VERTICAL_NAME
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    "Thanks for your interest. One of our executive will contact you shortly.",
                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                suggestion_array = suggestion_array_fun(chat_d)
                chat_response["suggestions"] = suggestion_array
                # with client.settings(raw_response=True):
                #     res = client.service.GetLMSData(mobileNO, customerName, verticalName)
                #     a = res.content.decode("utf-8")
                #     b = json.loads(a.split('<')[0])
                #     if b.get("status") == "111":
                #         leadId = b.get("leadID")
                #     else:
                #         leadId = ''
                #     other_enquiry.LEAD_ID = leadId
                session = sessionmakerfun()
                session_data.SD_SESSION_ID=create_UUID()
                session.add(other_enquiry);
                try:
                    session.commit()
                except:
                    session.rollback()
                session = sessionmakerfun()
                session.add(session_data);
                try:
                    session.commit()
                except:
                    session.rollback()
            else:
                chat_response["responseType"] = 'Text'
                chat_response["responseText"] = googletransfn(
                    'Please provide a valid email id',
                    chat_d.CG_LANG_CODE)
                chat_response["responseText2"]=''
                chat_response["responseAction"] = ''
                suggestion_array = []
                suggestions = dict(
                    suggestionText=googletransfn("I don't have an Email", chat_d.CG_LANG_CODE),
                    suggestionInput="Skip email")
                suggestion_array.append(suggestions)

                chat_response['suggestions'] = suggestion_array
                session_data.SD_NEXT_ACTION = 'other Enter location or nearest branch'
                session = sessionmakerfun()
                session_data.SD_SESSION_ID=create_UUID()
                session.add(session_data);
                try:
                    session.commit()
                except:
                    session.rollback()

    # session.commit()
    return chat_response


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Sequence, Float, Unicode

Base = declarative_base()

class Branchs(Base):
    __tablename__ = 'TBL_BRANCHES'

    TB_ID_PK = Column(Integer, Sequence('SEQ_TB_PK'), primary_key=True, )
    TB_BRANCH_CODE = Column(String)
    TB_BRANCH_NAME = Column(Unicode(500, collation='AL16UTF16'))
    TB_ADDRESS = Column(String)
    TB_PINCODE = Column(String)
    TB_PHONE = Column(DateTime)
    TB_WORKING_TIME = Column(String)
    TB_LATITUDE = Column(Float)
    TB_LONGITUDE = Column(Float)
    VERSION = Column(Integer)

class ChatLogs(Base):
    __tablename__ = 'TBL_CHAT_LOGS'

    CL_ID_PK = Column(Integer, Sequence('SEQ_CL_PK'), primary_key=True, )
    CL_SESSION_ID = Column(String)
    CL_INPUT_DATA = Column(Unicode(500, collation='AL16UTF16'))
    CL_ACTION = Column(String)
    CL_OUTPUT_DATA = Column(String)
    CL_TIMESTAMP = Column(DateTime)
    CL_INTENT_ID = Column(String)
    CL_INTENT_NAME = Column(String)
    CL_CREATED_DATE = Column(DateTime)
    VERSION = Column(Integer)
    CL_ORG_INPUT_DATA = Column(String)
    CL_ORG_OUTPUT_DATA = Column(String)



class ChatContexts(Base):
    __tablename__ = 'TBL_CHAT_CONTEXTS'

    CC_ID_PK = Column(Integer, Sequence('SEQ_CC_PK'), primary_key=True, )
    CL_ID_FK = Column(Integer, ForeignKey('TBL_CHAT_LOGS.CL_ID_PK'))
    CC_LIFE_SPAN = Column(Integer)
    CC_NAME = Column(String)
    CC_CREATED_DATE = Column(DateTime)
    CC_VERSION = Column(Integer)
    CC_TEST = Column(String)

class SessionData(Base):
    __tablename__ = 'TBL_SESSION_DATA'

    SD_ID_PK = Column(Integer, Sequence('SEQ_SD_PK'), primary_key=True)
    SD_SESSION_ID = Column(String)
    SD_CUSTOMER_NAME = Column(String)
    SD_MOBILE_NO = Column(String)
    SD_MOB_OTP = Column(String)
    SD_LATITUDE = Column(Float)
    SD_LONGITUDE = Column(Float)
    SD_PF_NAME = Column(String)
    SD_PF_VERSION = Column(String)
    SD_PF_LAYOUT = Column(String)
    SD_PF_OS_ARCHR = Column(String)
    SD_PF_OS_FAMILY = Column(String)
    SD_PF_OS_VERSION = Column(String)
    SD_PF_DESC = Column(String)
    SD_IPV4 = Column(String)
    SD_IPV6 = Column(String)
    CG_ID_FK = Column(Integer, ForeignKey('TBL_CHAT_LANGUAGES.CG_ID_PK'))
#    SD_IS_MOBILE_VERIFIED = Column(DateTime)
    SD_NEXT_ACTION = Column(String)
    SD_TRAN_TYPE = Column(String)
    SD_TRAN_ID = Column(Integer)
    SD_CREATED_DATE = Column(String)
    SD_UPDATED_DATE = Column(String)
    VERSION = Column(Integer)
    # SD_REMOTE_ADDRESS = Column(String)

class ChatLanguages(Base):
    __tablename__ = 'TBL_CHAT_LANGUAGES'

    CG_ID_PK = Column(Integer, Sequence('SEQ_CG_PK'), primary_key=True )
    CG_LANG_CODE = Column(String)
    CG_LANG_NAME = Column(Unicode(500, collation='AL16UTF16'))
    # CG_LANG_NAME = Column(String)
    CG_LANG_NAME_EN = Column(String)
    CG_IS_ACTIVE = Column(Integer)
    CG_CREATED_DATE = Column(DateTime)
    CG_UPDATED_DATE = Column(String)
    VERSION = Column(Integer)


class FAQResponses(Base):
    __tablename__ = 'TBL_FAQ_RESPONSES'

    FR_ID_PK = Column(Integer, Sequence('SEQ_FR_PK'), primary_key=True )
    FQ_ID_FK = Column(Integer, ForeignKey('TBL_FAQ.FQ_ID_PK'))
    CG_ID_FK = Column(Integer, ForeignKey('TBL_CHAT_LANGUAGES.CG_ID_PK'))
    FR_RESPONSE = Column(String)
    FR_CREATED_DATE = Column(DateTime)
    VERSION = Column(Integer)


class FAQS(Base):
    __tablename__ = 'TBL_FAQS'

    FQ_ID_PK = Column(Integer, primary_key=True)
    FQ_QUESTION = Column(String)
    FQ_INTENT_NAME = Column(String)
    FQ_IS_ACTIVE = Column(Integer)
    FQ_INTEGRATION_FLAG = Column(Integer)
    FQ_INTEGRATION_METHOD = Column(String)
    # FR_RESPONSE = Column(String)
    FQ_CREATED_DATE = Column(DateTime)
    FQ_UPDATED_DATE = Column(DateTime)
    VERSION = Column(Integer)


class GlInquiry(Base):
    __tablename__ = 'TBL_GL_INQUIRY'

    GL_ID_PK = Column(Integer, Sequence('SEQ_GL_PK'), primary_key=True)
    SD_ID_FK = Column(Integer, ForeignKey('TBL_SESSION_DATA.SD_ID_PK'))
    GL_CUSTOMER_NAME = Column(String)
    GL_MOBILE_NO = Column(String)
    GL_LOAN_AMOUNT = Column(Integer)
    GL_MOBILE_OTP = Column(Integer)
    GL_IS_MOBILE_VERIFIED = Column(Integer)
    GL_EMAIL_ID = Column(String)
    TB_ID_FK = Column(Integer, ForeignKey('TBL_BRANCHES.TB_ID_PK'))
    GL_IS_BRANCH_CONFIRMED = Column(Integer)
    GL_CREATED_DATE = Column(DateTime)
    GL_UPDATED_DATE = Column(DateTime)
    VERSION = Column(Integer)
    LEAD_ID = Column(String)
    GL_TYPE= Column(String)

class OvInquiry(Base):
    __tablename__ = 'TBL_OV_INQUIRY'

    OV_ID_PK = Column(Integer, Sequence('SEQ_OV_PK'), primary_key=True)
    SD_ID_FK = Column(Integer, ForeignKey('TBL_SESSION_DATA.SD_ID_PK'))
    OV_CUSTOMER_NAME = Column(String)
    OV_MOBILE_NO = Column(String)
    OV_VERTICAL_NAME = Column(String)
    OV_MOBILE_OTP = Column(Integer)
    OV_IS_MOBILE_VERIFIED = Column(Integer)
    OV_EMAIL_ID = Column(String)
    OV_CREATED_DATE = Column(DateTime)
    OV_UPDATED_DATE = Column(DateTime)
    VERSION = Column(Integer)
    LEAD_ID = Column(String)
    # FOREX_AMT = Column(Integer)
    # PINCODE = Column(Integer)

class CBInquiry(Base):
    __tablename__ = 'TBL_CALLBACK_DATA'

    CB_ID_PK = Column(Integer, Sequence('SEQ_CB_PK'), primary_key = True )
    SD_ID_FK = Column(Integer)
    CB_MOBILE_NUMBER = Column(Integer)
    CB_MOBILE_OTP = Column(Integer)
    CB_IS_MOBILE_VERIFIED = Column(String)
    CB_CREATED_DATE = Column(DateTime)

class Complaints(Base):
    __tablename__ = 'TBL_COMPLAINTS'

    CL_ID_PK = Column(Integer, Sequence('SEQ_CB_PK'),primary_key=True)
    SD_ID_FK = Column(Integer,ForeignKey('TBL_SESSION_DATA.SD_ID_PK'))
    CUSTOMER_YN = Column(String)
    PRODUCT_CATEGORY = Column(String)
    BRANCH_NAME = Column(String)
    STAFF_DTL = Column(String)
    OVERALL_SERVICE = Column(String)
    MPRM_DTL = Column(String)
    SRVC_RTNG = Column(String)
    FEEDBACK = Column(String)
    SUGGESTIONS = Column(String)
    COMPLAINT_DATE = Column(DateTime)
    CUST_NAME = Column(String)
    LOAN_NO = Column(Integer)
    CUST_EMAIL = Column(String)
    CUST_PHONE = Column(Integer)
    CUST_ADDRESS = Column(String)




from Models import ChatLogs, SessionData, ChatContexts, GlInquiry, Branchs
# from sqlalchemy.orm import sessionmaker, session
# from flask_session import Session

from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import cx_Oracle

#engine = create_engine("oracle://Sreekanth:chatbot123#321@10.1.9.96:1749/UATDB",implicit_returning=False)
# # engine = create_engine("oracle://chatbot:mapSql@localhost:1521/orcl",implicit_returning=False)
# session_maker = sessionmaker(bind=engine)
# session_maker.configure(bind=engine)
# session = session_maker();



####engine = create_engine("oracle://Sreekanth:chatbot123#321@10.1.9.96:1749/UATDB",implicit_returning=False)


#user = 'mana0809'
#pwd = 'mana0809'
#dsn = cx_Oracle.makedsn('10.150.3.15','1521',service_name='MAFILUAT.allexadbclients.macomspokevcn.oraclevcn.com')

#engine = create_engine('oracle+cx_oracle://{user}:{pwd}@{dsn}', echo=True)






##user = 'mana0809'
##pwd = 'mana0809'
##dsn = cx_Oracle.makedsn(
##    '10.150.3.15', 1521,
##     service_name='MAFILUAT.allexadbclients.macomspokevcn.oraclevcn.com'
##)
##engine = create_engine(f'oracle+cx_oracle://{user}:{pwd}@{dsn}', echo=True)



user = 'sreekanth'
pwd = 'chatbot123#321'
dsn = cx_Oracle.makedsn(
    '10.150.3.181', 1521,
     service_name='chatbot_chatpdb.paas.oracle.com'
)
engine = create_engine(f'oracle+cx_oracle://{user}:{pwd}@{dsn}', echo=True)






session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)





def sessionmakerfun():
    session = Session()
    return session

def chatSessionService(session_id):
    print('inside sessionid',session_id)
    session = sessionmakerfun()

    result = session.query(SessionData).filter(SessionData.SD_SESSION_ID == session_id).all();
    print('length = ',len(result))
    if len(result) == 0:
        session_data = SessionData()
        #print('Before updateing session id= ',session_id)
        if session_id != '':
            session_data.SD_SESSION_ID = session_id
        else:
            session_data.SD_SESSION_ID=111
        session_data.SD_IS_MOBILE_VERIFIED = 0
        session_data.SD_LATITUDE = 0
        session_data.SD_LONGITUDE = 0
        session_data.SD_CREATED_DATE = datetime.now()
        session_data.VERSION = 0
        session_data.CG_ID_FK = 1
        session = sessionmakerfun()
        session.add(session_data)
        try:
            session.commit()
        except:
            session.rollback()

    else:
        session_data = result[0]
    #session = sessionmakerfun()
    #session.add(session_data)
    #try:
    #    session.commit()
    #except:
    #    session.rollback()


    return session_data


def saveMetaData(session_data,mdata):
    session_data.SD_PF_NAME = mdata['platform_name']
    session_data.SD_PF_VERSION = mdata['platform_version']
    session_data.SD_PF_LAYOUT = mdata['platform_layout']
    session_data.SD_PF_OS_ARCHR = mdata['platform_os']['architecture']
    session_data.SD_PF_OS_FAMILY = mdata['platform_os']['family']
    session_data.SD_PF_OS_VERSION = mdata['platform_os']['version']
    session_data.SD_PF_DESC = mdata['platform_description']
    session_data.SD_LATITUDE = mdata['latitude']
    session_data.SD_LONGITUDE = mdata['longitude']
    session_data.SD_IPV4 = mdata['ipv4']
    session_data.SD_IPV6 = mdata['ipv6']
    session = sessionmakerfun()
    session.add(session_data)
    try:
        session.commit()
    except:
        session.rollback()




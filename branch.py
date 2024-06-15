import cx_Oracle
from sessionChecking import sessionmakerfun
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.sql import text
# session = sessionmakerfun()
#test for pushing
def branch_details_loc(latitudeVal,longitudeVal):
    km = 50
    numberOFBranches = 3
    action = "Select Branch"
    session = sessionmakerfun()
    c = session.execute(text("SELECT * FROM (SELECT TB_ID_PK, TB_BRANCH_CODE, TB_BRANCH_NAME, TB_ADDRESS, TB_PINCODE, TB_PHONE, TB_WORKING_TIME, 'Select Branch', distance FROM (SELECT z.TB_ID_PK, z.TB_BRANCH_CODE, z.TB_BRANCH_NAME, z.TB_ADDRESS, z.TB_PINCODE, z.TB_PHONE, z.TB_WORKING_TIME,z.TB_LATITUDE, z.TB_LONGITUDE, p.radius, p.distance_unit * rad2deg * (ACOS(LEAST(1.0,COS(deg2rad * (p.latpoint)) * COS(deg2rad * (z.TB_LATITUDE)) * COS(deg2rad * (p.longpoint - z.TB_LONGITUDE)) + SIN(deg2rad * (p.latpoint)) * SIN(deg2rad * (z.TB_LATITUDE))))) AS distance FROM TBL_BRANCHES z JOIN ( SELECT   '"+str(latitudeVal)+"'  AS latpoint, '"+str(longitudeVal)+"' AS longpoint, '50' AS radius,        '111.045' AS distance_unit, '57.2957795' AS rad2deg, '0.0174532925' AS deg2rad FROM  DUAL ) p ON 1=1 WHERE z.TB_LATITUDE BETWEEN p.latpoint  - (p.radius / p.distance_unit) AND p.latpoint  + (p.radius / p.distance_unit) AND z.TB_LONGITUDE BETWEEN p.longpoint - (p.radius / (p.distance_unit * COS(deg2rad * (p.latpoint)))) AND p.longpoint +(p.radius / (p.distance_unit * COS(deg2rad * (p.latpoint))))) WHERE distance <= radius ORDER BY distance ) WHERE ROWNUM <=  '3'")) # use triple quotes if you want to spread your query across multiple lines
    suggestion_array=[]
    for row in c:
        branches_array = dict(branchId=row[0], branchCd=row[1],
                              branchName=row[2], address=row[3]
                              , pinCode=row[4], phone=row[5],
                              workingTime=row[6], action="Select Branch")
        suggestion_array.append(branches_array)
    return suggestion_array

def branch_details_pincode(pinCOde):
    km = 50
    numberOFBranches = 3
    action = "Select Branch"
    session = sessionmakerfun()
    c = session.execute(text("SELECT * FROM(SELECT * FROM(SELECT TB_ID_PK, TB_BRANCH_CODE, TB_BRANCH_NAME, TB_ADDRESS, TB_PINCODE, TB_PHONE, TB_WORKING_TIME, 'Select pinCode', ABS(TO_NUMBER(TB_PINCODE) - " + str(pinCOde)+" ) diff FROM TBL_BRANCHES) ORDER BY diff ) WHERE ROWNUM <= '3'")) # use triple quotes if you want to spread your query across multiple lines
    suggestion_array=[]
    for row in c:
        # branches_array = dict(branchId=row[0], branchCd=row[1],
        #                       branchName=row[2], address=row[3]
        #                       , pinCode=row[4], phone=row[5],
        #                       workingTime=row[6], action="Select Branch")
        branches_array=dict(suggestionText=row[2],suggestionInput=row[2])
        suggestion_array.append(branches_array)
    return suggestion_array

from arcgis.gis import GIS
from datetime import datetime
from tkinter import messagebox
import sys
import os
import smtplib
from email.message import EmailMessage
print("opened")
now = datetime.now()
date = now.strftime('%Y%m%d')
def emailNotification(message, subject, fromAcct, toAcct, SMTPDomain):
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = fromAcct
        msg['To'] = toAcct
        s = smtplib.SMTP(SMTPDomain)
        s.send_message(msg)
        s.quit()
def downloadAGOLData(backupLocation, gisPath, account, password, itemID):
    public_data_item_id = itemID
    gis = GIS(gisPath, account, password)
    data_item = gis.content.get(public_data_item_id)
    fgdb_title = data_item.title.replace(" ","_")+date
    result = data_item.export(fgdb_title, "File Geodatabase")
    data_path = backupLocation+"\\"+date
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    result.download(data_path)
    print("downloaded")
    print(result)
    try:
         result.delete()
    except Exception as e:
         print(e)
    print(data_item.title.replace(" ","_")+date+" complete")
try:
    # these lines can be recycled for as many pieces of content (item ID's) you'd like to back up. The following arguments are used: windows file explorer backup location, AGOL organization url, administrator built in account name, administrator built in account password, AGOL item ID (found at the end of the URL on the item details page for this item)
    downloadAGOLData(r'C:/backup',"http://myOrg.maps.arcgis.com/home","myAGOLAdminAccount","myAGOLAdminPassword",'6e92f521e1e54ae2b8a8927ee1dce26a')
    downloadAGOLData(r'C:/backup',"http://myOrg.maps.arcgis.com/home","myAGOLAdminAccount","myAGOLAdminPassword",'bc00be1799c94814a0191f3c9f83495f')
except Exception as e:
    #if the backup process fails, email the data steward.
    print(str(e))
    emailNotification(r'Sidewalks data backup for '+date+' failed. Error: '+str(e),'Sidewalk Data Backup for '+date+' Failed!', 'john.doe@gmail.com','john.doe@gmail.com','smtp.gmail.com')
    sys.exit(0)
sys.exit(0)
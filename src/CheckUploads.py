#===============================================================================
#                                                                                    
# CheckUploads.py Copyright 2013 Neighborhoodguard all Rights Reserved
# Special program to check that at least one file was uploaded on the day before
# as part of the Neighborhood Guard program         
# Program only checks for directories that conforms to the data format
# This should be run once a day                
#                                                                                    
# Written by Howard Matis                                                       
#                                                                                    
# Version 1.0   November 30, 2013
#         1.1   December 1, 2013  Clean up some code and send one image
#         1.2   December 2, 2013  Added log file to show errors
#         1.3   December 3, 2013  Do not send camera owners messages when a problem, more diagnostics
#         1.4   December 3, 2013
#         1.5   December 5, 2013  More Updates
#         1.6   December 9, 2013  Change Way Multiple recipients are sent
#         1.7   December 10, 2013 More robust against ftp failures
#         1.8   December 21, 2013 Change smtp method
#         1.9   January 13, 2014  Change path for web viewer
#
#===============================================================================

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib     #needed for mail program
import datetime    #to get current date
import ftplib      #ftp routines
import os          #os commands
import sys
import traceback
import time         #to get sleep function
from random import randint   #random number generator
from os import rename   #for os rename

from CheckUploads_localsettings import *

def check_ftp_files():
            
    try:
        ftp = ftplib.FTP(machine)
        try:
            ftp.login(machine_name, machine_code)
        except:
            print "Unable to logon to", machine_name
            ftp_connection = False
            return ftp_connection, ftp_connection, ftp_connection, ftp_connection #put in error code
    except:
        print 'Unable to ftp to', machine
        ftp_connection = False
        return ftp_connection, ftp_connection, ftp_connection, ftp_connection #put in error code

    
    now = datetime.datetime.now()
    now -= datetime.timedelta(days=1)
    yesterday = now.strftime('20' + '%y' +'-' + '%m' + '-' + '%d')   #will fail in year 2100
    line_count = []
    images_found =[]
            
    for camera in cameras:
        command = 'cwd ' + '/' + camera_path + '/' + yesterday + '/' + camera + '/hires'
        try:
            ftp.voidcmd(command)    #need to handle errors
            
        # empty list that will receive all the log entry
            log = [] 
        # we pass a callback function bypass the print_line that would be called by retrlines
        # we do that only because we cannot use something better than retrlines
            ftp.retrlines('LIST', callback=log.append)
        # we use rsplit because it more efficient in our case if we have a big file
            files = (line.rsplit(None, 1)[1] for line in log)
        # get you file list
            files_list = list(files)
            total_lines = len(files_list)
        except:
            print 'No images found for the camera located at', camera
            total_lines = 0
            
        if total_lines > 0:
            try:
                random_image = files_list[ randint(0,total_lines - 1) ]
                print "The random image name is", random_image,"with",total_lines,'files'
                ftp.retrbinary("RETR " + random_image ,open(random_image, 'wb').write)  #This is bad code.  Would rather directly save it to tmp directly
                print "Successful downloaded the file", random_image
                newfile = image_directory + camera + '.jpg'
                print "Creating new file", newfile
                rename(random_image, newfile)               #saving files as 'image_directory'imageN.jpg
                print "Renamed the file to", newfile
                images_found.append(True)  
            except:
                print "Unable to retrieve image file", random_image, "from camera", camera
                images_found.append(False)  
        else:
            images_found.append(False)           

        line_count.append(total_lines)               #return the total lines sent from the camera
    ftp.quit()
    ftp_connection = True
    return ftp_connection,line_count,yesterday,images_found

def send_email(good_camera_state, files_found, date, images_found):   #This routine sends an email to people on the call list
    if good_camera_state == False:
        print "There was at least one camera MISSING images on", date
        print "Please take action!!"
    else:
        print "All cameras were producing images on", date

    smtpserver = smtplib.SMTP(smtp_server, smtp_port)
    smtpserver.set_debuglevel(debuglevel)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    try:
        smtpserver.login( smtp_user, smtp_id)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        print "Cannot logon to Computer"
        sys.exit(0)
    
    msg = MIMEMultipart()
    msg['To'] = ",".join(tos)
    msg['From'] = smtp_user
    if good_camera_state == False:
        msg['Subject'] = "*** ERROR: No images were generated from at least one CharingCross/Sherwick camera on " + date + " ***"
    else:
        msg['Subject'] = "All CharingCross/Sherwick cameras uploaded images on " + date

    msg.preamble = 'Multipart massage.\n'   # That is what you see if you don't have an email reader:
               
    body =''
    for index, value in enumerate(cameras):
        captured_images = files_found[index]
        body = body + 'The number of images recorded for the camera located at '  + value  + ' is ' + str (captured_images) + '\n'
  
    body = body + '\n'
    part = MIMEText(body)       # This is the textual part:
    msg.attach(part) 
       
    print ""
    print "The Message Body without images is:"
    print msg
    
    total_images = 0
    for index, value in enumerate(cameras):                 #add the images
        captured_images = files_found[index]
        total_images = total_images + captured_images
        if captured_images > 0:
            # This is the binary part(The Attachment)
            if images_found[index]:
                newfile = image_directory + value + '.jpg'
                part = MIMEApplication(open(newfile,"rb").read())
                part.add_header('Content-Disposition', 'attachment', filename= newfile)
                msg.attach(part)
            else:
                print "Unable to get fetch image from camera", value
    
    if email:
        smtpserver.sendmail(smtp_user, tos, msg.as_string() )
        
    if total_images > 0:                            #Only send warning messages to camera owners if at least one camera worked
        if good_camera_state == False:
            for index, value in enumerate(cameras):
                captured_images = files_found[index]
                if captured_images == 0:            #send a message to the owner of a file
                    msg = 'To:' + cameras_host[index] + '\n' + 'From: ' + smtp_user + '\n' + "Subject: *** ERROR: No images received from the camera located at " + value + "on date " + date +" ***\n"
                    msg = msg + '\n Please try to fix the camera.\nFor assistance contact Howard Matis at HSMatis@gmail.com.\nThank you.'
                    if email:
                        smtpserver.sendmail(smtp_user, cameras_host[index], msg)
                        print "Error with camera located at",value," Message sent to",cameras_host[index]
        else:
            print '\nNo need to send a message to any owner as all cameras had images collected by server.'
    else:
        print "\nDid not send a message to camera owners because there was a problem with the program: No images found!!"
    
    print 'All email sent!'
    smtpserver.close()

def fcount(path):    #""" Counts the number of files in a directory """
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1
    return count

def check_cameras(files):   #Checks whether a camera is working.  If there is at least one image uploaded, then the camera is declared working
    all_working_cameras = True          #a positive error code says that received images for all cameras
    for file_count in files:
        if file_count == 0:
            all_working_cameras = False
    return all_working_cameras
    
for n in range(180):     #try n ftp connections before giving up
    (ftp_connection,files_found,date, images_found) = check_ftp_files()
    if ftp_connection:
        break
    else:
        sleep_time = 60              #time in seconds to wait
        print "Waiting", sleep_time,"seconds to see if FTP connection can be retried for iteration", n
        time.sleep(sleep_time)      

if ftp_connection:
    good_camera_state = check_cameras(files_found)
    send_email(good_camera_state, files_found, date,images_found)  
    print "\nExecution of program CheckUploads has completed."
else:
    print "\nFailed after repeated attempts to connect."
quit()
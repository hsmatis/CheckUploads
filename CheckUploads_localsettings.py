
#===============================================================================
#                                                                                    
# CheckUploads_localsettings.py Copyright 2013-4 Neighborhoodguard all Rights Reserved
# Special program to check that at least one file was uploaded on the day before
# as part of the Neighborhood Guard program         
#
# This program set the parameters used by CheckUploads.py
#                                                                                    
# Written by Howard Matis                                                       
#                                                                                    
# Version 1.0    November 30, 2013                                                                   
#         1.1    December 1, 2013     Clean up some code and add sending of images
#         1.2    December 3, 2013     Some Cleanup
#         1.6    December 9, 2013     Change Way Multiple recipients are sent
#         1.7    December 21, 2013    Switch to yahoo account
#
#===============================================================================

#list of people getting full information from cameras

tos = ['terryg2@ix.netcom.com', 'williamptullis@gmail.com', 'HSMatis@gmail.com', 'TommyT@AccountMate.com', 'fitzpaul@sbcglobal.net' ]

cameras = []                        #list of the camera names
cameras.append("6808Charing")
cameras.append("6900Sherwick")
cameras.append("6975Charing")

cameras_host = []                   #list of the host of a camera - email only when there is an error for their camera
cameras_host.append("TommyT@AccountMate.com")
cameras_host.append("fmsets@hotmail.com")
cameras_host.append("hrsron@gmail.com")


smtp_user = 'alerts@charingcrosssherwick.org'     #This account is only to get a smtp server
smtp_server = 'mail.charingcrosssherwick.org'
smtp_id = 'password for the mail server'
smtp_port = 587

machine = 'Name of the Machine'
machine_name = 'username of the ftp server'
machine_code = 'password for the ftp server'
camera_path = 'video.charingcrosssherwick.org'

image_directory = ' /Users/family/GoogleDrive/Workspace-General/CheckUploads/tmp/'                 #location where images are stored

#execution parameters

email = True
debuglevel = False

CheckUploads
============

Program written by Howard Matis - HSMatis@gmail.com

Check the performance of the camera system daily for the performance of the neighborhood guard system the day before.

This program looks on the ftp server, counts the number of files.  It then sends a report of this number via email
to a list of people.  The email also contains a random picture from one of the cameras.  

In addition, it sends a message to the owner of a camera if no files were uploaded for yesterday


CheckUploads.sh should be run by a cron job once a day
CheckUploads_localsettings.py needs to be updated for the particular camera environment

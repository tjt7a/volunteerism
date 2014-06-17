#Import statements for XML parser, SMTPLIB (for email) and random (for shuffling)
import xml.etree.ElementTree as ET
import smtplib
from email.mime.text import MIMEText
from random import shuffle
import string

#This is the volunteer script
#It selects a volunteer and sends that volunteer an email

# Parse the volunteer.xml file containing the list of volunteers
tree = ET.parse("/home/tjt7a/volunteerism/volunteers.xml")
root = tree.getroot()

volunteer_list = []

for volunteer in root.findall('volunteer'):
	count = volunteer.attrib['count']
	name = volunteer.find('name').text
	email = volunteer.find('email').text
	volunteer_list.append((name, email, int(count)))

sorted_list = []

# Sort the list of volunteers by their counts
sorted_list = sorted(volunteer_list, key=lambda volunteer: volunteer[2])
#Grab the smallest count available
smallest_count = sorted_list[0][2]

# Create a temp list of all lab mates with the same count
temp_list = []
for volunteer in sorted_list:
	if volunteer[2] == smallest_count:
		temp_list.append(volunteer)

# Shuffle that list
shuffle(temp_list)

# Find the volunteer that we selected and increment their count
for volunteer in root.findall('volunteer'):
	name =  volunteer.find('name').text
	if name == temp_list[0][0]:
		count = str(int(volunteer.attrib['count'])+1)
		volunteer.attrib['count'] = count
tree.write("/home/tjt7a/volunteerism/volunteers.xml")

# Send the email!
email_fp = open('/home/tjt7a/volunteerism/email.txt', 'rb')
hplp_fp = open('/home/tjt7a/volunteerism/hplp.txt', 'rb')
vol_msg = MIMEText(email_fp.read())

# Replace the '#####' token with the name of the volunteer
hplp_str = hplp_fp.read()
hplp_str = string.replace(hplp_str, "#####", name)

hplp_msg = MIMEText(hplp_str)
email_fp.close()
hplp_fp.close()

me = 'MCP'
you = temp_list[0][1] 
hplp = "hplp@collab.itc.virginia.edu"

vol_msg['Subject'] = 'You are this week\'s HPLP Volunteer!'
vol_msg['From'] = me
vol_msg['To'] = you

hplp_msg['Subject'] = "Congratulate this week\'s HPLP Volunteer: "+name
hplp_msg['From'] = me
hplp_msg['To'] = hplp

s = smtplib.SMTP('localhost')
s.sendmail(me, [you], vol_msg.as_string())
s.sendmail(me, [hplp], hplp_msg.as_string())
s.quit()

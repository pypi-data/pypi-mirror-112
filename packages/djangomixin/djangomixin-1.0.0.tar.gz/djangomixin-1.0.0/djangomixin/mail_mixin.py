import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


from_email = settings.DEFAULT_FROM_EMAIL
from_sender = settings.DEFAULT_FROM_SENDER
username_smtp = settings.USERNAME_SMTP
password_smtp = settings.PASSWORD_SMTP
host_smtp = settings.HOST_SMTP
port_smtp = settings.PORT_SMTP


def send_mail(sender=from_email, sender_name=from_sender, recipient=None, \
				  subject='Message From Django Server', body_tex='', body_html=''):

	if recipient is None or not sender:
		return

	USERNAME_SMTP = username_smtp
	PASSWORD_SMTP = password_smtp
	HOST = host_smtp
	PORT = int(port_smtp)

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = email.utils.formataddr((sender_name, sender))
	msg['To'] = recipient
	# msg.add_header('X-SES-CONFIGURATION-SET', CONFIGURATION_SET)

	part1 = MIMEText(body_tex, 'plain')
	part2 = MIMEText(body_html, 'html')

	msg.attach(part1)
	msg.attach(part2)

	try:
		server = smtplib.SMTP(HOST, PORT)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(USERNAME_SMTP, PASSWORD_SMTP)
		server.sendmail(sender, recipient, msg.as_string())
		server.close()
	except Exception as e:
		return {'success': False, 'msg': str(e)}
	else:
		return {'success': True, 'msg': 'Email sent!'}

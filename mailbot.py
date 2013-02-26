#!/usr/bin/python
import imaplib, smtplib, email

class Mailbot():
	def __init__(self):
		self.username    = ""
		self.password    = ""
		self.from_field  = ""
		self.to_field    = ""

		self.imap_server = "imap.gmail.com"
		self.imap_port   = 993
		self.smtp_server = "smtp.gmail.com"
		self.smtp_port   = 587

	def new_msgs_uid_list(self):
		response, data = self.imap.uid(
			"search", None, "UNSEEN")
		uid_list = data[0].split()
		return uid_list

	def imap_connect(self):
		self.imap = imaplib.IMAP4_SSL(self.imap_server)
		self.imap.login(self.username, self.password)
		self.imap.select("inbox")

	def imap_logout(self):
		print self.imap.logout()

	def smtp_connect(self):
		self.smtp = smtplib.SMTP(self.smtp_server+":"+str(self.smtp_port))
		self.smtp.starttls()
		self.smtp.login(self.username, self.password)

	def smtp_logout(self):
		self.smtp.quit()

	def compose_msg(self, uid):
		response, data = self.imap.uid("fetch", uid, "(RFC822)")
		orig_msg = email.message_from_string(data[0][1])
		msg = "subject: "+orig_msg["subject"]+"\n\n"
		maintype = orig_msg.get_content_maintype()

		if maintype == "multipart":
			for part in orig_msg.get_payload():
				maintype = emsg.get_content_maintype()
				if ("text" in maintype) or ("html" in maintype):
					msg += orig_msg.get_payload()

		elif ("text" in maintype) or ("html" in maintype):
			msg += orig_msg.get_payload()
		return msg

	def forward_msg(self, uid):
		msg_body = self.compose_msg(uid)
		self.smtp.sendmail(self.from_field,
				   self.to_field,
				   msg_body)

	def forward_all_msgs(self):
		self.imap_connect()
		msg_list = self.new_msgs_uid_list() 
		if len(msg_list) > 0:
			self.smtp_connect()
			for i in msg_list:
				self.forward_msg(i)
			self.smtp_logout()
		self.imap_logout()

if __name__ == "__main__":
	bot = Mailbot()
	bot.forward_all_msgs()

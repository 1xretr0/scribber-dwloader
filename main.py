import imaplib
import email
from email.header import decode_header
from html.parser import HTMLParser
import requests

"""
Html parsing class
"""
class MyHTMLParser(HTMLParser):
	link = ""

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			if "kindle-content-requests-prod" in attrs[0][1]:
				self.link = attrs[0][1]

"""
@param link: the file url
@param subject: the email subject to obtain file title
"""
def download_pdf(link, subject):
	r = requests.get(link)

	file_title = subject.split('"')[1::2]

	pdf = open(r'/your/download/route/' + file_title[0] + ".pdf", 'wb') # MODIFY ROUTE
	pdf.write(r.content)
	pdf.close()

	print("***File Downloaded!***")

# main script flow
def main():
	# account credentials
	username = "email" 	# MODIFY
	password = "passwd" # MODIFY

	# use your email provider's IMAP server, you can look for your provider's IMAP server on Google
	# or check this page: https://www.systoolsgroup.com/imap/
	# for office 365 (hotmail, outlook), it's this:
	imap_server = "outlook.office365.com" # MODIFY EMAIL SERVER

	# number of top emails to fetch
	N = 3 # MODIFY?

	# create an IMAP4 class with SSL, use your email provider's IMAP server
	imap = imaplib.IMAP4_SSL(imap_server)
	# authenticate
	imap.login(username, password)

	# select a mailbox (in this case, the inbox mailbox)
	# use imap.list() to get the list of mailboxes
	status, messages = imap.select("INBOX")

	# total number of emails
	messages = int(messages[0])

	for i in range(messages, messages-N, -1):
		# fetch the email message by ID
		res, msg = imap.fetch(str(i), "(RFC822)")
		for response in msg:
			if isinstance(response, tuple):
				# parse a bytes email into a message object
				msg = email.message_from_bytes(response[1])

				# decode the email subject
				subject, encoding = decode_header(msg["Subject"])[0]
				if isinstance(subject, bytes):
					# if it's a bytes, decode to str
					subject = subject.decode(encoding)

				# decode email sender
				sender, encoding = decode_header(msg.get("From"))[0]
				if isinstance(sender, bytes):
					sender = sender.decode(encoding)

				print("Sender:", sender)
				print("Subject:", subject)

				# validate kindle scribe email
				if (sender == "Amazon Kindle <do-not-reply@amazon.com>" and "You sent" in subject):
					# if the email message is multipart
					if msg.is_multipart():
						# iterate over email parts
						for part in msg.walk():
							# extract content type of email
							content_type = part.get_content_type()
							content_disposition = str(part.get("Content-Disposition"))
							try:
								# get the email body
								body = part.get_payload(decode=True).decode()
							except:
								pass

							if content_type == "text/plain":
								# print text/plain emails and skip attachments
								print(body)
					else:
						# extract content type of email
						content_type = msg.get_content_type()
						# get the email body
						body = msg.get_payload(decode=True).decode()
						if content_type == "text/plain":
							# print only text email parts
							print(body)

					if content_type == "text/html":
						parser = MyHTMLParser()
						parser.feed(body)

						print("***Downloading File***")
						download_pdf(parser.link, subject)

						imap.close()
						imap.logout()

						exit()

				print("="*100)
	# close the connection and logout
	imap.close()
	imap.logout()


if __name__ == '__main__':
	main()
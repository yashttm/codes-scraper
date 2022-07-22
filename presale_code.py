#!/usr/bin/env python

from imap_tools import MailBox, AND
from imap_tools.errors import MailboxLoginError
from loguru import logger

# get list of email subjects from INBOX folder

logger.add('file_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation="5 MB")
emails = []
with open("emails.txt", "r") as emailfile:
    for line in emailfile:
        emails.append(line.strip())

# email = "ttmtickets@outlook.com"
for email in emails:
    try:
        with MailBox('outlook.office365.com').login(email, 'TICKETMERCHANT!982') as mailbox:
            logger.info("-------------------------")
            logger.info("Logged in to: {}".format(email))
            # subjects = []
            cuids = []
            # inboxes = ["Junk", "INBOX"]
            inboxes = ["Elton"]
            for inbox in inboxes:
                logger.info("Processing: {}".format(inbox))
                mailbox.folder.set(inbox)
                with open("codes.txt", "a+") as codefile:
                    for msg in mailbox.fetch(AND(subject='Elton John Goodwill Gesture - Important Information')):
                        if ("Elton John Goodwill Gesture - Important Information" in msg.subject) :
                            # subjects.append(msg.to)
                            cuids.append(msg.uid)
                            # mailbox.move(msg.uid, 'INBOX/Harry Styles Presale Codes')
                            logger.warning(msg.subject)
                            text = msg.text
                            try:
                                code = text.split("Unique Redemption Code is:")[1].split("Redemption code is")[0]
                                code = code.strip()

                                # qty = text.split("to redeem the")[1].split("ticket/s")[0]
                                # qty = qty.replace('["', "").replace('"]', "")
                                logger.success("{} - {}".format(msg.to[0], code.strip()))
                                codefile.write("{} - {}".format(msg.to[0], code.strip()))
                                codefile.write("\n")
                            except:
                                print(text)
                                with open("failures.txt", "a+") as failures:
                                    logger.error(email)
                                    failures.write("{email} - \"{to}\"".format(email=email, to=msg.to[0]))
                                    failures.write("\n")
                                    failures.close()
                        else:
                            print(msg.subject)
                    codefile.close()
            if len(cuids) < 1:
                # with open("failures.txt", "a+") as failures:
                logger.error(email)
                # failures.write(email)
                # failures.write("\n")
                # failures.close()
    except MailboxLoginError:
        # with open("failures.txt", "a+") as failures:
        logger.error("{} - LOGIN FAILED".format(email))
            # failures.write("{} - LOGIN FAILED".format(email))
            # failures.write("\n")
            # failures.close()

# # get list of email subjects from INBOX folder - equivalent verbose version
# mailbox = MailBox('imap.mail.com')
# mailbox.login('test@mail.com', 'pwd', initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg
# subjects = [msg.subject for msg in mailbox.fetch(AND(all=True))]
# mailbox.logout()
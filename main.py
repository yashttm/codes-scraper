#!/usr/bin/env python

from imap_tools import MailBox, AND

# get list of email subjects from INBOX folder
with MailBox('outlook.office365.com').login('gsvllcau@outlook.com', 'GSVLLC2020') as mailbox:
    subjects = []
    cuids = []
    auids = []
    inboxes = ["Junk", "INBOX"]
    for inbox in inboxes:
        print("Clearing: ", inbox)
        mailbox.folder.set(inbox)
        for msg in mailbox.fetch(mark_seen=False):
            if ("Your ticket transfer" in msg.subject) and ("is on the way for" in msg.subject):
                subjects.append(msg.subject)
                cuids.append(msg.uid)
            elif ("accepted your Ticket Forward Invitation." in msg.subject) or ("accepted your ticket transfer for" in msg.subject):
                subjects.append(msg.subject)
                auids.append(msg.uid)
            else:
                print(msg.subject)
        for uid in cuids:
            mailbox.move(uid, 'Confirmations - Ticket Forward')
        for uid in auids:
            mailbox.move(uid, 'Accepteds')
    print(subjects)

# # get list of email subjects from INBOX folder - equivalent verbose version
# mailbox = MailBox('imap.mail.com')
# mailbox.login('test@mail.com', 'pwd', initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg
# subjects = [msg.subject for msg in mailbox.fetch(AND(all=True))]
# mailbox.logout()
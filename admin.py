from Linephu.linepy import *
from Linephu.akad.ttypes import *
import time, random
import timeit



client = LINE()
client.log("Auth Token : " + str(client.authToken))
#client = LINE('email', 'password')

oepoll = OEPoll(client)

MySelf = client.getProfile()
JoinedGroups = client.getGroupIdsJoined()
print("My MID : " + MySelf.mid)

whiteListedMid = ["uadb864b186b1290dd86edb85ca87255d", "u23b3abbf2518782cc270e370d4c73713", "u50057fea961021c1599ff21157a84c43", "udb0d47a9a2f0a29804b0fda72787ce68", "u974b7cd3b88d461e103c92ecf3c990a7", "u260ad7f1ae40ae412594930291222161", "ue6aa8348fc13819fad9c3c20c780c897", "ua0eac1836a6251d2e7a7fb448f5ebbb3", "ub51d2d0bb6ac317c501b60c1bf49e7b5"]

#mymid : ""


def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        client.acceptGroupInvitation(op.param1)
        JoinedGroups.append(op.param1)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_INVITE_INTO_GROUP\n\n")
        return

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
    try:
        botlist = ["ua0eac1836a6251d2e7a7fb448f5ebbb3", "ub51d2d0bb6ac317c501b60c1bf49e7b5"]
        b = open("b.txt", "r")
        blackListedMid = b.readline()
        b.close()
        if op.param2 in blackListedMid:
            try:
                group = client.getGroup(op.param1)
                if group.preventedJoinByTicket == True:
                    try:
                        group.preventedJoinByTicket = False
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(random.choice(botlist), "/jgk gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url mid: " + op.param3 + " mid")
                    except Exception as e:
                        print(e)
                else:
                    try:
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        if op.param3 == MySelf.mid:
            hb = open("hb.txt", "r")
            b = open("b.txt", "r")
            halfBlackListedMid = hb.readline()
            blackListedMid = b.readline()
            hb.close()
            b.close()
            if op.param2 not in halfBlackListedMid and op.param3 not in blackListedMid:
                hb = open("hb.txt", "w")
                hb.write(op.param2)
                hb.close()
            elif op.param2 in halfBlackListedMid:
                b = open("b.txt", "w")
                b.write(op.param2)
                b.close()
            JoinedGroups.remove(op.param1)
        else:
            if op.param3 in whiteListedMid:
                if op.param2 not in whiteListedMid:
                    try:
                        group = client.getGroup(op.param1)
                        if group.preventedJoinByTicket == True:
                            try:
                                group.preventedJoinByTicket = False
                                str1 = client.reissueGroupTicket(op.param1)
                                client.updateGroup(group)
                                client.sendMessage(random.choice(botlist), "/jgk gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url mid: " + op.param3 + " mid")
                            except Exception as e:
                                print(e)
                        else:
                            try:
                                str1 = client.reissueGroupTicket(op.param1)
                                client.updateGroup(group)
                                client.sendMessage(random.choice(botlist), "/jgk gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url mid: " + op.param3 + " mid")
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
                group = client.getGroup(op.param1)
                if group.preventedJoinByTicket == True:
                    try:
                        group.preventedJoinByTicket = False
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
                else:
                    try:
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.toType == 0:
                    print("\n")
                    print("Private Chat Message Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Message : " + msg.text)
                    print("\n")
                    if msg._from in whiteListedMid:
                        if msg.text.startswith("/jgurlx"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                            group = client.getGroup(str1)
                            try:
                                client.reissueGroupTicket(str1)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                else:
                    pass
            except:
                pass
        else:
            pass
    except Exception as error:
        print(error)
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "mid":
                    client.sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    client.sendMessage(msg.to, text=None, contentMetadata={'mid': msg._from}, contentType=13)
                if msg.text == "you":
                    client.sendMessage(msg.to, text=None, contentMetadata={'mid': msg.to}, contentType=13)
                if msg.text == "speed":
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    client.sendMessage(msg.to, str1)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "invite bot":
                    group = client.getGroup(msg.to)
                    try:
                        group.preventedJoinByTicket = False
                        str1 = client.reissueGroupTicket(msg.to)
                        client.updateGroup(group)
                    except Exception as e:
                        print(e)
                    client.sendMessage("u23b3abbf2518782cc270e370d4c73713", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    client.sendMessage("u50057fea961021c1599ff21157a84c43", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    client.sendMessage("udb0d47a9a2f0a29804b0fda72787ce68", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    client.sendMessage("u974b7cd3b88d461e103c92ecf3c990a7", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    client.sendMessage("u260ad7f1ae40ae412594930291222161", "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    client.sendMessage("ue6aa8348fc13819fad9c3c20c780c897", "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                if msg.text == "speed":
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    client.sendMessage(msg.to, str1)
                if msg.text == "gcreator":
                    group = client.getGroup(msg.to)
                    ga = group.creator.mid
                    client.sendContact(msg.to, ga)
                if msg.text == "mid":
                    client.sendMessage(msg.to, msg._from)
                if msg.text == "gid":
                    client.sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "[群組名稱]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[群組圖片]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventedJoinByTicket is False: md += "\n\n行動網址: 開啟\n"
                    else: md += "\n\n行動網址: 關閉\n"
                    if group.invitee is None: md += "\n成員數: " + str(len(group.members)) + "人\n\n邀請中: 0人"
                    else: md += "\n成員數: " + str(len(group.members)) + "人\n邀請中: " + str(len(group.invitee)) + "人"
                    client.sendMessage(msg.to,md)
                if msg.text == "me":
                    client.sendContact(msg.to, MySelf.mid)
                if msg.text == "/destroy":
                    print("start destroying")
                    botlist = "u23b3abbf2518782cc270e370d4c73713", "u50057fea961021c1599ff21157a84c43", "udb0d47a9a2f0a29804b0fda72787ce68", "u974b7cd3b88d461e103c92ecf3c990a7", "u260ad7f1ae40ae412594930291222161", "ue6aa8348fc13819fad9c3c20c780c897"]
                    _name = msg.text.replace("/destroy","")
                    group = client.getGroup(msg.to)
                    targets = []
                    for g in group.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        client.leaveGroup(msg.to)
                        JoinedGroups.remove(msg.to)
                    else:
                        for target in targets:
                            try:
                                client.sendMessage(random.choice(botlist), "/kick gid: " + msg.to + " gid mid: " + target + " mid")
                            except:
                               client.sendMessage(msg.to, "error")
                if msg.text == "報數":
                    client.sendMessage("u23b3abbf2518782cc270e370d4c73713", "/sm mid: " + msg.to + " mid text: 1 text")
                    client.sendMessage("u50057fea961021c1599ff21157a84c43", "/sm mid: " + msg.to + " mid text: 2 text")
                    client.sendMessage("udb0d47a9a2f0a29804b0fda72787ce68", "/sm mid: " + msg.to + " mid text: 3 text")
                    client.sendMessage("u974b7cd3b88d461e103c92ecf3c990a7", "/sm mid: " + msg.to + " mid text: 4 text")
                    client.sendMessage("u260ad7f1ae40ae412594930291222161", "/sm mid: " + msg.to + " mid text: 5 text")
                    client.sendMessage("ue6aa8348fc13819fad9c3c20c780c897", "/sm mid: " + msg.to + " mid text: 6 text")
        else:
            pass

    except Exception as e:
        print(e)
        print ("\n\nSEND_MESSAGE\n\n")
        return



# Add function to LinePoll
oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.SEND_MESSAGE: SEND_MESSAGE,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

while True:
    oepoll.trace()

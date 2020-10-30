import smtplib
import random
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level='INFO')
logger = logging.getLogger(__name__)

participants = {'participant1': 'participant1@mail.com', 'participant2': 'participant2@mail.com',
                'participant3': 'participant3@mail.com', 'participant4': 'participant4@mail.com',
                'participantN': 'participantN@mail.com', 'participantM': 'participantM@mail.com'}

tuplesToAvoid = {'participantN': 'participantM',
                 'participantM': 'participantN'}  # we assume here that you can avoid only one person. See line 52 -> 55.


def _uniqueEverSeen(seq):
    """
    function to drop duplicates in seq while preserving order.
    :param seq: seq to reorder.
    :return: seq without duplicates.
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def _sendMail(receiver, namePicked):
    """
    function that send email via sender_email gmail.
    See: https://realpython.com/python-send-email/ for more information.
    :param receiver: Person that will receive the mail.
    :param namePicked:  The name drawn by the receiver.
    :return: None.
    """
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "yourHostGmail@gmail.com"  # Enter your address
    password = "yourPwd"
    receiver_email = participants[receiver]  # Enter receiver address
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your beautiful subject !"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """Hello {}, Your beautiful message to announce the name picked : {}""".format(receiver, namePicked)
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def selectSantas():
    """
    function to draw a name for every participant.
    :return: dict with receivers in keys, and participants picked in values.
    """
    # pick up first names in tuplesToAvoid, to avoid impossible combination if every others participants have been selected.
    participantsNames = _uniqueEverSeen(list(tuplesToAvoid.keys()) + list(participants.keys()))
    namesToPick = participantsNames.copy()
    # dict with all correspondences between participants
    finalTuples = {}
    for name in participantsNames:
        namesToPickAux = [x for x in namesToPick if x != name]
        if name in tuplesToAvoid:
            participantToAvoid = tuplesToAvoid[name]
            if participantToAvoid in namesToPickAux:
                namesToPickAux.remove(participantToAvoid)
        namePicked = random.choice(namesToPickAux)
        namesToPick.remove(namePicked)
        finalTuples[name] = namePicked
    return finalTuples


if __name__ == "__main__":
    # Sometimes, you can find impossible combination.
    # For example :
    # participantN -> participant 1, participantM -> participant2,
    # participant1 -> participant3, participant2 -> participantN, participant3 -> participantM
    # participant4 has no choice but to pick himself. It's impossible. So we retry a combination.
    # It's almost impossible that we pick up this kind of combination ten times or more in a row.
    nbTry = 10
    k = 0
    foundCombination = False
    while k < nbTry:
        try:
            finalTuples = selectSantas()
            foundCombination = True
            logger.info("Found a good combination, going to send mails...")
            for receiver, namePicked in finalTuples.items():
                # print("Correspondance {} -> {}".format(receiver, namePicked))  # to debug
                _sendMail(receiver=receiver, namePicked=namePicked)
            logger.info("Every mail was sent.")
            break
        except IndexError:
            k += 1
            logger.warning("Impossible combination found, retrying...")
    if not foundCombination:
        logger.error("No successful draw !".format(nbTry))
        raise Exception("No successful draw after {} tries, no mail was sent. Try to increase nbTry.".format(nbTry))



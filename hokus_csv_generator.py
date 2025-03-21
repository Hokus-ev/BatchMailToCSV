import imaplib
import email
import argparse
import logging


logger = logging.getLogger(__name__)


def ui():
    #TODO
    return

def parse_email_parameter(input_str):
    str_buffer = input_str.split("@",1)[0]
    return str_buffer

def filter_cleanup_Double_whitespaces(TextForFilter):
    cleanedText = TextForFilter
    while "  " in cleanedText:
        cleanedText = cleanedText.replace('  ', ' ')
    return str(cleanedText)

def filter_Replace_EOL_AND_TABS(TextForFilter):
    cleanedText = TextForFilter
    cleanedText = cleanedText.replace('\r', '') # filter return operator
    cleanedText = cleanedText.replace('\n', '') # filter newline operator
    cleanedText = cleanedText.replace('\t', '') # filter tab operator
    return str(cleanedText)

def filter_text(TextForFilter):
    cleanedText = TextForFilter
    cleanedText = filter_cleanup_Double_whitespaces(cleanedText)
    cleanedText = filter_Replace_EOL_AND_TABS(cleanedText)
    #add more filters if you feel it's necessary
    return str(cleanedText)


def main():
    #setup logging
    logging.basicConfig(filename='csv_generator_log.txt', level=logging.INFO)

    #defining necessary variables from user input
    # Argument-Parser erstellen
    parser = argparse.ArgumentParser(
        description="Dieses Skript verarbeitet E-Mails basierend auf den angegebenen Eingaben."
    )

    # Erforderliche Argumente
    parser.add_argument(
        "--server-domain",
        required=True,
        help="Die Domain des Servers, z. B. mail.example.com."
    )
    parser.add_argument(
        "--mail-login-name",
        required=True,
        help="Der Benutzername für den Mail-Login."
    )
    parser.add_argument(
        "--mail-login-password",
        required=True,
        help="Das Passwort für den Mail-Login."
    )

    # Optionale Argumente
    parser.add_argument(
        "--csv-topics",
        default="",
        help="Pfad zu einer CSV-Datei, die zu verarbeitende Themen enthält."
    )
    parser.add_argument(
        "--output-file",
        default="output.csv",
        help="Der Name der Ausgabedatei (Standard: output.txt)."
    )
    parser.add_argument(
        "--mail-directory",
        default="INBOX",
        help="Das Verzeichnis auf dem Mailserver, das verarbeitet werden soll."
    )

    # Argumente parsen
    args = parser.parse_args()

    str_server_domain = args.server_domain
    str_mail_login_credentials = [args.mail_login_name, args.mail_login_password]
    str_csv_topics = args.csv_topics
    str_filename_csv = args.output_file
    str_mail_directory = args.mail_directory

    #login to server
    mail = imaplib.IMAP4_SSL(str_server_domain)
    mail.login(str_mail_login_credentials[0], str_mail_login_credentials[1])
    mail.select(str_mail_directory)

    typ, data = mail.search(None, 'ALL')

    csv_content = []
    csv_content.append(str_csv_topics + "\n")


    #parse emails
    for num in data[0].split():
        try:
            typ, msg_data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            content = msg.get_payload(decode=True).decode('utf-8')
            start_index = content.find('CSV:') + 6
            if start_index >= 6:
                clean_text = content[start_index:]
                csv_content.append(clean_text)
        except Exception as e:
            print("Error in message parsing: " + str(e) + "\n")
            logger.info(msg)
            print("written problematic message to log")

    with open(str_filename_csv, 'w', newline='\n') as csvfile:
        for line in csv_content:
            try:
                csvfile.write(str(filter_text(line).split('--')[0]) + '\n')
            except Exception as e:
                print("Error occurred while writing line to CSV:", e)


if __name__ == "__main__":
    main()

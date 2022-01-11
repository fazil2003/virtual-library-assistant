
def send_mail(user_mail):

    # Python code to illustrate Sending mail with attachments 
    # from your Gmail account  

    # libraries to be imported 
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "alloasktechnologies@gmail.com"
    toaddr = user_mail

    # instance of MIMEMultipart 
    msg = MIMEMultipart()

    # storing the senders email address   
    msg['From'] = fromaddr

    # storing the receivers email address  
    msg['To'] = toaddr

    # storing the subject  
    msg['Subject'] = "The book you were looking for is available in the library right now"

    # string to store the body of the mail 
    body = """Come and get your book quickly before others get
    <img src='http://ecampus.psgpolytech.ac.in/studzone/(S(jst4jbu2fp4qu5hyjsw5r5zg))/Images/psgtechlogo.jpg' />"""

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'html'))

    # open the file to be sent  
    # filename = "img.png"
    # attachment = open("/media/mohamedfazil/Projects/College/FinalYear/Email/img.png", "rb")

    # instance of MIMEBase and named as p 
    # p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form 
    # p.set_payload((attachment).read())

    # encode into base64 
    # encoders.encode_base64(p)

    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg' 
    # msg.attach(p)

    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security 
    s.starttls()

    # Authentication 
    s.login(fromaddr, "iwillwinthisworld")

    # Converts the Multipart msg into a string 
    text = msg.as_string()

    # sending the mail 
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session 
    s.quit()


send_mail("mohamedfazil463@gmail.com")
import smtplib, os, commands
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

def send_mail(send_to,directory,sid):
    msg = MIMEMultipart()
    msg['From'] = "labmelosh@gmail.com"
    msg['To'] = send_to
    msg['Subject'] = 'Contents of directory %s' % os.path.abspath(directory)

    msg.attach( MIMEText("Here is the simulation you ran.") )
    tar_file = "%s.tar" % sid
    status,output = commands.getstatusoutput("tar cf %s %s" % (tar_file,directory))
    assert status is 0,status
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(tar_file,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % tar_file)
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('labmelosh@gmail.com','scine-model')
    server.sendmail(msg['From'],msg['To'], msg.as_string())
    server.quit()
    os.remove(tar_file)

if __name__ == '__main__':
    send_mail("aashidham@gmail.com","all","213r4")

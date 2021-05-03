
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


#def notify_message_to_given_email_list(posted_by,email_list,message):
def notify_message_to_given_email_list(user_id,user_email,user_message,email_list,id_list,last_email_sent_time_list):
    
    #Email body.
    plain_text = "Hi,\nThis is the plain text version of this Email.\nHere is a link that is for testing:\nhttps://amp.dev/documentation/guides-and-tutorials/start/create_email/?format=email"


    html = """
    <html>
    <head>
    <meta charset="utf-8">    
    </head>
    <body>
        <p>Hi!<br>
        <h1>Hello, I am an HTML MAIL!!!!</h1>
        </p>
    </body>
    </html>
    """

    html_amp = """
  
<!doctype html>
<html ⚡4email data-css-strict>
<head>
  <meta charset="utf-8">
  <script async custom-element="amp-form" src="https://cdn.ampproject.org/v0/amp-form-0.1.js"></script>
  <script async custom-template="amp-mustache" src="https://cdn.ampproject.org/v0/amp-mustache-0.2.js"></script>
  <script async custom-element="amp-list" src="https://cdn.ampproject.org/v0/amp-list-0.1.js"></script>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp4email-boilerplate>body{visibility:hidden}</style>
</head>
<body>
  Hello, <b>AMP4EMAIL</b> world.
  <hr>email_list,last_email_sent_time_listemail_list,email_list,last_email_sent_time_list,last_email_sent_time_listlast_email_sent_time_list
    <br>
      USER : <b>posted_by</b>
    <br>
      MESSAGE : message
    <hr>

    <amp-list id="myAmpList" layout="fixed-height" height="400" src="%s/user/get_last_one_hour_msg?email=%s&_id=%s" binding="no">
      <template type="amp-mustache">
          <div class="product">
              <div>
                <div>{{email}}</div>
                <div>{{message}}</div>
                <div>{{timestamp}}</div>
              </div>
          </div> 
        <hr>
      </template> 
    </amp-list>

    <form method="post" action-xhr='%s/user/receive_response_from_email?email=%s&_id=%s&time=%s'>
      
      <div submit-success>
        <template type="amp-mustache">
          <br>
          USER : <b>{{user}}</b>
          <br>
            MESSAGE : {{message}}
          <hr>
        </template>
      </div>
    
      <div class="m1" id="step2" >
        <label class="block" for="info">Would you like to reply?</label>
        <textarea class="block" id="message_from_email" name="message_from_email" rows="3"></textarea>
      </div>
      <input type="submit" value="send">
      <input type="reset" value="Clear">

      <div submitting>
         Form submitting... Thank you for waiting
      </div>
      <div submit-error>
        <template type="amp-mustache">
          Oops! error.
        </template>
      </div>


    </form>
</body>
</html>"""
    updated_last_email_sent_time_list=[]
    base_url='https://39fcd39ef714.ngrok.io'
    for recipent_email,recipent_id,time in zip(email_list,id_list,last_email_sent_time_list):
      if not time=='NA' and datetime.datetime.now()-time< datetime.timedelta(minutes = 5):
        updated_last_email_sent_time_list.append(time)
        continue
      updated_last_email_sent_time_list.append(datetime.datetime.now())
      fromm='p81252@gmail.com'
      to=recipent_email#'priyal81252@gmail.com'
      #to='ampforemail.whitelisting@gmail.com'
      print("from :",fromm,' ----------- ',"to : ", to, '----- msg : ',user_message)

      #Main Mimetype
      msg = MIMEMultipart('alternative')
      msg['Subject'] = "AMP Email"
      msg['From'] = fromm
      msg['To'] = recipent_email

      #Important: Some email clients only render the last MIME part, so it is
      #recommended to place the text/x-amp-html MIME part before the text/html.
      part1 = MIMEText(plain_text, 'plain')
      part2 = MIMEText(html_amp%(base_url,recipent_email,recipent_id,base_url,recipent_email,recipent_id,datetime.datetime.now()), 'x-amp-html')
      part3 = MIMEText(html, 'html')

      msg.attach(part1)
      msg.attach(part2)
      msg.attach(part3)

      s = smtplib.SMTP('smtp.gmail.com',587)
      s.starttls()
      s.login(fromm, "tanishqjain01")
      s.sendmail(fromm, to, msg.as_string().encode('utf-8'))
      s.quit()
    print("all emails have been sent")
    #print(updated_last_email_sent_time_list)
    return updated_last_email_sent_time_list


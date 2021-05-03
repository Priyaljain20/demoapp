import flask
from flask import Flask,request,jsonify,make_response
from flask_mail import Mail, Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)

@app.route('/')
def hello():
    fromm='p81252@gmail.com'
    to='priyal81252@gmail.com'
    #to='ampforemail.whitelisting@gmail.com'

    #Main Mimetype
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "AMP Email"
    msg['From'] = fromm
    msg['To'] = to

    #Email body.
    plain_text = "Hi,\nThis is the plain text version of this Email.\nHere is a link that is for testing:\nhttps://amp.dev/documentation/guides-and-tutorials/start/create_email/?format=email"


    html = """\
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


    html_amp = """\
  
<!doctype html>
<html ⚡4email data-css-strict>
<head>
  <meta charset="utf-8">
  <script async custom-element="amp-form" src="https://cdn.ampproject.org/v0/amp-form-0.1.js"></script>
  <script async custom-template="amp-mustache" src="https://cdn.ampproject.org/v0/amp-mustache-0.2.js"></script>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp4email-boilerplate>body{visibility:hidden}</style>
</head>
<body>
  Hello, AMP4EMAIL world.
  <div>
      <amp-img class="m1" width="600" height="314" layout="responsive" src="https://amp.dev/static/img/sharing/default-600x314.png"></amp-img>
      <p>It’s been a busy few days at the latest AMP conference. We hope you had a good time!</p>
    </div>

    <hr>

    <form method="post" action-xhr='"""+'https://3776bf8b77f4.ngrok.io/reply?email=%s'+"""'>
      
      <div class="m1" id="step2" >
        <label class="block" for="info">Would you like to tell us more?</label>
        <textarea class="block" id="info" name="name" rows="5"></textarea>
      </div>
      <input type="submit" value="Send feedback">
      <input type="reset" value="Clear">

      <div submitting>
          Form submitting... Thank you for waiting 1.{{name}} 2.  
      </div>
      <div submit-success>
        <template type="amp-mustache">
          Success! Thanks {{message}} {{severity}} {{name}}
        </template>
      </div>
      <div submit-error>
        <template type="amp-mustache">
          Oops! {{message}}, {{severity}}.
        </template>
      </div>

    </form>
  
</body>
</html>"""

    #Important: Some email clients only render the last MIME part, so it is
    #recommended to place the text/x-amp-html MIME part before the text/html.
    part1 = MIMEText(plain_text, 'plain')
    #part2 = MIMEText(html_ampo, 'x-amp-html')
    part2 = MIMEText(html_amp%to, 'x-amp-html')
    part3 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)
    msg.attach(part3)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromm, "tanishqjain01")
    s.sendmail(fromm, to, msg.as_string().encode('utf-8'))
    s.quit()

    return 'Hello, World!'


@app.route('/reply',methods=['post'])
def reply():
  print(request)
  print(request.headers)
  print(request.values)
  print(request.args)
  print( 'yes got replyyyyyyyyy')
  #print(request.params)    

  response = make_response(
      jsonify(
          {"message": "returned from api", "severity": "danger"}
      ),
      200,
  )
  response.headers["Content-Type"] = "application/json"
  response.headers["Access-Control-Allow-Credentials"]="true"
  response.headers["Access-Control-Allow-Origin"] = "*"
  response.headers["AMP-Access-Control-Allow-Source-Origin"] = request.args["__amp_source_origin"]
  response.headers["Access-Control-Expose-Headers"] = "AMP-Access-Control-Allow-Source-Origin"
  # response.headers["AMP-Redirect-To"] = "https://www.google.com/"
  # response.headers["Access-Control-Expose-Headers"] = "AMP-Redirect-To, AMP-Access-Control-Allow-Source-Origin"
  return response

@app.route('/get_pat_one_hour_messages')
def get_pat_one_hour_messages():
  print(request)
  print(request.headers)
  print(request.values)
  print(request.args)
  print( 'yes got replyyyyyyyyy')
  #print(request.params)    

  response = make_response(
      jsonify(
          {"items": [{"email":"user5@gmail.com","message":"hello","timestamp":"Mon, 12 Apr 2021 09:39:36 GMT"},{"email":"user5@gmail.com","message":"my name is user5","timestamp":"Mon, 19 Apr 2021 11:08:34 GMT"},{"timestamp":"lala"}]
}
      ),
      200,
  )
  response.headers["Content-Type"] = "application/json"
  response.headers["Access-Control-Allow-Credentials"]="true"
  response.headers["Access-Control-Allow-Origin"] = "*"
  response.headers["AMP-Access-Control-Allow-Source-Origin"] = request.args["__amp_source_origin"]
  response.headers["Access-Control-Expose-Headers"] = "AMP-Access-Control-Allow-Source-Origin"
  return response
  



if __name__ == '__main__':
    app.run()
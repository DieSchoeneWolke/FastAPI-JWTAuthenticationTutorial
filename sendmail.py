import os
import smtplib
from email.message import EmailMessage

email = os.getenv("email")
password = os.getenv("password")



def send_mail(to, token, username, email=email, password=password):
    msg = EmailMessage()
    msg.add_alternative(
        f"""\
<html>
  <head>
    <title>Login</title>
  </head>
  <body>
    <div id="box">
      <h2> Welcome {username},</h2> 
        <p> please click on the following link 
            <a href="http://localhost:8000/verify/{token}"></a> 
            to complete your registration!
        </p>
      </form>
    </div>
  </body>
</html>

<style>
  #box {{
    margin: 0 auto;
    max-width: 500px;
    border: 1px solid black;
    height: 200px;
    text-align: center;
    background: lightgray;
  }}

  p {{
    padding: 10px 10px;
    font-size: 18px;
  }}

  .inline {{
    display: inline;
  }}

  .link-button {{
    background: none;
    border: none;
    color: blue;
    font-size: 22px;
    text-decoration: underline;
    cursor: pointer;
    font-family: serif;
  }}
  .link-button:focus {{
    outline: none;
  }}
  .link-button:active {{
    color: red;
  }}
</style>
    """,
        subtype="html",
    )

    msg["Subject"] = "Activation of your account"
    msg["From"] = email
    msg["To"] = to

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL("smtp-relay.brevo.com", 587)
    server.login(email, password)
    server.send_message(msg)
    server.quit()
import re
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from tasks.sample_tasks import ProductsManager
from django.views.decorators.csrf import csrf_exempt
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




class ProductsCron():

    def __init__(self, list_of_products):
        self.list_of_products = list_of_products
       

    def runCron(self, type):
        self.list_of_products = serializers.serialize(
            'json', ProductsManager().get_queryset())
        print("Cron Is Running At Every 1 minute")
        return HttpResponse(self.list_of_products, content_type="application/json")

    def run_task_cron_def(self):
        inventory_products = serializers.serialize(
            'json', ProductsManager().get_queryset())
        # convert string to  object
        json_object = json.loads(inventory_products)
        if (len(json_object) > 0):
            for x in range(len(json_object)):
                if (json_object[x]["fields"]["stocks"] <= '10'):
                    stock_status = serializers.serialize(
                        'json', ProductsManager().get_stocks(str(json_object[x]["fields"]["stocks"])))
                    stocks = str(json.loads(stock_status)
                                 [x]["fields"]["stocks"])
                    title = str(json.loads(stock_status)[x]["fields"]["title"])
                    price = str(json.loads(stock_status)[x]["fields"]["price"])
                    return self.sendEmail(stocks, title, price)
        # print("run_task_cron_def Cron Is Running At Every 1 minute")

    def sendEmail(self, stocks, title, price):
        text = f'This Product - {title} of Price {price} is left only {stocks}..'
        from_email = 'pallavidapriya75@gmail.com'
        to_emails = ['priyaarshinipallavi@gmail.com',
                     'htfhfhfhfh#gamil.com', 'writerpro2025@gmail.com']
        emails_valid_invalid = self.validate_email(to_emails)
        print("Successfully did not sent email message to %s: It is invalid mail" %
              (", ".join(emails_valid_invalid[1])))
        subject = 'Inventory Goods Update'
        assert isinstance(emails_valid_invalid[0], list)
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(emails_valid_invalid[0])
        msg['Subject'] = subject
        txt_part = MIMEText(text, 'plain')
        msg.attach(txt_part)

        html_part = MIMEText(
            "This Product - {0} of Price {1} is left only {2}..".format(title, price, stocks))
        msg.attach(html_part)
        msg_str = msg.as_string()

        return self.send_mail(from_email, emails_valid_invalid[0], msg_str)

    def validate_email(self, emails):
        valid_emails = []
        invalid_emails = []
        for email in emails:
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                valid_emails.append(email)
            else:
                invalid_emails.append(email)
        return valid_emails, invalid_emails
    def test_conn_open(self, conn):
        try:
            status = conn.noop()[0]
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        return True if status == 250 else False
    def send_mail(self, from_email, to_emails, msg_str):
        
        try:
            returnable = ''
            print("this is hittiing here")
            username = 'pallavidapriya75@gmail.com'
            password = 'rrfz dfhp hrzr mlxz'
            server = smtplib.SMTP(host='smtp.gmail.com', port=587)
            # server = smtplib.SMTP(host='smtp.gmail.com', port=584)
            if not self.test_conn_open(server):
                returnable = f"An error occurred: Cannot assign requested address"
                raise OSError ("Cannot assign requested address")
               
                
            server.ehlo()
            server.starttls()
            server.login(username, password)
            print("Email Successfully sent  to %s: For a product inventory update" %
                  ", ".join(to_emails))
            for email in to_emails:
                server.sendmail(
                    from_email, email,  msg_str)
            returnable = "Email Successfully sent  to %s: For a product inventory update" %", ".join(to_emails)
            return returnable    
        except Exception as error:
            returnable = f"An error occurred: {error}"
            return returnable
        # f"An error occurred: {e}"

    def returnHomePPage(self, request):
        return render(request, "home.html", {'products': self.list_of_products})

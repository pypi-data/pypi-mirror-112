from notifier.controller import NotificationController
import requests
import json
from utils import exceptions


class Email(NotificationController):

    def __init__(self, config = None):
        
        self._requirement = {
            "required": {"uidx" : "str", "subject" : "str", "html_body" : "str", "endpoint" : "str", "template_name" : "str"}
        }

        if config:
            f = open(config)
        else:
            f = open("providers/config.json")

        config = json.load(f)
        email_config = config['email']

        self.endpoint = email_config['endpoint']
        self.header = email_config['header']
        f.close()

    # provides users with infoormation regarding input format
    @property
    def required(self) -> dict:
        return json.dumps(self._requirement, indent=4)

    # validate data based on the standard schema
    def _validate_data(self, **data) -> bool:
        schema = self._requirement['required']
        schema_keys = list(schema.keys())
        schema_keys.sort()
        input_keys = list(data.keys())
        input_keys.sort()
        return schema_keys == input_keys

    # raises InvalidInput exception if validation fails else builds the email content
    def _process_data(self, **data):

        if self._validate_data(**data):
            return self._build_data(data)
        else:
            raise exceptions.InvalidInput

    # extract information from the input
    def _build_data(self, data) -> None:
        self.uidx = data['uidx']
        self.subject = data['subject']
        self.html_body = data['html_body']
        self.endpoint = data['endpoint']
        self.template_name = data['template_name']

    # sends email based on uidx
    def send_uidx_email(self):

        # Templating engine
        payload = {
            "tenantId": 2297,
            "to": self.uidx,
            "templateName": self.template_name,
            "renderPairs": {
                "subject": self.subject,
                "description": self.html_body
            }
        }

        # Curl request to CRM/UCP
        # Status report
        try:
            response = requests.request('POST', self.endpoint, data=json.dumps(payload), headers = self.header, timeout=3)

            # Success
            if response.status_code == 200:
                report = {
                    'statusCode' : 200,
                    'statusMessage' : f"Message sent successfully to uidx : {self.uidx}",
                    'statusType' : 'SUCCESS',
                }
                return json.dumps(report, indent = 4)

        except requests.ConnectTimeout:
            response = ""
            raise exceptions.EmailExceptions(self.uidx, self.endpoint, response, connect_timeout = True)
        
        raise exceptions.EmailExceptions(self.uidx, self.endpoint, response)

    # overridden abstract method from base class
    def _send_notification(self):
        try:
            res = self.send_uidx_email()
            return res
        except exceptions.EmailExceptions as e:
            raise e
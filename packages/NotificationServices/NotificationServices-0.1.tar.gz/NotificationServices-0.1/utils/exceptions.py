import json

# Custom exceptions for email
class EmailExceptions(Exception):

    def __init__(self, uidx, endpoint, response, connect_timeout = False):
        self.response = response
        self.uidx = uidx
        self.endpoint = endpoint
        self.connect_timeout = connect_timeout
        super().__init__(self.response)
    
    def __str__(self):

        if self.connect_timeout:
            report = {
                'statusCode': 408,
                'statusMessage' : f"Message sent successfully to uidx {self.uidx}",
                'statusType' : "ERROR",
                'response' : ["channel : slack", "errorMeassage : Connection timed out"]
            }
            return json.dumps(report, indent = 4)

        report = {
            'statusCode' : self.response.status_code,
            'statusMessage' : f"Unable to send message to uidx: {self.uidx}",
            'statusType' : "ERROR",
            'response' : ["channel = slack"]
        }

        return json.dumps(report, indent=4)


# Custom exceptions for slack
class SlackExceptions(Exception):
    
    def __init__(self, slack_url, response, connect_timeout = False):
        self.slack_url = slack_url
        self.response = response
        self.connect_timeout = connect_timeout
        super().__init__(self.response)
    
    def __str__(self):

        # Getting channel_id from slack_url
        channel_id = self.slack_url.split('/')
        if self.connect_timeout:
            report = {
                'statusCode' : self.status_code,
                'statusMessage' : f"Unable to send message to slack channel: {channel_id[5]}",
                'statusType' : "ERROR",
                'response' : ["channel = slack"]
                
            }
            return json.dumps(report, indent=4)

        
        status_code = self.response.status_code
        report = str(self.response.text)

        # Failure
        report = {
            'statusCode' : status_code,
            'statusMessage' :f"Unable to send message to slack channel: {channel_id[5]}",
            'statusType' : "ERROR",
            'response' : ["channel = slack"]
        }

        return json.dumps(report, indent = 4)


class InvalidInput(Exception):
    def __str__(self) -> str:
        return "Invalid Input"
# {
#   "statusCode": 1001,
#   "statusMessage": "Data successfully processed",
#   "statusType": "SUCCESS",
#   "seasons": [
#     "Summer-2020",
#     "Spring-2021",
#     "Summer-2021",
#     "Spring-2019",
#     "Fall-2021"
#   ]
# }


# --------
# Error response :
# {
#     "statusCode": 400,
#     "statusType": "ERROR",
#     "statusMessage": "access_token is invalid"
# } 
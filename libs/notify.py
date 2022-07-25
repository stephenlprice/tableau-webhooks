from twilio.rest import Client

# twilio variables
twilioSID = env_dict["TWILIO_ACCOUNT_SID"]
twilioAuthToken = env_dict["TWILIO_AUTH_TOKEN"]
fromNumber = env_dict["TWILIO_FROM_NUMBER"]
toNumber = env_dict[""]
fromWhatsApp = env_dict["WHATSAPP_FROM"]
toWhatsApp = env_dict["WHATSAPP_TO"]

# msgStr = f"Datasource Refresh failed\n\tName:{dataSource.name}\n\tDescription:{dataSource.description}\n\tLast updated: {dataSource.updated_at}\n"

def sms(env_dict):
  twilioClient = Client(env_dict['TWILIO_ACCOUNT_SID'], env_dict['TWILIO_AUTH_TOKEN'])
  msgStr = ''
  textMessage = twilioClient.messages.create(
    body = msgStr,
    from_ = env_dict['TWILIO_FROM_NUMBER'],
    to = env_dict['TWILIO_TO_NUMBER']
  )
  # logFile.write(f"Text message SID: {textMessage.sid}\nSending SMS message from {fromNumber} to {toNumber}\n")




whatsappMessage = twilioClient.messages.create(
  body = msgStr,
  from_ = fromWhatsApp,
  to = toWhatsApp
)
# logFile.write(f"Whatsapp message SID: {whatsappMessage.sid}\nSending Whatsapp message from {fromWhatsApp} to {toWhatsApp}\n")

call = twilioClient.calls.create(
  twiml = f"<Response><Say>{msgStr}</Say></Response>",
  from_ = fromNumber,
  to = toNumber 
)

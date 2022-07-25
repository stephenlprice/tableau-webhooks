from twilio.rest import Client

# msgStr = f"Datasource Refresh failed\n\tName:{dataSource.name}\n\tDescription:{dataSource.description}\n\tLast updated: {dataSource.updated_at}\n"

def sms(env_dict, msgStr):
  twilioClient = Client(env_dict['TWILIO_ACCOUNT_SID'], env_dict['TWILIO_AUTH_TOKEN'])
  textMessage = twilioClient.messages.create(
    body = msgStr,
    from_ = env_dict['TWILIO_FROM_NUMBER'],
    to = env_dict['TWILIO_TO_NUMBER']
  )
  # logFile.write(f"Text message SID: {textMessage.sid}\nSending SMS message from {fromNumber} to {toNumber}\n")

def whatsapp(env_dict, msgStr):
  twilioClient = Client(env_dict['TWILIO_ACCOUNT_SID'], env_dict['TWILIO_AUTH_TOKEN'])
  whatsappMessage = twilioClient.messages.create(
    body = msgStr,
    from_ = env_dict['WHATSAPP_FROM'],
    to = env_dict['WHATSAPP_TO']
  )
  # logFile.write(f"Whatsapp message SID: {whatsappMessage.sid}\nSending Whatsapp message from {fromWhatsApp} to {toWhatsApp}\n")

def call(env_dict, msgStr):
  twilioClient = Client(env_dict['TWILIO_ACCOUNT_SID'], env_dict['TWILIO_AUTH_TOKEN'])
  call = twilioClient.calls.create(
    twiml = f"<Response><Say>{msgStr}</Say></Response>",
    from_ = env_dict['TWILIO_FROM_NUMBER'],
    to = env_dict['TWILIO_TO_NUMBER']
  )

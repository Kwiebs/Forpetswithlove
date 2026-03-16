#!/usr/bin/env python3
import os
from agentmail import AgentMail
from dotenv import load_dotenv

os.chdir('/home/kweeb/.openclaw/workspace')
load_dotenv()

mail = AgentMail(api_key=os.getenv('AGENTMAIL_API_KEY'))
mail.send(
    to='ambrosio@agentmail.to',
    subject='✅ AgentMail Test',
    body='This is a test message from OpenClaw AgentMail setup.'
)

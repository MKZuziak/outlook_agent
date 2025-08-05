from exchangelib import Credentials, Account, DELEGATE
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

# STEP 1: Connect to Outlook
def connect_to_outlook():
    creds = Credentials(EMAIL, PASSWORD)
    account = Account(
        primary_smtp_address=EMAIL,
        credentials=creds,
        autodiscover=True,
        access_type=DELEGATE,
    )
    return account

# STEP 2: Tool – Read the latest unread email
@tool
def read_latest_email(query: str) -> str:
    """
    Reads the most recent unread email from Outlook.
    The input is ignored; it just returns latest message.
    """
    account = connect_to_outlook()
    inbox = account.inbox
    messages = inbox.filter(is_read=False).order_by('-datetime_received')[:1]
    if not messages:
        return "No unread emails."
    msg = messages[0]
    return f"From: {msg.sender.email_address}\nSubject: {msg.subject}\nBody:\n{msg.body}"

# STEP 3: Tool – Confirm and send reply manually
@tool
def confirm_and_send_reply(reply: str) -> str:
    """
    Shows the reply and asks the user for confirmation.
    If confirmed, sends the email reply.
    """
    account = connect_to_outlook()
    inbox = account.inbox
    messages = inbox.filter(is_read=False).order_by('-datetime_received')[:1]
    if not messages:
        return "No message to reply to."
    
    msg = messages[0]
    print("\n--- Suggested Reply ---")
    print(reply)
    confirm = input("\nSend this reply? (y/n): ")
    if confirm.lower() != 'y':
        return "Reply not sent."
    
    m = msg.reply()
    m.body = reply
    m.send()
    return "Reply sent."

# STEP 4: Define tools for the agent
tools = [
    Tool.from_function(read_latest_email),
    Tool.from_function(confirm_and_send_reply)
]

# STEP 5: Define the agent
llm = ChatOpenAI(temperature=0, model="gpt-4")  # or "gpt-3.5-turbo"
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# STEP 6: Run the agent with a user prompt
if __name__ == "__main__":
    query = "Read my latest email and prepare a polite reply."
    result = agent.run(query)
    print("\nAgent Result:\n", result)

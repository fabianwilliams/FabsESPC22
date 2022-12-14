import configparser
from Graph import Graph

def main():
    print('ESPC Fabian & Gabby Williams Python Graph Session\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. List my inbox')
        print('3. Send mail')
        print('4. List users (requires app-only)')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        if choice == 0:
            print('Goodbye...')
        elif choice == 1:
            display_access_token(graph)
        elif choice == 2:
            list_inbox(graph)
        elif choice == 3:
            send_mail(graph)
        elif choice == 4:
            list_users(graph)
        else:
            print('Invalid choice!\n')

def greet_user(graph: Graph):
    user = graph.get_user()
    print('Hello,', user['displayName'])
    # For Work/school accounts, email is in mail property
    # Personal accounts, email is in userPrincipalName
    print('Email:', user['mail'] or user['userPrincipalName'], '\n')

def display_access_token(graph: Graph):
    token = graph.get_user_token()
    print('User token:', token, '\n')

def list_inbox(graph: Graph):
    message_page = graph.get_inbox()

    # Output each message's details
    for message in message_page['value']:
        print('Message:', message['subject'])
        print('  From:', message['from']['emailAddress']['name'])
        print('  Status:', 'Read' if message['isRead'] else 'Unread')
        print('  Received:', message['receivedDateTime'])

    # If @odata.nextLink is present
    more_available = '@odata.nextLink' in message_page
    print('\nMore messages available?', more_available, '\n')

def send_mail(graph: Graph):
    # Send mail to the signed-in user
    # Get the user for their email address
    user = graph.get_user()
    #user_email = user['mail'] or user['userPrincipalName']
    user_email = 'gabbyg@fabster.onmicrosoft.com'

    graph.send_mail('Jada & Fabian says Hi from ESPC22', 'Hello Attendees in our Denmark Session!', user_email)
    print('Mail sent.\n')

def list_users(graph: Graph):
    users_page = graph.get_users()

    # Output each users's details
    for user in users_page['value']:
        print('User:', user['displayName'])
        print('  ID:', user['id'])
        print('  Email:', user['mail'])

    # If @odata.nextLink is present
    more_available = '@odata.nextLink' in users_page
    print('\nMore users available?', more_available, '\n')

# Run main
main()
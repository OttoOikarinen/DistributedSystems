import xmlrpc.client

# Proxy for the address
address = 'http://localhost:8000'
proxy = xmlrpc.client.ServerProxy(address)

print("Connected to server at " + address)

# Function to add a new note or append data to an existing one
def add_note(topic, text, timestamp):
    response = proxy.process_input(topic, text, timestamp)
    print(response)

# Function to query Wikipedia for additional information on a topic
def search_wikipedia(topic):
    response = proxy.query_wikipedia(topic)
    print(response)

# User interaction here in endless loop.
while True:
    print("1: Add/Append note")
    print("2: Search Wikipedia")
    print("3: Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        topic = input("Enter topic you want to add or append: ")
        text = input("Enter text: ")
        timestamp = input("Enter timestamp: ")
        add_note(topic, text, timestamp)
    elif choice == '2':
        topic = input("Enter search term for Wikipedia search: ")
        search_wikipedia(topic)
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please try again.")
    print("\n")

import socket
import thread
import sys
import os
import time
import json
import ast

products = {}
idCount = 100
server1Products = {}
server2Products = {}
server3Products = {}

serverValues = ['', '', '', '']

# SERVER HOST AND SERVER
HOST = ''
PORT = 50004
serverValue = 4

newProduct = {}

server1Host = '127.0.0.1'
server1Port = 50001
server2Host = '127.0.0.1'
server2Port = 50002
server3Host = '127.0.0.1'
server3Port = 50003

#Clocks
clockIterarion = 4
localClock = 11
globalClock = 0

serversQuantity = 4
testServers = {}

def Product(productCode = 0, productName = '', productValue = 0, productAvailability = 0):
	return {'code': productCode, 'name': productName, 'value': productValue, 'availability': productAvailability}

def getNewProduct(connection):
    try:
		connection.send("SENDNEWPRODUCT")
		serverNumber = connection.recv(1)
		print("getting information from server" + serverNumber)
		serverNumber = int(serverNumber)

		global globalClock
		global localClock
		globalClock = connection.recv(2)
		globalClock = int(globalClock)
		if globalClock > (localClock + 1):
			localClock = globalClock
		else:
			localClock += 1
		connection.send(str(localClock))

		print '\nProduct:',
		information = connection.recv(1024)
		newProduct.update({serverNumber: information})
		information = ast.literal_eval(json.loads(information))
		print information

		serverValues[serverNumber - 1] = information

    except Exception as msg:
        connection.send("ERROR")
        #File Error.
        print("Error message: " + str(msg))
        return

def sendServerValues(connection):
    try:
        connection.send("GETVALUES");
        print "Sending Server Values"
        connection.send(str(serverValue))

        connection.send(str(server4Values[0]))
        connection.send(str(server4Values[1]))
        connection.send(str(server4Values[2]))
        connection.send(str(server4Values[3]))

        print "Finish Sending Values"

    except Exception as msg:
        connection.send("ERROR")
        #File Error.
        print("Error message: " + str(msg))
        return

def sendNumber(connection):
    print "Sending server number"
    connection.send(str(serverValue))
    time.sleep(1)
    print "Sending server value"
    connection.send(str(serverValue))

def connected(connection, client):
	###  Function that starts a new thread for the connection
	while True:
		msg = connection.recv(1024)
		if (msg == "GETNUMBER"):
			print("Connection started with " + str(client))
			getNumber(connection)
		elif (msg == "GETNEWPRODUCT"):
			print("Connection started with " + str(client))
			getNewProduct(connection)
		elif (msg == "SENDSERVERVALUES"):
			print("Connection started to send server values")
			sendServerProduct(connection)
		elif (msg == "SENDNUMBER"):
			print("Connection started with " + str(client))
			sendNumber(connection)
		else:
			connection.close()
			break

	thread.exit()

def menu():
    print '----------------------------------------'
    print '---- 1 -> Update Value of a Product ----'
    print '---- 2 -> Get Product Situation     ----'
    print '---- 3 -> Create new Product        ----'
    print '---- 4 -> List Local Products       ----'
    print '---- 5 -> List Global Products      ----'
    print '----------------------------------------'

def feedLocalStructure():
    for i in xrange(100):
        products.update({i: Product(i, "Product "+str(i), 5*i, 1)})
        server1Products.update({i: Product(i, "Product "+str(i), 5*i, 1)})
        server2Products.update({i: Product(i, "Product "+str(i), 5*i, 1)})
        server3Products.update({i: Product(i, "Product "+str(i), 5*i, 1)})

def listLocalProducts():
	print '_____________________________'
	print '| ID | Name | Price | Stock |'
	for product in products:
		print '| ',
		print products[product]['code'],
		print ' | ',
		print products[product]['name'],
		print ' | ',
		print products[product]['value'],
		print ' | ',
		print products[product]['availability'],
		print ' |'

def listGlobalProducts(serverId):
	print '_____________________________'
	print '| ID | Name | Price | Stock |'
	for product in products:
		print '| ',
		print products[product]['code'],
		print ' | ',
		print products[product]['name'],
		print ' | ',
		print products[product]['value'],
		print ' | ',
		print products[product]['availability'],
		print ' |'

	for product in server1Products:
		print '| ',
		print products[product]['code'],
		print ' | ',
		print products[product]['name'],
		print ' | ',
		print products[product]['value'],
		print ' | ',
		print products[product]['availability'],
		print ' |'

	for product in server2Products:
		print '| ',
		print products[product]['code'],
		print ' | ',
		print products[product]['name'],
		print ' | ',
		print products[product]['value'],
		print ' | ',
		print products[product]['availability'],
		print ' |'

	for product in server3Products:
		print '| ',
		print products[product]['code'],
		print ' | ',
		print products[product]['name'],
		print ' | ',
		print products[product]['value'],
		print ' | ',
		print products[product]['availability'],
		print ' |'

# Create a socket that use IPV4 and TCP protocol
# Bind the port for this process conections
# Set the maximun number of queued connections
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origin = (HOST, PORT)

try:
    tcp.bind(origin)
    print("Binded")
except socket.error as SBE:
    print("Bind failed!")
    print(SBE)
    sys.exit()

tcp.listen(5)

print("TCP started and already listening...")

# Server accept connections until a keyboard interrupt
# If there is a keyboard interrupt, release the port

feedLocalStructure()
time.sleep(5)

server1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server3Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	server1Socket.connect((server1Host, int(server1Port)))
	print("Connected to 1!")

	server2Socket.connect((server2Host, int(server2Port)))
	print("Connected to 2!")

	server3Socket.connect((server3Host, int(server3Port)))
	print("Connected to 3!")

except socket.error as sem:
    print("ERROR: Couldn't connect.")
    print(sem)
    sys.exit()

# actualSocket.send("GETFILE")
# sendFile(host, port, filePath)

try:
    while True:
		localClock += clockIterarion
		connection, client = tcp.accept()

		# For every connect a new thread will be created
		thread.start_new_thread(connected, tuple([connection, client]))

except KeyboardInterrupt:
    print("\n\n--- TCP connection ended ---")
    tcp.close()
    sys.exit()

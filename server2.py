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
server3Products = {}
server4Products = {}

# SERVER HOST AND SERVER
HOST = ''
PORT = 50002
serverValue = 2

newProduct = {}

# OTHER SERVERS AND HOSTS
server1Host = '127.0.0.1'
server1Port = 50001
server3Host = '127.0.0.1'
server3Port = 50003
server4Host = '127.0.0.1'
server4Port = 50004

serverValues = ['', '', '', '']

#Clocks
clockIterarion = 2
localClock = 11
globalClock = 0

serversQuantity = 4
testServers = {}

def Product(productCode = 0, productName = '', productValue = 0, productAvailability = 0):
	return {'code': productCode, 'name': productName, 'value': productValue, 'availability': productAvailability}

def doByzantineAgreement():
	print "\nStarting Byzantine Agreement:"
	print "Server Values:"
	print serverValues

	count = 0
	percentage = 100/serversQuantity

	testServers = {}
	testServers.update({serverValues[0]: percentage})

	if serverValues[1] in testServers:
		testServers[serverValues[1]] += percentage
	else:
		testServers.update({serverValues[1]: percentage})

	if serverValues[2] in testServers:
		testServers[serverValues[2]] += percentage
	else:
		testServers.update({serverValues[2]: percentage})

	if serverValues[3] in testServers:
		testServers[serverValues[3]] += percentage
	else:
		testServers.update({serverValues[3]: percentage})

	for x in testServers:
		if testServers[x] >= 60:
			count += 1
			print "The new product is ok!"

def receiveServerValues(connection):
	serverNumber = int(connection.recv(8))
	serverObject = connection.recv(1024)
	serverValues[serverNumber - 1] = serverObject

def getAllValues():
    server1Socket.send("SENDSERVERVALUES")
    returnMessage = server1Socket.recv(1024)
    if (returnMessage == "GETVALUES"):
        print("Connection started with 2")
        receiveServerValues(server1Socket)

    server3Socket.send("SENDSERVERVALUES")
    returnMessage = server3Socket.recv(1024)
    if (returnMessage == "GETVALUES"):
        print("Connection started with 3")
        receiveServerValues(server3Socket)

    server4Socket.send("SENDSERVERVALUES")
    returnMessage = server4Socket.recv(1024)
    if (returnMessage == "GETVALUES"):
        print("Connection started with 4")
        receiveServerValues(server4Socket)

def getNewProduct(connection):
	try:
		connection.send("SENDNEWPRODUCT");
		serverNumber = connection.recv(8)
		print("getting information from server" + serverNumber)
		serverNumber = int(serverNumber)

		global globalClock
		global localClock
		globalClock = int(connection.recv(8))
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

		time.sleep(5)
		getAllValues()

	except Exception as msg:
		connection.send("ERROR")
		#File Error.
		print("Error message: " + str(msg))
		return

def sendServerProduct(connection):
    try:
		connection.send("GETPRODUCT")

		print "Sending server new product"
		connection.send(str(serverValue))

		time.sleep(1)

		data_string = json.dumps(str(newProduct).replace("'",'"')) #data serialized
		connection.send(data_string)
		print "Finish Sending Product"

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
		server3Products.update({i: Product(i, "Product "+str(i), 5*i, 1)})
		server4Products.update({i: Product(i, "Product "+str(i), 5*i, 1)})

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

	for product in server4Products:
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

time.sleep(5)

server1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server3Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server4Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	server1Socket.connect((server1Host, int(server1Port)))
	print("Connected to 1!")

	server3Socket.connect((server3Host, int(server3Port)))
	print("Connected to 3!")

	server4Socket.connect((server4Host, int(server4Port)))
	print("Connected to 4!")

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

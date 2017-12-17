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

newProducts = {}

# OTHER SERVERS AND HOSTS
server1Host = '127.0.0.1'
server1Port = 50001
server3Host = '127.0.0.1'
server3Port = 50003
server4Host = '127.0.0.1'
server4Port = 50004

serversQuantity = 4
testServers = {}

def Product(productCode = 0, productName = '', productValue = 0, productAvailability = 0):
	return {'code': productCode, 'name': productName, 'value': productValue, 'availability': productAvailability}

def getNewProduct(connection):
	try:
		connection.send("SENDNEWPRODUCT");
		serverNumber = connection.recv(8)
		print("getting information from server" + serverNumber)
		serverNumber = int(serverNumber)

		print '\nProduct:',
		information = connection.recv(1024)
		information = ast.literal_eval(json.loads(information))
		print information

		newProducts.update({serverNumber: information})
		if serverNumber == 1:
			time.sleep(5)

			server1Socket.send("GETNEWPRODUCT")
			returnMessage = server1Socket.recv(1024)
			if (returnMessage == "SENDNEWPRODUCT"):
				print("Connection started with 1")
				sendNumber(server1Socket)

			server3Socket.send("GETNEWPRODUCT")
			returnMessage = server3Socket.recv(1024)
			if (returnMessage == "SENDNEWPRODUCT"):
				print("Connection started with 3")
				sendNumber(server3Socket)

			server4Socket.send("GETNEWPRODUCT")
			returnMessage = server4Socket.recv(1024)
			if (returnMessage == "SENDNEWPRODUCT"):
				print("Connection started with 4")
				sendNumber(server4Socket)

		if serverNumber == 4:
			time.sleep(5)
			print server2Values

	except Exception as msg:
		connection.send("ERROR")
		#File Error.
		print("Error message: " + str(msg))
		return

def getNumber(connection):
    try:
        connection.send("SENDNUMBER");
        serverNumber = connection.recv(8)
        print("getting information from server" + serverNumber)
        serverNumber = int(serverNumber)

        print '\nValue:',

        information = connection.recv(8)
        information = int(information)
        print information

        server2Values[serverNumber-1] = information

        if serverNumber == 1:
            time.sleep(5)

            server1Socket.send("GETNUMBER")
            returnMessage = server1Socket.recv(1024)
            if (returnMessage == "SENDNUMBER"):
                print("Connection started with 1")
                sendNumber(server1Socket)

            server3Socket.send("GETNUMBER")
            returnMessage = server3Socket.recv(1024)
            if (returnMessage == "SENDNUMBER"):
                print("Connection started with 3")
                sendNumber(server3Socket)

            server4Socket.send("GETNUMBER")
            returnMessage = server4Socket.recv(1024)
            if (returnMessage == "SENDNUMBER"):
                print("Connection started with 4")
                sendNumber(server4Socket)

            time.sleep(30)
            msg = connection.recv(1024)
            if (msg == "SENDSERVERVALUES"):
                print("Connection started to send server values")
                sendServerValues(connection)

        if serverNumber == 4:
            time.sleep(5)
            print server2Values

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

time.sleep(20)

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
        connection, client = tcp.accept()

        # For every connect a new thread will be created
        thread.start_new_thread(connected, tuple([connection, client]))

except KeyboardInterrupt:
    print("\n\n--- TCP connection ended ---")
    tcp.close()
    sys.exit()

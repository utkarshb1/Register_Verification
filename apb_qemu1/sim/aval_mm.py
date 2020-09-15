from struct import *
import time
import os
class Aval_mm:

	WRITE=0
	READ=1
	IDLE=2
	DONE=3
	WRITE_RSP=4
	READ_RSP=5
	IDLE_RSP=6
	DONE_RSP=7
	ids = []


	"""docstring for Aval-mm"""
	def __init__(self, fifo, id = 0, version = 1,idcount = 0):
		self.fifo=fifo
		self.id=id
		self.version=version
		self.idcount=idcount
		print ("file opened successfully:\n")


	def write(self,address,*wdata):
		pkt_len = 16
		endian = 0x0f
		op = self.WRITE
		data_len = 4
		# print(" , ",wdata,address)
		request = pack("=BIHIBIIQI",endian,pkt_len,self.version,self.id,op,0,data_len,address,wdata[0])
		print("Write:  ", request)
		request = str(request,'Latin-1')
		print("Write Request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address, wdata[0]])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		time.sleep(1)

		Lines = ff_rd.readlines()
		read_value = int(str(int(Lines[-1].strip())),16)
		print(" ", wdata[0]," ",read_value)
		if read_value == wdata[0]:
			os.write(vf,int.to_bytes(1,1,byteorder='big',signed=False))
			print("Written: ",int.to_bytes(1,2,byteorder='big',signed=False))
		else:
			os.write(vf,int.to_bytes(0,1,byteorder='big',signed=False))
			print("Not Written: ",int.to_bytes(0,2,byteorder='big',signed=False))
		# if self.id <90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0


	def read(self,address):
		pkt_len=12
		endian=0x0f
		op =self.READ
		data_len =0
		request = pack("=BIHIBIIQ",endian,pkt_len,self.version,self.id,op,0,data_len,address)
		print("Read:  ", request)
		request = str(request,'Latin-1')
		# request = request.decode(encoding='Latin -1')
		print("Read request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		Lines = ff_rd.readlines()
		print(Lines[-1].strip())
		# for line in Lines:
		# 	print("Line: {}".format(line.strip()))
		# if self.id <90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0

	def ctrl_command(self):
		pkt_len = 0;
		endian=0x0f;
		op = self.DONE;
		request = pack("=BIHIB",endian,pkt_len,self.version,self.id, op)
		request = str(request,'Latin-1')
		# request = request.decode(encoding='Latin-1')
		print("Term Request => ", [endian, pkt_len, self.version, self.id, op])
		self.fifo.write(request)
		fi.flush()
		self.fifo.flush()
		self.id += 1
		# if self.id < 90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0
		# count = self.idcount
		# print(count)
		
		
fifopath = "qemu_apb_req.fifo"
read_path = "/tmp/pipe.in"
fifo_read = "/home/utk/Intern_Project/Register_Verification/apb_qemu1/testbench/data.txt"
verify_path = "/tmp/pipe.out"

#Check if fifo exists
if os.path.exists(read_path):
    os.remove(read_path)
if os.path.exists(verify_path):
    os.remove(verify_path)
os.mkfifo(read_path)
os.mkfifo(verify_path)
#Open Gnumeric
rf = os.open(read_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
vf = os.open(verify_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
ff_rd = open(fifo_read, 'r')
fi =open(fifopath,'w')
mm = Aval_mm(fi)

# mm.write(0x2C,0x55)
# time.sleep(2)
# mm.read(0x2C)

# time.sleep(2)
# os.read(rd_fifo,1024)#
while True:
	s = os.read(rf, 32)
	s = str(s,'latin-1')
	s = s.split(',')
	ope = int(s[0])
	if ope == 1:#Write
		addr = int(s[1],16)
		data = int(s[2],16)
		print (f"Address:{addr} and Data:{data}")
		mm.write(addr,data)
		time.sleep(1)
		# mm.read(0x2C)
		# break
	# elif ope == 0:#Read
		# addr = int(s[1])
# for i in range(0,12):
	# mm.write(0x2C, i)
	# mm.read(0x2C)

mm.ctrl_command()
fi.close()
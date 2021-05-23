import xmlrpc.client as cl

import sys

# # import xmlrpclib
#
# addr = "10.0.0.2"
# port = 8100
# # rhost = xmlrpclib.Server("http://" + addr + ":" + str(port))
# rhost = cl.ServerProxy("http://" + addr + ":" + str(port))
# # msg = rhost.str_get()
# # print(msg)
# # inp = ""
# print("Guess a number between 1 and 100")
# print()
# while 1:
#     # msg = rhost.str_get()
#     # print(msg)
#
#     inp = input(">")
#     msg = rhost.guess_number(int(inp))
#
#     print(msg)
#
# if "found" in msg:
#     sys.exit(0)
x = sys.argv[1]
port = "8100"
proxy = cl.ServerProxy("http://" + str(x) + ":8100")
num1 = 30
num2 = 20

# result = proxy.add(num1, num2)
# print(f"Result is : {result}")
ack, cpu_l = proxy.check_req(0.8, 0.2)
print(f"{ack},{cpu_l}")
# print(f"Server Answer-> status= {ack}, new_cpu_avail= {cpu_l}")
# print(round(cpu_l, 2))

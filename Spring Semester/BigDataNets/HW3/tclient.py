import xmlrpc.client as cl

import sys


# Get pass arguments when calling client
sip, current_cpu, new_req = sys.argv[1], sys.argv[2], sys.argv[3]

port = "8100"
proxy = cl.ServerProxy("http://" + str(sip) + ":8100")
# num1 = 30
# num2 = 20
# print(current_cpu, new_req)
# result = proxy.add(num1, num2)
# print(f"Result is : {result}")

ack, cpu_l = proxy.check_req(float(current_cpu), float(new_req))
print(f"{ack},{cpu_l}")

# print(f"Server Answer-> status= {ack}, new_cpu_avail= {cpu_l}")
# print(round(cpu_l, 2))

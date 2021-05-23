import xmlrpc.client as cl

import sys


# Get pass arguments when calling client
sip, current_cpu, new_req = sys.argv[1], sys.argv[2], sys.argv[3]

port = "8100"
proxy = cl.ServerProxy("http://" + str(sip) + ":8100")


ack, cpu_l = proxy.check_req(float(current_cpu), float(new_req))
print(f"{ack},{cpu_l}")

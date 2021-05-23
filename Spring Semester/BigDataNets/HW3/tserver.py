from xmlrpc.server import SimpleXMLRPCServer

# import socket
# import string
# import socketserver
# import os
# import sys
# from subprocess import Popen, PIPE
#
# x = int(sys.argv[1])
# tries = 0
#
#
# class SimpleThreadedXMLRPCServer(socketserver.ThreadingMixIn, SimpleXMLRPCServer):
#     allow_reuse_address = True


#
# class Functions:
#     # var_str = "yyyaaa"
#
#     def guess_number(self, n):
#         global tries
#         tries = tries + 1
#         if n > x:
#             msg = "Number is too high"
#         if n < x:
#             msg = "Number is too low"
#         if n == x:
#             msg = "You found the number in " + str(tries) + "tries. Congratulations!"
#             tries = 0
#         return msg
#
#     # def str_get():
#     #     return var_str
#
#
# if __name__ == "__main__":
#     port = 8100
#     server = SimpleThreadedXMLRPCServer(("", port))
#     server.register_instance(Functions())
#     print("Serever listening...")
#     server.serve_forever()


def add(num1, num2):
    return num1 + num2


class MyServer:
    # def __init__(self):
    #     self.cpu_avail = 1
    #     self.accepted = False

    def check_req(self, cpu_avail, cpu_req):
        if cpu_req <= cpu_avail:
            cpu_avail -= cpu_req  # update new avail cpu
            accepted = True
        else:
            accepted = False

        return (accepted, round(cpu_avail, 3))


server = SimpleXMLRPCServer(("", 8100))
print("server serving...")
# server.register_function(add, "add")
server.register_instance(MyServer())
server.serve_forever()

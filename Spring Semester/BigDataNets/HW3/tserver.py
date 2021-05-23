from xmlrpc.server import SimpleXMLRPCServer


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

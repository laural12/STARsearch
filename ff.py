import pyvisa
import pickle


# Input prompts for if you'd rather not edit this file directly
if input("Has the fieldfox IP address changed? [y/n]") == "y":
    ip = input("What is the fieldfox IP address?")
else:
    with open('ff_ip.pickle', 'rb') as handle:
        ip_pkl = pickle.load(handle)
    ip = ip_pkl["ip"]
#----------------------------------------------------------

# Otherwise just edit ip here:
# ip = "10.32.114.148"
#-----------------------------

rm = pyvisa.ResourceManager()
# rm.list_resources()
inst = rm.open_resource(f'TCPIP0::{ip}::inst0:INSTR')
print(inst.query('*IDN?'))




# cleanup to close
a = {"ip" : ip}
with open("ff_ip.pickle", "wb") as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

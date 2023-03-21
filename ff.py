import sys

# path = "/home/odroid/.local/lib/python3.10/site-packages"
path = "/home/laura/.local/lib/python3.8/site-packages"
sys.path.insert(0, path)

import pyvisa
import pickle
import time


# Input prompts for if you'd rather not edit this file directly
# if input("Has the fieldfox IP address changed? [y/n]") == "y":
#     ip = input("What is the fieldfox IP address?")
# else:
#     with open("ff_ip.pickle", "rb") as handle:
#         ip_pkl = pickle.load(handle)
#     ip = ip_pkl["ip"]
# ----------------------------------------------------------

# Otherwise just edit ip here:
ip = "192.168.0.1"
# -----------------------------

rm = pyvisa.ResourceManager()
# rm.list_resources()
inst = rm.open_resource(f"TCPIP0::{ip}::inst0:INSTR")
print(inst.query("*IDN?"))

# inst.write(
#     "CALC:MARK:FUNC:BAND:SPAN:AUTO 1"
# )  # Set the span of the marker (default: 5% of FF frequency span)
# # inst.query("CALC:MARK1:FUNC BPOW")
# inst.write(
#     "CALC:MARK1:STR 1"
# )  # Set marker 1 to track the peak signal (will automatically adjust center frequency to do so)

# print(inst.query("CALC:MARK1:STR?"))

# Set center freq
inst.write("FREQ:CENT 1.185e9")
# set iBW to be within 100kHz (narrow bandwidth)
inst.write("SENS:CME:IBW 100e3")

inst.write("SENS:MEAS:CHAN CHP")
print("Reading channel power")
print(
    inst.query("SENS:MEAS:CHAN?")
)  # Just prints 1, I think CHP is the first measurement
print(
    inst.query("CALC:MEAS:DATA?")
)  # This is the command that actually gives you info. Gives power, then PSD, in dB

# cleanup to close
inst.close()

a = {"ip": ip}
with open("ff_ip.pickle", "wb") as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

import pyvisa
import pickle


# Input prompts for if you'd rather not edit this file directly
if input("Has the fieldfox IP address changed? [y/n]") == "y":
    ip = input("What is the fieldfox IP address?")
else:
    with open("ff_ip.pickle", "rb") as handle:
        ip_pkl = pickle.load(handle)
    ip = ip_pkl["ip"]
# ----------------------------------------------------------

# Otherwise just edit ip here:
# ip = "10.32.114.148"
# -----------------------------

rm = pyvisa.ResourceManager()
# rm.list_resources()
inst = rm.open_resource(f"TCPIP0::{ip}::inst0:INSTR")
print(inst.query("*IDN?"))

inst.write(
    "CALC:MARK:FUNC:BAND:SPAN:AUTO 1"
)  # Set the span of the marker (default: 5% of FF frequency span)
# inst.query("CALC:MARK1:FUNC BPOW")
inst.write(
    "CALC:MARK1:STR 1"
)  # Set marker 1 to track the peak signal (will automatically adjust center frequency to do so)

inst.query("CALC:MARK1:STR?")

# cleanup to close
inst.close()

a = {"ip": ip}
with open("ff_ip.pickle", "wb") as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

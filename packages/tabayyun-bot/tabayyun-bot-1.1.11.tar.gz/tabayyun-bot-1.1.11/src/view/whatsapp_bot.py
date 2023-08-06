import os
from src.lib.whatsapp import WhatsApp
driver_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../lib/bin")

os.environ["PATH"] += os.pathsep + driver_dir

whatsapp = WhatsApp(10)
print(whatsapp.send_message("Salam", ":heart: Good!"))
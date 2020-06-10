# from main import main
# print("Download and install update if available")
# def download_and_install_update_if_available():
#     o = ota_updater.OTAUpdater('https://github.com/DenisCrnic/ota_test/')
#     o.download_and_install_update_if_available('Denis', 'ljubljana')
#     o.check_for_update_to_install_during_next_reboot()


# def start():
#     main.hello()
#     # your custom code goes here. Something like this: ...


# def boot():
#     download_and_install_update_if_available()
#     start()

# boot()


# This is the first code to run on the controller. i:
# - connect to wifi using library in pyboard/main/main/WiFi
# - check for updates on given git repository 
#   - if any new updates are available it will download and install them and reset
# - call start() function in main/main.py


from main import ota_updater
from main import main

# WiFi Credentials
ssid = 'Denis'
password = 'ljubljana'

def download_and_install_update_if_available():
    o = ota_updater.OTAUpdater('https://github.com/DenisCrnic/SECCS_client/')
    o.download_and_install_update_if_available(ssid, password)
    o.check_for_update_to_install_during_next_reboot()

print("Download and install update if available")
download_and_install_update_if_available()
main.start()



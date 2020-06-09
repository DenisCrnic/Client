from main import ota_updater
from main import main

# from main import main

def download_and_install_update_if_available():
    o = ota_updater.OTAUpdater('https://github.com/DenisCrnic/ota_test/')
    o.download_and_install_update_if_available('Denis', 'ljubljana')
    o.check_for_update_to_install_during_next_reboot()


def start():
    main.hello()
    # your custom code goes here. Something like this: ...


def boot():
    download_and_install_update_if_available()
    start()

boot()

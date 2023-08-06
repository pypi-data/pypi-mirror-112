'''IOSXE configure functions for meraki'''

# Python
import re
import logging
import time
import pdb, sys

# Genie
from genie.utils.timeout import Timeout

# Unicon
from unicon import Connection
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import (
    SubCommandFailure,
    TimeoutError,
    ConnectionError,
)
# Logger
log = logging.getLogger(__name__)

def configure_meraki_register(device, token, mac_address):
    """
    This method is used to register the device to meraki dashboard
    It uses token, mac-address
        Args:
            device ("obj"): Device object
            token ("str"): Token used for registration eg: Q2ZZ-2RT8-9D9P
            mac_address: MAC Address of the device eg: 00:18:0a:00:58:ef
        Raises:
            Exception

        Returns:
            True if succeeded else False
    """

    dialog = Dialog([
        Statement(
            pattern=r"Enter token for switch +(\d+):",
            action="sendline({})".format(token),
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=r"Check if token is entered correctly? \[confirm\].*",
            action="sendline()",
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=r"Enter Mac Addr for switch +(\d+) in hh:hh:hh:hh:hh:hh:",
            action="sendline({})".format(mac_address),
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(pattern=r"Check if mac address is entered correctly? \[confirm\].*",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False
        ),
        Statement(pattern=r"Mac address is .*",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False)
    ])

    cmd = 'service meraki register token'
    try:
        device.execute(cmd, reply=dialog)
    except Exception as err:
        log.error("Failed to register the device correctly: {err}".format(err=err))
        raise Exception(err)


def configure_conversion_reversion(device, via_console, mode='conversion', reload_timeout=200,
                                    username=None,
                                    password=None,
                                    reload_creds=None,
                                    reload_hostname='Switch',
                                    retry=30,
                                    interval=10):
    """
    This method verifies if the device is ready for conversion from CAT9K Classic mode
    to Meraki Mode.
    It verifies the device is ready by using 'show meraki' command.
    Once the device is ready, it execute 'service meraki start'
    which will reload the device and come up in Meraki mode.
        Args:
                device ("obj"): Device object
                via_console(`str`): Via to use to reach the device console.
                mode ("str"): Type of mode to be executed : 'conversion' or 'reversion'
                reload_timeout ("int"): How long to wait after the reload starts
                username ("str"): Username after conversion
                password ("str"): Password after conversion
                reload_creds ("str"): reload_creds after conversion
                reload_hostname ("str"): reload_hostname after conversion will be 'Switch'

        Raises:
            Exception

        Returns:
            True if succeeded else False
    """

    if mode == 'conversion':
        mode_check = 'C9K-C'
        dialog = Dialog([
            Statement(
                pattern=r"proceeding with conversion is destructive to the IOS configuration "
                        r"and will render the device as only manageable as via Meraki .* "
                        r"Continue? \[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(pattern=r"^.*RETURN to get started",
                      action='sendline()',
                      loop_continue=False,
                      continue_timer=False)
        ])
        log.info('Verify if the device is ready for conversion')
    else:
        mode_check = 'C9K-M'
        dialog = Dialog([
            Statement(
                pattern=r"proceeding with conversion is destructive to the IOS configuration "
                        r"and will render the device to regular Cat9K "
                        r"Continue? \[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(pattern=r"^.*RETURN to get started",
                      action='sendline()',
                      loop_continue=False,
                      continue_timer=False)
        ])
        log.info('Verify if the device is ready for reversion')

    # Collect device base information since in Meraki Mode there wont
    # be any configs on the device.
    os = device.os
    hostname = device.name

    username, password = device.api.get_username_password(
        device=device,
        username=username,
        password=password,
        creds=reload_creds)

    ip = str(device.connections[via_console]["ip"])
    port = str(device.connections[via_console]["port"])

    #Execute 'show meraki' and check the status of registration and the mode.
    #Switch#show meraki
    #Switch              Serial                                   Conversion
    #Num PID             Number      Meraki SN     Mac Address    Status          Mode
    #5  C9300-24T       FJC2328U02M Q2ZZ-8FAF-954B 0018.0a00.50b7 Registered      C9K-C
    cmd = 'show meraki'
    output = device.parse(cmd)
    if output is not None:
        for sw in output['meraki']['switch']:
            current_mode = output['meraki']['switch'][sw]['current_mode']
            if current_mode != mode_check:
                log.error("Device is not ready, device is NOT in '{}' "
                          "mode".format(mode_check))
                return(False)

    log.info('Device is ready for Conversion from C9K - '
             'Classic Mode to C9K - Meraki Mode')

    # Start the Conversion or Reversion according to the
    # mode specified by the user.
    if mode == 'conversion':
        log.info('Execute service meraki start command')
        cmd = 'service meraki start'
    else:
        log.info('Execute service meraki stop command')
        cmd = 'service meraki stop'

    try:
        device.execute(cmd, reply=dialog, timeout=reload_timeout)
        device.disconnect()
    except SubCommandFailure:
        # Disconnect and destroy the connection
        log.info(
            "Successfully executed {} command on device {}".format(
                device.name, cmd
            )
        )
        log.info(
            "Disconnecting and destroying handle to device {}".format(
                device.name
            )
        )
        device.disconnect()
        device.destroy()
    except Exception as e:
        raise Exception(
            "Error while reloading device '{}'".format(device.name)
        ) from e

    # Reconnect to device which will be in Meraki Mode after
    # conversion or in Classic mode after reversion
    log.info(
        "\n\nReconnecting to device '{}' after conversion/reversion "
        "and reload...".format(hostname)
    )
    new_device = Connection(
        credentials=dict(default=dict(username=username, password=password)),
        os=os,
        hostname=reload_hostname,
        start=["telnet {ip} {port}".format(ip=ip, port=port)],
        prompt_recovery=True,
    )

    #Try to reconnect with iteration
    for i in range(int(retry)):
        try:
            new_device.connect()
        except:
            time.sleep(interval)
            if i == int(retry-1):
                log.error('Retry connection failed')
                return(False)

    log.info(
        "Successully reconnected to device '{}' after 'Conversion/Reversion' "
        "and reload'".format(hostname)
    )

    new_device.disconnect() # Disconnect the device

    if mode == 'conversion':
        log.info('Device from C9K-C to C9K-M Conversion happened Successfully')
    else:
        log.info('Device from C9K-M to C9K-C Reversion happened Successfully')

    return(True)



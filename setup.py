# -*- coding: utf-8 -*-
"""
XKCD Url Handler - Installation utility
@author: Rémi Oudin
@date: 15/04/2017
@license: GPLv3

Utility to install XKCD Url Handler.
"""


from os.path import dirname, abspath, isdir, isfile
from os import makedirs, remove
from sys import stdout
import shutil
from subprocess import call
import argparse
from xdg import BaseDirectory

FILE = "xkcd_handler.py"
TERMINATOR_CONFIG = BaseDirectory.xdg_config_home + "/" + "terminator/config"
INSTALL_PATH = BaseDirectory.xdg_config_home + "/" + "terminator/plugins/"
SCRIPT_PATH = dirname(abspath(__file__)) + "/" +  FILE

def check_path(create=False):
    """ Check if the installation path exist,
    and creates it if not when create=True.
    """
    check_str = "Checking the destination path: %s ..." % INSTALL_PATH
    stdout.write(check_str)
    stdout.flush()
    if isdir(INSTALL_PATH) and isfile(INSTALL_PATH + FILE):
        stdout.write("\r" + check_str + "File Already exists!\n")
        stdout.flush()
        stdout.write("Exiting...\n")
        return False
    elif isdir(INSTALL_PATH):
        stdout.write("\r" + check_str + " Ok!\n")
        stdout.flush()
        return True
    else:
        stdout.write("\r" + check_str + "Absent!\n")
        stdout.flush()
        if create:
            stdout.write("Creating the directory...")
            stdout.flush()
            try:
                makedirs(INSTALL_PATH)
                stdout.write("\rCreating the directory...... Ok!\n")
                stdout.flush()
                return True
            except OSError:
                stdout.write("\rCreating the directory...... Failed!\n")
                stdout.flush()
                stdout.write("Exiting...\n")
                return False
        else:
            return False

def modify_conf_file(remove_line=False):
    """ Modifies the configuration file of Terminator."""
    if not remove_line:
        command = ["sed " + "'s/\\( *enabled_plugins.*\\)/\\1, XKCDUrlHandler/' "\
            + "-i " + TERMINATOR_CONFIG]
        if (call(["grep XKCDUrlHandler %s > /dev/null" % TERMINATOR_CONFIG],
            shell=True)) == 0:
            return True
    else:
        command = ["sed " + "'s/, XKCDUrlHandler//' " + "-i " + TERMINATOR_CONFIG]
    stdout.write("Modifying configuration file...")
    stdout.flush()
    if call(command, shell=True) == 0:
        stdout.write("\rModifying configuration file... Succeded\n")
        stdout.flush()
        return True
    else:
        stdout.write("\rModifying configuration file... Failed\n")
        stdout.flush()
        return False


def install():
    """ Install the files in the good directory."""
    if check_path(create=True):
        stdout.write("Copying file to %s..." % INSTALL_PATH)
        stdout.flush()
        try:
            shutil.copy2(SCRIPT_PATH, INSTALL_PATH)
            stdout.write("\rCopying file to %s... Ok!\n" % INSTALL_PATH)
        except IOError:
            stdout.write("\rCopying file to %s... Failed!\n" % INSTALL_PATH)
            stdout.flush()
            stdout.write("Couldn't copy file...\n")

def uninstall():
    """ Uninstall the files """
    uninstall_str = "Removing script from %s..." % INSTALL_PATH
    stdout.write(uninstall_str)
    if isfile(INSTALL_PATH + FILE):
        try:
            remove(INSTALL_PATH + FILE)
            stdout.write("\r" + uninstall_str + " Ok!\n")
            stdout.flush()
        except OSError:
            stdout.write("\r" + uninstall_str + "Failed!\n")
            stdout.flush()
    else:
        stdout.write("\r" + uninstall_str + "File unexistant!\n")
        stdout.flush()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser("Installation utility for XKCD "
                                     "Url Handler")
    GROUP = PARSER.add_mutually_exclusive_group()
    GROUP.add_argument(
        "--check", "-c",
        help="Checks if the path exists",
        action="store_true"
    )
    GROUP.add_argument(
        "--install", "-i",
        help="Install the script, and modifies the configuration file.",
        action="store_true"
    )
    GROUP.add_argument(
        "--uninstall", "-u",
        help="Uninstall the script",
        action="store_true"
    )
    PARSER.add_argument(
        "--modify-conf", "-m", choices=["remove", "add"],
        help="Modifiy the configuration file",
        action="store",
    )

    ARGS = PARSER.parse_args()
    if  ARGS.check:
        check_path()
    elif ARGS.install:
        install()
        modify_conf_file()
    elif ARGS.modify_conf:
        modify_conf_file(remove_line=("remove"== ARGS.modify_conf))
    elif ARGS.uninstall:
        modify_conf_file(remove_line=True)
        uninstall()
    else:
        install()

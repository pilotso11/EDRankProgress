"""
EDMC Rank Progress Plugin
Copyright (c) 2021 Seth Osher, ALl Rights Reserved
Licensed under AGPLv3
"""

import tkinter as tk
from typing import Optional

import myNotebook as nb
from ranklogger import RankLogger

from config import appname, config

PLUGIN_NAME = "EDRankProgress"

LOG = RankLogger()


class RankProgress:
    """
    RankProgress implements the EDMC plugin interface.
    It adds 3 lines to the EDMC UI showing the progress toward ranks
    """

    def __init__(self) -> None:
        # Be sure to use names that wont collide in our config variables
        self.combat = 0
        self.trade = 0
        self.explore = 0
        self.soldier = 0
        self.exobiologist = 0
        self.empire = 0
        self.federation = 0
        self.combat = config.get_int('last_combat')
        self.trade = config.get_int('last_trade')
        self.explore = config.get_int('last_explore')
        self.soldier = config.get_int('last_soldier')
        self.exobiologist = config.get_int('last_exobiologist')
        self.empire = config.get_int('last_empire')
        self.federation = config.get_int('last_federation')

        self.frame = None
        self.labels = []

        LOG.log("RankProgress instantiated", "INFO")
        LOG.log(f"Progress Com={self.combat} Tt={self.trade} Exp={self.explore}", "INFO")
        LOG.log(f"Progress Merc={self.soldier} Exo={self.exobiologist} Fed={self.federation} Emp={self.empire}", "INFO")

    def on_load(self) -> str:
        """
        on_load is called by plugin_start3 below.

        It is the first point EDMC interacts with our code after loading our module.

        :return: The name of the plugin, which will be used by EDMC for logging and for the settings window
        """
        return PLUGIN_NAME

    def on_unload(self) -> None:
        """
        on_unload is called by plugin_stop below.

        It is the last thing called before EDMC shuts down. Note that blocking code here will hold the shutdown process.
        """
        self.on_preferences_closed("", False)  # Save our prefs

    def setup_preferences(self, parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
        """
        setup_preferences is called by plugin_prefs below.

        It is where we can setup our own settings page in EDMC's settings window. Our tab is defined for us.

        :param parent: the tkinter parent that our returned Frame will want to inherit from
        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        :return: The frame to add to the settings window
        """

        return

    def on_preferences_closed(self, cmdr: str, is_beta: bool) -> None:
        """
        on_preferences_closed is called by prefs_changed below.

        It is called when the preferences dialog is dismissed by the user.

        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        """
        pass

    def setup_main_ui(self, parent: tk.Frame) -> tk.Frame:
        """
        Create our entry on the main EDMC UI.

        This is called by plugin_app below.

        :param parent: EDMC main window Tk
        :return: Our frame
        """

        current_row = 0
        if len(self.labels) == 0:  # Initialize the UI
            frame = tk.Frame(parent)
            frame.columnconfigure(1, weight=1)
            for i in range(3):
                self.labels.append((tk.Label(frame), tk.Label(frame)))
                self.labels[i][0].grid(row=current_row, column=0, sticky=tk.W)
                self.labels[i][1].grid(row=current_row, column=1, sticky=tk.W)
                current_row += 1

            self.labels[0][0]["text"] = "Horizons:"
            self.labels[1][0]["text"] = "Odyssey:"
            self.labels[2][0]["text"] = "Powers:"

            self.frame = frame

        self.update_stats()

        return self.frame

    def update_stats(self):
        """
        Update our data on the UI
        :return: Nothing
        """

        LOG.log("Update UI", "INFO")
        self.labels[0][1]["text"] = f"Combat: {self.combat}%\tTrade: {self.trade}%\tExploration: {self.explore}%"
        self.labels[1][1]["text"] = f"Mercenary: {self.soldier}%\tExobiology: {self.exobiologist}%"
        self.labels[2][1]["text"] = f"Empire: {self.empire}%\tFederation: {self.federation}%"

    def update_ranks(self, entry):
        """
        Update our stats from the log entry
        :param entry: the log entry as a dictionary
        :return: nothing
        """
        if "Combat" in entry:
            self.combat = entry["Combat"]
            self.trade = entry["Trade"]
            self.explore = entry["Explore"]
            self.empire = entry["Empire"]
            self.federation = entry["Federation"]
        if "Soldier" in entry:
            self.soldier = entry["Soldier"]
            self.exobiologist = entry["Exobiologist"]

        LOG.log(f"Progress Com={self.combat} Tt={self.trade} Exp={self.explore}", "INFO")
        LOG.log(f"Progress Merc={self.soldier} Exo={self.exobiologist} Fed={self.federation} Emp={self.empire}", "INFO")
        config.set("last_combat", self.combat)
        config.set("last_trade", self.trade)
        config.set("last_explore", self.explore)
        config.set("last_soldier", self.soldier)
        config.set("last_exobiologist", self.exobiologist)
        config.set("last_empire", self.empire)
        config.set("last_federation", self.federation)

        self.update_stats()

plug = RankProgress()


# Note that all of these could be simply replaced with something like:
# plugin_start3 = cc.on_load
def plugin_start3(plugin_dir: str) -> str:
    return plug.on_load()


def plugin_stop() -> None:
    return plug.on_unload()


def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    return plug.setup_preferences(parent, cmdr, is_beta)


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    return plug.on_preferences_closed(cmdr, is_beta)


def plugin_app(parent: tk.Frame) -> Optional[tk.Frame]:
    return plug.setup_main_ui(parent)


def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry["event"] == "Progress":
        LOG.log(f"Progress Event {entry}", "INFO")
        plug.update_ranks(entry)


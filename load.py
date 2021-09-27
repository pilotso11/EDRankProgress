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

combat_ranks = {0: "Harmless", 1: "Mostly Harmless", 2: "Novice", 3: "Competent", 4: "Expert",
                5: "Master", 6: "Dangerous", 7: "Deadly", 8: "Elite", 9: "Elite I", 10: "Elite II", 11: "Elite III",
                12: "Elite IV", 13: "Elite V"}
trade_ranks = {0: "Penniless", 1: "Mostly Penniless", 2: "Peddler", 3: "Dealer", 4: "Merchant",
               5: "Broker", 6: "Entrepreneur", 7: "Tycoon", 8: "Elite", 9: "Elite I", 10: "Elite II", 11: "Elite III",
               12: "Elite IV", 13: "Elite V"}
explore_ranks = {0: "Aimless", 1: "Mostly Aimless", 2: "Scout", 3: "Surveyor", 4: "Trailblazer",
                 5: "Pathfinder", 6: "Ranger", 7: "Pioneer", 8: "Elite", 9: "Elite I", 10: "Elite II",
                 11: "Elite III", 12: "Elite IV", 13: "Elite V"}
soldier_ranks = {0: "Defenceless", 1: "Mostly Defenceless", 2: "Rookie", 3: "Soldier", 4: "Gunslinger",
                 5: "Warrior", 6: "Gladiator", 7: "Deadeye", 8: "Elite", 9: "Elite I", 10: "Elite II",
                 11: "Elite III", 12: "Elite IV", 13: "Elite V"}
exobiologist_ranks = {0: "Directionless", 1: "Mostly Directionless", 2: "Compiler", 3: "Collector", 4: "Cataloguer",
                      5: "Taxonomist", 6: "Ecologist", 7: "Geneticist", 8: "Elite", 9: "Elite I", 10: "Elite II",
                      11: "Elite III", 12: "Elite IV", 13: "Elite V"}
federation_ranks = {0: "None", 1: "Recruit", 2: "Cadet", 3: "Midshipman", 4: "Petty Officer",
                    5: "Chief Petty Officer", 6: "Warrant Officer", 7: "Ensign", "8": "Lieutenant",
                    9: "Lieutenant Commander", 10: "Post Commander",
                    11: "Post Captain", 12: "Rear Admiral", 13: "Vice Admiral", 14: "Admiral"}
empire_ranks = {0: "None", 1: "Outsider", 2: "Serf", 3: "Master", 4: "Squire",
                5: "Knight", 6: "Lord", 7: "Baron", 8: "Viscount", 9: "Count", 10: "Earl",
                11: "Marquis", 12: "Duke", 13: "Prince", 14: "King"}


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

        self.combat_rank = 0
        self.trade_rank = 0
        self.explore_rank = 0
        self.soldier_rank = 0
        self.exobiologist_rank = 0
        self.empire_rank = 0
        self.federation_rank = 0

        self.combat = config.get_int('last_combat')
        self.trade = config.get_int('last_trade')
        self.explore = config.get_int('last_explore')
        self.soldier = config.get_int('last_soldier')
        self.exobiologist = config.get_int('last_exobiologist')
        self.empire = config.get_int('last_empire')
        self.federation = config.get_int('last_federation')

        self.combat_rank = config.get_int('last_combat_rank')
        self.trade_rank = config.get_int('last_trade_rank')
        self.explore_rank = config.get_int('last_explore_rank')
        self.soldier_rank = config.get_int('last_soldier_rank')
        self.exobiologist_rank = config.get_int('last_exobiologist_rank')
        self.empire_rank = config.get_int('last_empire_rank')
        self.federation_rank = config.get_int('last_federation_rank')

        self.show_ranks = config.get("show_ranks") == "true"
        self.show_progress = config.get("show_ranks") == "true"

        self.frame = None
        self.labels = []

        self.log_data()

    def log_data(self):
        LOG.log("RankProgress instantiated", "INFO")
        LOG.log(f"Progress Com={self.combat} Tt={self.trade} Exp={self.explore}", "INFO")
        LOG.log(f"Progress Merc={self.soldier} Exo={self.exobiologist} Fed={self.federation} Emp={self.empire}", "INFO")
        LOG.log(f"Rank Com={self.combat_rank} Tt={self.trade_rank} Exp={self.explore_rank}", "INFO")
        LOG.log(
            f"Rank Merc={self.soldier_rank} Exo={self.exobiologist_rank} Fed={self.federation_rank} Emp={self.empire_rank}",
            "INFO")

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
        if len(self.labels) == 0:  # Initialize the UI
            frame = tk.Frame(parent)
            frame.columnconfigure(5, weight=1)
            self.labels.append((tk.Label(frame, text="Horizons",
                                         borderwidth=2, relief="ridge", width="25", justify="center"),
                                tk.Label(frame, text="", justify="center"),
                                tk.Label(frame, text="Odyssey",
                                         borderwidth=2, relief="ridge", width="25", justify="center"),
                                tk.Label(frame) ))
            self.labels[0][0].grid(row=0, column=0, columnspan=2)
            self.labels[0][1].grid(row=0, column=2, columnspan=1)
            self.labels[0][2].grid(row=0, column=3, columnspan=2)

            self.labels.append((tk.Label(frame, text="Combat:"), tk.Label(frame),
                                tk.Label(frame, text="", justify="center"),
                                tk.Label(frame, text="Mercenary:"), tk.Label(frame),
                                tk.Label(frame)))
            self.labels[1][0].grid(row=1, column=0, sticky=tk.W)
            self.labels[1][1].grid(row=1, column=1, sticky=tk.W)
            self.labels[1][2].grid(row=1, column=2, sticky=tk.W)
            self.labels[1][3].grid(row=1, column=3, sticky=tk.W)
            self.labels[1][4].grid(row=1, column=4, sticky=tk.W)

            self.labels.append((tk.Label(frame, text="Trade:"), tk.Label(frame),
                                tk.Label(frame, text="", justify="center"),
                                tk.Label(frame, text="Exobiology:"), tk.Label(frame),
                                tk.Label(frame)))
            self.labels[2][0].grid(row=2, column=0, sticky=tk.W)
            self.labels[2][1].grid(row=2, column=1, sticky=tk.W)
            self.labels[2][2].grid(row=2, column=2, sticky=tk.W)
            self.labels[2][3].grid(row=2, column=3, sticky=tk.W)
            self.labels[2][4].grid(row=2, column=4, sticky=tk.W)

            self.labels.append((tk.Label(frame, text="Exploration:"), tk.Label(frame),
                                tk.Label(frame, text="", justify="center"),
                                tk.Label(frame, text=""), tk.Label(frame),
                                tk.Label(frame)))
            self.labels[3][0].grid(row=3, column=0, sticky=tk.W)
            self.labels[3][1].grid(row=3, column=1, sticky=tk.W)
            self.labels[3][2].grid(row=3, column=2, sticky=tk.W)
            self.labels[3][3].grid(row=3, column=3, sticky=tk.W)
            self.labels[3][4].grid(row=3, column=4, sticky=tk.W)

            self.labels.append((tk.Label(frame, text="Powers",
                                         borderwidth=2, width=55, relief="ridge", justify="center"),
                                tk.Label(frame)))
            self.labels[4][0].grid(row=5, column=0, columnspan=5)

            self.labels.append((tk.Label(frame, text="Empire:", justify="center"), tk.Label(frame),
                                tk.Label(frame, text="", justify="center"),
                                tk.Label(frame, text="Federation:"), tk.Label(frame),
                                tk.Label(frame)))
            self.labels[5][0].grid(row=6, column=0, sticky=tk.W)
            self.labels[5][1].grid(row=6, column=1, sticky=tk.W)
            self.labels[5][2].grid(row=6, column=2, sticky=tk.W)
            self.labels[5][3].grid(row=6, column=3, sticky=tk.W)
            self.labels[5][4].grid(row=6, column=4, sticky=tk.W)

            self.frame = frame

        self.update_stats()

        return self.frame

    def update_stats(self):
        """
        Update our data on the UI
        :return: Nothing
        """

        LOG.log("Update UI", "INFO")

        self.labels[1][1]["text"] = f"{combat_ranks[self.combat_rank]}  {self.combat}%"
        self.labels[2][1]["text"] = f"{trade_ranks[self.trade_rank]}  {self.trade}%"
        self.labels[3][1]["text"] = f"{explore_ranks[self.explore_rank]}  {self.explore}%"

        self.labels[1][4]["text"] = f"{soldier_ranks[self.soldier_rank]}  {self.soldier}%"
        self.labels[2][4]["text"] = f"{exobiologist_ranks[self.exobiologist_rank]}  {self.exobiologist}%"

        self.labels[5][1]["text"] = f"{empire_ranks[self.empire_rank]}  {self.empire}%"
        self.labels[5][4]["text"] = f"{federation_ranks[self.federation_rank]}  {self.federation}%"

    def update_progress(self, entry):
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

        self.log_data()

        config.set("last_combat", self.combat)
        config.set("last_trade", self.trade)
        config.set("last_explore", self.explore)
        config.set("last_soldier", self.soldier)
        config.set("last_exobiologist", self.exobiologist)
        config.set("last_empire", self.empire)
        config.set("last_federation", self.federation)

        self.update_stats()

    def update_ranks(self, entry):
        """
        Update our stats from the log entry
        :param entry: the log entry as a dictionary
        :return: nothing
        """
        if "Combat" in entry:
            self.combat_rank = entry["Combat"]
            self.trade_rank = entry["Trade"]
            self.explore_rank = entry["Explore"]
            self.empire_rank = entry["Empire"]
            self.federation_rank = entry["Federation"]
        if "Soldier" in entry:
            self.soldier_rank = entry["Soldier"]
            self.exobiologist_rank = entry["Exobiologist"]

        self.log_data()

        config.set("last_combat_rank", self.combat_rank)
        config.set("last_trade_rank", self.trade_rank)
        config.set("last_explore_rank", self.explore_rank)
        config.set("last_soldier_rank", self.soldier_rank)
        config.set("last_exobiologist_rank", self.exobiologist_rank)
        config.set("last_empire_rank", self.empire_rank)
        config.set("last_federation_rank", self.federation_rank)

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
        plug.update_progress(entry)
    elif entry["event"] == "Rank":
        LOG.log(f"Rank event {entry}", "INFO")
        plug.update_ranks(entry)

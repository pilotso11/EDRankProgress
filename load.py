"""
EDMC Rank Progress Plugin
Copyright (c) 2021 Seth Osher, ALl Rights Reserved
Licensed under AGPLv3
Version 1.0 - initial release
Version 1.1 - changed layout and made layout configurable
Version 1.2 - Removed borders, tweaked settings ui
"""

import tkinter as tk
from typing import Optional

import myNotebook as nb
from ranklogger import RankLogger

from config import appname, config
from theme import theme

PLUGIN_NAME = "EDRankProgress"
VERSION = "1.2"

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
        self.show_rank = tk.IntVar(value=config.get_int('edrp_show_rank') and 1)
        self.show_rank_row = tk.IntVar(value=config.get_int('edrp_show_rank_row') and 1)
        self.show_rank_button = None
        self.show_rank_row_button = None

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

        self.combat = config.get_int('edrp_last_combat')
        self.trade = config.get_int('edrp_last_trade')
        self.explore = config.get_int('edrp_last_explore')
        self.soldier = config.get_int('edrp_last_soldier')
        self.exobiologist = config.get_int('edrp_last_exobiologist')
        self.empire = config.get_int('edrp_last_empire')
        self.federation = config.get_int('edrp_last_federation')

        self.combat_rank = config.get_int('edrp_last_combat_rank')
        self.trade_rank = config.get_int('edrp_last_trade_rank')
        self.explore_rank = config.get_int('edrp_last_explore_rank')
        self.soldier_rank = config.get_int('edrp_last_soldier_rank')
        self.exobiologist_rank = config.get_int('edrp_last_exobiologist_rank')
        self.empire_rank = config.get_int('edrp_last_empire_rank')
        self.federation_rank = config.get_int('edrp_last_federation_rank')

        self.show_rank_val = config.get_int('edrp_show_rank')
        self.show_rank_row_val = config.get_int('edrp_show_rank_row')

        self.frame = None
        self.labels = dict()

        self.log_data()

    def log_data(self):
        LOG.log("RankProgress instantiated", "INFO")
        LOG.log(f"Progress Com={self.combat} Trd={self.trade} Exp={self.explore}", "INFO")
        LOG.log(f"Progress Merc={self.soldier} Exo={self.exobiologist} Fed={self.federation} Emp={self.empire}", "INFO")
        LOG.log(f"Rank Com={self.combat_rank} Trd={self.trade_rank} Exp={self.explore_rank}", "INFO")
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
        """Plugin preferences setup hook."""
        frame = nb.Frame(parent)
        frame.columnconfigure(1, weight=1)

        self.show_rank_button = nb.Checkbutton(
            # LANG: Settings>EDSM - Label on checkbox for 'send data'
            frame, text='Show Ranks', variable=self.show_rank,
            command=self.on_check
        )
        self.show_rank_button.grid(columnspan=2, padx=12, pady=(5, 0), sticky=tk.W)

        self.show_rank_row_button = nb.Checkbutton(
            # LANG: Settings>EDSM - Label on checkbox for 'send data'
            frame, text='Use separate row for rank', variable=self.show_rank_row
        )
        self.show_rank_row_button.grid(columnspan=2, padx=24, pady=(5, 0), sticky=tk.W)

        label = nb.Label(frame, text=f"{PLUGIN_NAME} {VERSION}")
        label.grid(columnspan=2, padx=12, pady=(10, 0), sticky=tk.W)

        self.on_check() # Set enabled state of second button

        return frame

    def on_check(self):
        # Toggle state of separate row checkbox
        if self.show_rank.get() == 1:
            self.show_rank_row_button["state"] = tk.NORMAL
        else:
            self.show_rank_row_button["state"] = tk.DISABLED

    def on_preferences_closed(self, cmdr: str, is_beta: bool) -> None:
        """
        on_preferences_closed is called by prefs_changed below.

        It is called when the preferences dialog is dismissed by the user.

        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        """
        config.set('edrp_show_rank', self.show_rank.get())
        self.show_rank_val = self.show_rank.get()
        config.set('edrp_show_rank_row', self.show_rank_row.get())
        self.show_rank_row_val = self.show_rank_row.get()
        self.setup_frame()
        self.update_stats()

    def setup_main_ui(self, parent: tk.Frame) -> tk.Frame:
        """
        Create our entry on the main EDMC UI.

        This is called by plugin_app below.

        :param parent: EDMC main window Tk
        :return: Our frame
        """
        if len(self.labels) == 0:  # Initialize the UI
            frame = tk.Frame(parent)
            self.frame = frame
            self.setup_frame()

        self.update_stats()

        return self.frame

    def setup_frame(self):
        frame = self.frame
        for widget in frame.winfo_children():
            widget.destroy()

        border = 0

        frame_h = tk.Frame(frame, borderwidth=border, relief="groove")
        frame_h.columnconfigure(1, weight=1)  # Pad the last column
        frame_o = tk.Frame(frame, borderwidth=border, relief="groove")
        frame_o.columnconfigure(1, weight=1)  # Pad the last column
        frame_p = tk.Frame(frame, borderwidth=border, relief="groove")
        # Pad the center column and force the labels and values to be the same width
        frame_p.columnconfigure(0, weight=1, uniform="l")
        frame_p.columnconfigure(1, weight=1, uniform="v")
        frame_p.columnconfigure(2, weight=2)
        frame_p.columnconfigure(3, weight=1, uniform="l")
        frame_p.columnconfigure(4, weight=1, uniform="v")

        # Layout the 3 frames - ensure the 2 columns are the same width and we fill the full width
        #  Horz   Odys
        #    Powers
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.columnconfigure(1, weight=1, uniform="a")
        frame.columnconfigure(2, weight=5)
        frame_h.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        frame_o.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        frame_p.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Two labels for each
        self.labels = dict()
        self.labels["com"] = (tk.Label(frame_h), tk.Label(frame_h))  # combat
        self.labels["trd"] = (tk.Label(frame_h), tk.Label(frame_h))  # trade
        self.labels["exp"] = (tk.Label(frame_h), tk.Label(frame_h))  # exploration
        self.labels["merc"] = (tk.Label(frame_o), tk.Label(frame_o))  # mercenary
        self.labels["exo"] = (tk.Label(frame_o), tk.Label(frame_o))  # exobiology
        self.labels["emp"] = (tk.Label(frame_p), tk.Label(frame_p))  # empire
        self.labels["fed"] = (tk.Label(frame_p), tk.Label(frame_p))  # Federation

        if self.show_rank_row_val == 1 and self.show_rank_val == 1:

            # Layout with 2 rows, one for Progress and one for Rank

            tk.Label(frame_h, text="Horizons", justify="center").grid(row=0, column=0, columnspan=2)  # Horizons Label
            tk.Label(frame_h, text="Combat:").grid(row=1, column=0, sticky=tk.W)  # Combat Label
            self.labels["com"][0].grid(row=1, column=1, sticky=tk.W)  # combat pct
            self.labels["com"][1].grid(row=2, column=0, columnspan=2)  # combat rank
            tk.Label(frame_h, text="Trade:").grid(row=3, column=0, sticky=tk.W)  # trade label
            self.labels["trd"][0].grid(row=3, column=1, sticky=tk.W)
            self.labels["trd"][1].grid(row=4, column=0, columnspan=2)
            tk.Label(frame_h, text="Exploration:").grid(row=5, column=0, sticky=tk.W)  # Exploration
            self.labels["exp"][0].grid(row=5, column=1, sticky=tk.W)
            self.labels["exp"][1].grid(row=6, column=0, columnspan=2)

            tk.Label(frame_o, text="Odyssey", justify="center").grid(row=0, column=0, columnspan=2)  # Odyssey Label
            tk.Label(frame_o, text="Mercenary:").grid(row=1, column=0, sticky=tk.W)  # Mercenary label
            self.labels["merc"][0].grid(row=1, column=1, sticky=tk.W)  # merc pct
            self.labels["merc"][1].grid(row=2, column=0, columnspan=2)  # merc rank
            tk.Label(frame_o, text="Exobiology:").grid(row=3, column=0, sticky=tk.W)  # Exobiology
            self.labels["exo"][0].grid(row=3, column=1, sticky=tk.W)
            self.labels["exo"][1].grid(row=4, column=0, columnspan=2)

            tk.Label(frame_p, text="Powers", justify="center").grid(row=0, column=0, columnspan=5, sticky=tk.W + tk.E)
            tk.Label(frame_p, text="Empire:").grid(row=1, column=0, sticky=tk.W)  # Empire
            self.labels["emp"][0].grid(row=1, column=1, sticky=tk.W)
            self.labels["emp"][1].grid(row=2, column=0, columnspan=2)
            tk.Label(frame_p, text="Federation:").grid(row=1, column=3, sticky=tk.W)  # Federation
            self.labels["fed"][0].grid(row=1, column=4, sticky=tk.W)
            self.labels["fed"][1].grid(row=2, column=3, columnspan=2)

        else:
            # Layout with 1 rows, one for Progress and Rank if enabled
            tk.Label(frame_h, text="Horizons", justify="center").grid(row=0, column=0, columnspan=2)  # Horizons Label
            tk.Label(frame_h, text="Combat:").grid(row=1, column=0, sticky=tk.W)  # Combat Label
            self.labels["com"][0].grid(row=1, column=1, sticky=tk.W)
            tk.Label(frame_h, text="Trade:").grid(row=2, column=0, sticky=tk.W)  # Trade
            self.labels["trd"][0].grid(row=2, column=1, sticky=tk.W)
            tk.Label(frame_h, text="Exploration:").grid(row=3, column=0, sticky=tk.W)  # Exploration
            self.labels["exp"][0].grid(row=3, column=1, sticky=tk.W)

            tk.Label(frame_o, text="Odyssey", justify="center").grid(row=0, column=0, columnspan=2)  # Odyssey Label
            tk.Label(frame_o, text="Mercenary:").grid(row=1, column=0, sticky=tk.W)  # Mercenary label
            self.labels["merc"][0].grid(row=1, column=1, sticky=tk.W)
            tk.Label(frame_o, text="Exobiology:").grid(row=2, column=0, sticky=tk.W)  # Exobiology
            self.labels["exo"][0].grid(row=2, column=1, sticky=tk.W)

            tk.Label(frame_p, text="Powers", justify="center").grid(row=0, column=0, columnspan=5, sticky=tk.W + tk.E)
            tk.Label(frame_p, text="Empire:").grid(row=1, column=0, sticky=tk.W)  # Empire
            self.labels["emp"][0].grid(row=1, column=1, sticky=tk.W)
            tk.Label(frame_p, text="Federation:").grid(row=1, column=3, sticky=tk.W)  # Federation
            self.labels["fed"][0].grid(row=1, column=4, sticky=tk.W)

        for widget in frame.winfo_children():
            theme.update(widget)

    def update_stats(self):
        """
        Update our data on the UI
        :return: Nothing
        """

        LOG.log("Update UI", "DEBUG")

        if self.show_rank_row_val == 0 and self.show_rank_val == 1:
            self.labels["com"][0]["text"] = f"{combat_ranks[self.combat_rank]}  {self.combat}%"
            self.labels["trd"][0]["text"] = f"{trade_ranks[self.trade_rank]}  {self.trade}%"
            self.labels["exp"][0]["text"] = f"{explore_ranks[self.explore_rank]}  {self.explore}%"

            self.labels["merc"][0]["text"] = f"{soldier_ranks[self.soldier_rank]}  {self.soldier}%"
            self.labels["exo"][0]["text"] = f"{exobiologist_ranks[self.exobiologist_rank]}  {self.exobiologist}%"

            self.labels["emp"][0]["text"] = f"{empire_ranks[self.empire_rank]}  {self.empire}%"
            self.labels["fed"][0]["text"] = f"{federation_ranks[self.federation_rank]}  {self.federation}%"

        else:
            self.labels["com"][0]["text"] = f"{self.combat}%"
            self.labels["trd"][0]["text"] = f"{self.trade}%"
            self.labels["exp"][0]["text"] = f"{self.explore}%"
            self.labels["com"][1]["text"] = f"{combat_ranks[self.combat_rank]}"
            self.labels["trd"][1]["text"] = f"{trade_ranks[self.trade_rank]}"
            self.labels["exp"][1]["text"] = f"{explore_ranks[self.explore_rank]}"

            self.labels["merc"][0]["text"] = f"{self.soldier}%"
            self.labels["exo"][0]["text"] = f"{self.exobiologist}%"
            self.labels["merc"][1]["text"] = f"{soldier_ranks[self.soldier_rank]}"
            self.labels["exo"][1]["text"] = f"{exobiologist_ranks[self.exobiologist_rank]}"

            self.labels["emp"][0]["text"] = f"{self.empire}%"
            self.labels["fed"][0]["text"] = f"{self.federation}%"
            self.labels["emp"][1]["text"] = f"{empire_ranks[self.empire_rank]}"
            self.labels["fed"][1]["text"] = f"{federation_ranks[self.federation_rank]}"

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

        config.set("edrp_last_combat", self.combat)
        config.set("edrp_last_trade", self.trade)
        config.set("edrp_last_explore", self.explore)
        config.set("edrp_last_soldier", self.soldier)
        config.set("edrp_last_exobiologist", self.exobiologist)
        config.set("edrp_last_empire", self.empire)
        config.set("edrp_last_federation", self.federation)

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

        config.set("edrp_last_combat_rank", self.combat_rank)
        config.set("edrp_last_trade_rank", self.trade_rank)
        config.set("edrp_last_explore_rank", self.explore_rank)
        config.set("edrp_last_soldier_rank", self.soldier_rank)
        config.set("edrp_last_exobiologist_rank", self.exobiologist_rank)
        config.set("edrp_last_empire_rank", self.empire_rank)
        config.set("edrp_last_federation_rank", self.federation_rank)

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

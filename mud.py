#! /usr/bin/env python3
import mud.game
import mud.server
# mud.game.GAME = mud.game.Game("iut")
# mud.game.GAME = mud.game.Game("greg")
mud.game.GAME = mud.game.Game("final")
mud.game.GAME.load()
mud.game.GAME.start()

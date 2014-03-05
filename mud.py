#! /bin/env python3
import mud.game
mud.game.GAME = mud.game.Game("iut")
mud.game.GAME.load()
import mud.server
mud.server.main()

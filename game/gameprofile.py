import json


class GameProfile:

    def finishGame(self, game):
        print(self.coins)
        print("Game finished")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

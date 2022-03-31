class Wish:
    def __init__(self, name, type, rarity, pity) -> None:
        self.name = name
        self.type = type
        self.rarity = rarity
        self.pity = pity

    def __str__(self):
        if self.rarity == 5:
            return f"`{self.rarity}* ({self.pity} under pity) {self.name} ({self.type})`"
        if self.rarity == 4:
            return f"**{self.rarity}* ({self.pity} under pity) {self.name} ({self.type})**"
        else:
            return f"{self.rarity}* ({self.pity} under pity) {self.name} ({self.type})"
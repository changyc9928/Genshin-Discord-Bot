from database.coop import Coop

class SetStatement():
    def __init__(self, stmt, and_stmt):
        super().__init__()
        self.stmt = stmt
        self.and_stmt = and_stmt

    def accept(self, visitor):
        return visitor.visit_set_stmt(self)

class TimesStatement():
    def __init__(self, attributes, times):
        self.attributes = attributes
        self.times = times

    def accept(self, visitor):
        return visitor.visit_times_stmt(self)

class TimeStatement():
    def __init__(self, time):
        self.time = time

    def accept(self, visitor):
        return visitor.visit_time_stmt(self)


class Evaluator():
    def __init__(self, bot, tree):
        self.tree = tree
        self.bot = bot

    def evaluate(self):
        self.tree.accept(self)

    def visit_set_stmt(self, set_stmt):
        set_stmt.stmt.accept(self)
        
        if set_stmt.and_stmt is not None:
            set_stmt.and_stmt.accept(self)

    def visit_times_stmt(self, times_stmt):
        for attribute in times_stmt.attributes:
            # modify farm count here with times_stmt.times
            pass
            
    async def visit_time_stmt(self, time_stmt):
        # modify player time here with time_stmt.time
        Coop.data[self.bot.user.id].change_time(time_stmt.time)
        channel = self.bot.get_channel(self.bot.channel)
        await channel.send(f"@everyone, {self.bot.user.id} has changed his/her online time to {Coop.data[self.bot.user.id].time}.")
        
        

from database.coop import Coop

class SetStatement():
    def __init__(self, stmt, and_stmt):
        self.stmt = stmt
        self.and_stmt = and_stmt

    async def accept(self, visitor):
        return await visitor.visit_set_stmt(self)

class TimesStatement():
    def __init__(self, attributes, times):
        self.attributes = attributes
        self.times = times

    async def accept(self, visitor):
        return await visitor.visit_times_stmt(self)

class TimeStatement():
    def __init__(self, time):
        self.time = time

    async def accept(self, visitor):
        return await visitor.visit_time_stmt(self)


class Evaluator():
    def __init__(self, bot, coop, tree):
        self.tree = tree
        self.bot = bot
        self.coop = coop

    async def evaluate(self):
        return await self.tree.accept(self)

    async def visit_set_stmt(self, set_stmt):
        await set_stmt.stmt.accept(self)
        
        if set_stmt.and_stmt is not None:
            await set_stmt.and_stmt.accept(self)
        return 0

    async def visit_times_stmt(self, times_stmt):
        for attribute in times_stmt.attributes:
            # modify farm count here with times_stmt.times
            pass
        return 0
            
    async def visit_time_stmt(self, time_stmt):
        # modify player time here with time_stmt.time
        channel = self.bot.get_channel(self.bot.channel)
        print("Coop data: ", self.coop.data)
        print("My current user ID is: ", self.bot.user.id)
        self.coop.data[self.bot.user.id].change_time(str(time_stmt.time))
        await channel.send(f"@everyone, {self.bot.user.mention} has changed his/her online time to {self.coop.data[self.bot.user.id].time}.")
        return 0
        
        

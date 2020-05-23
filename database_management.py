import random
import time

import mysql.connector as mariadb
from discord.ext import commands

from launcher import cnx, logger, DB_NAME


def dbcallprocedure(procedure, *, commit: bool = False, returns: bool = False, params: tuple):
    db = cnx.get_connection()
    cursor = db.cursor()
    if returns:
        # we can be certain that the return value is at index [1] from all stored procedures
        # but since we return, we need to ensure the closing of the database connection first, then return
        return_value = cursor.callproc(procedure, params)[1]
        db.close()
        return return_value
    cursor.callproc(procedure, params)
    if commit:
        db.commit()
    db.close()


def checkdbforuser(message):
    result = dbcallprocedure('CheckUserExist', returns=True, params=(message.author.id, '@res'))
    if result:
        # entry for this user ID exists, proceed to check for last XP gain time, possibly awarding some new XP
        last_xp_gain = dbcallprocedure('CheckXPTime', returns=True, params=(message.author.id, '@res'))
        unix_now = int(time.time())
        if unix_now - last_xp_gain > 120:
            # user got XP more than two minutes ago, award between 15 and 25 XP and update last XP gain time
            dbcallprocedure('IncreaseXP', commit=True, params=(message.author.id, random.randint(15, 25), unix_now))
    else:
        # user is unknown to the database, add it with user ID and default in the other fields
        dbcallprocedure('AddNewUser', commit=True, params=(message.author.id,))


class DatabaseManagement(commands.Cog, command_attrs=dict(hidden=True)):
    """Manages the DTbot MariaDB database"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.message.author)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        elif message.author.bot:
            return
        try:
            checkdbforuser(message)
        finally:
            pass
        pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        dbcallprocedure('AddNewServer', commit=True, params=(guild.id, guild.member_count))

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        result = dbcallprocedure('CheckCommandExist', returns=True, params=(ctx.command.qualified_name, '@res'))
        if result:
            dbcallprocedure('IncrementCommandUsage', commit=True, params=(ctx.command.qualified_name,))
        else:
            if ctx.command.cog_name is None:
                cog_name = "main"
            else:
                cog_name = ctx.command.cog_name
            dbcallprocedure('AddNewCommand', commit=True, params=(ctx.command.qualified_name, cog_name))
            # because the command was used this one time, we increment the default value (0) by 1
            dbcallprocedure('IncrementCommandUsage', commit=True, params=(ctx.command.qualified_name,))

    @commands.command(description="Manually adds an entry to the table 'users' of DTbot's database."
                                  "\nGenerally not required. Developers only.")
    async def adduserdata(self, ctx, user_id: int, user_xp: int, user_last_xp_gain: int, user_rep: int,
                          user_last_rep_awarded: int):
        params = (user_id, user_xp, user_last_xp_gain, user_rep, user_last_rep_awarded)
        try:
            dbcallprocedure('ManualNewUser', commit=True, params=params)
            await ctx.send(f"Row added successfully to table `users` in database `{DB_NAME}`.")
        except mariadb.Error as err:
            logger.error(err)
        except Exception as e:
            logger.error(e)

    @commands.command(description="Manually changes the prefix a server wants to use for DTbot."
                                  "\nNeeds to be 1-3 characters in length.\nCurrently not in use. Developers only.",
                      aliases=['csp', 'changeprefix'],
                      rest_is_raw=True)
    async def changeserverprefix(self, ctx, *newprefix: str):
        newprefix = ''.join(newprefix)
        if len(newprefix) <= 3:
            dbcallprocedure('ChangeServerPrefix', commit=True, params=(ctx.message.guild.id, newprefix))
            await ctx.send(f'Prefix for {ctx.guild} changed to `{newprefix}`.')
        else:
            await ctx.send("Invalid prefix length (max. 3 characters)")

    @commands.command(description="Manually cycles through the bot's servers to refresh the table 'servers' of the "
                                  "database.\nGenerally not required. Developers only.")
    async def refreshservers(self, ctx):
        for guild in self.bot.guilds:
            dbcallprocedure('AddNewServer', commit=True, params=(guild.id, guild.member_count))
        await ctx.send('Server list refreshed.', delete_after=5)

    @commands.command(description="Manually resets the prefix a server wants to use for DTbot to the default."
                                  "\nCurrently not in use. Developers only.")
    async def resetserverprefix(self, ctx):
        dbcallprocedure('ChangeServerPrefix', commit=True, params=(ctx.message.guild.id, '+'))
        await ctx.send(f'Prefix for {ctx.guild} reset to `+`.')


def setup(bot):
    bot.add_cog(DatabaseManagement(bot))

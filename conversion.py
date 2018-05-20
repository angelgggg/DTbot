from discord.ext import commands

class Conversions():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True,
                      name='ck',
                      description='Convert temperature from °Celsius to Kelvin',
                      brief='°C > K',
                      aliases=['ctok'])
    async def ______ck(self, number):
        ck_value = round(float(number) + 273.15, 2)
        await self.bot.say(str(ck_value) + '°K')


    @commands.command(hidden=True,
                      name='kc',
                      description='Convert temperature from Kelvin to °Celsius',
                      brief='K > °C',
                      aliases=['ktoc'])
    async def ______kc(self, number):
        ck_value = round(float(number) - 273.15, 2)
        await self.bot.say(str(ck_value) + '°C')


    @commands.command(hidden=True,
                      name='kf',
                      description='Convert temperature from Kelvin to °Fahrenheit',
                      brief='K > °F',
                      aliases=['ktof'])
    async def _____kf(self, number):
        ck_value = round(float(number) * 9/5 - 459.67, 2)
        await self.bot.say(str(ck_value) + '°F')


    @commands.command(hidden=True,
                      name='fk',
                      description='Convert temperature from Kelvin to °Fahrenheit',
                      brief='°F > K',
                      aliases=['ftok'])
    async def _____fk(self, number):
        ck_value = round((float(number) + 459.67) * 5/9, 2)
        await self.bot.say(str(ck_value) + 'K')


    @commands.command(name='cf',
                      description='Convert temperature from °Celsius to °Fahrenheit',
                      brief='°C > °F',
                      aliases=['ctof'])
    async def ____cf(self, number):
        cf_value = round(float(number) * 1.8 + 32, 2)
        await self.bot.say(str(cf_value) + '°F')


    @commands.command(name='fc',
                      description='Convert temperature from °Fahrenheit to °Celsius',
                      brief='°F > °C',
                      aliases=['ftoc'])
    async def ____fc(self, number):
        fc_value = round((float(number) - 32) / 1.8, 2)
        await self.bot.say(str(fc_value) + '°C')


    @commands.command(name='cmin',
                      description='Convert from Centimeters to Inches',
                      brief='cm > in',
                      aliases=['cmtoin'])
    async def ___cmin(self, number):
        cminch_value = round(float(number) * 0.393701, 2)
        await self.bot.say(str(cminch_value) + ' inch')


    @commands.command(name='incm',
                      description='Convert from Inches to Centimeters',
                      brief='in > cm',
                      aliases=['intocm'])
    async def ___incm(self, number):
        inchcm_value = round(float(number) * 2.54, 2)
        await self.bot.say(str(inchcm_value) + ' cm')


    @commands.command(name='ftm',
                      description='Convert from Feet to Meters',
                      brief='ft > m',
                      aliases=['fttom'])
    async def __ftm(self, number):
        ftm_value = round(float(number) * 0.3048, 2)
        await self.bot.say(str(ftm_value) + ' m')


    @commands.command(name='mft',
                      description='Convert from Meters to Feet',
                      brief='m  > ft',
                      aliases=['mtoft'])
    async def __mft(self, number):
        mft_value = round(float(number) / 0.3048, 2)
        await self.bot.say(str(mft_value) + ' ft')


    @commands.command(name='kmmi',
                      description='Convert from Kilometers to Miles',
                      brief='km > mi',
                      aliases=['kitomi'])
    async def _kmmi(self, number):
        kmmi_value = round(float(number) * 0.621371, 2)
        await self.bot.say(str(kmmi_value) + ' mi')


    @commands.command(name='mikm',
                      description='Convert Miles to Kilometers',
                      brief='mi > km',
                      aliases=['mitokm'])
    async def _mikm(self, number):
        mikm_value = round(float(number) / 0.621371, 2)
        await self.bot.say(str(mikm_value) + ' km')


def setup(bot):
    bot.add_cog(Conversions(bot))

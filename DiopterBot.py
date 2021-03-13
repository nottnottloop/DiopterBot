import discord
import logging

logging.basicConfig(level=logging.INFO)

# thar be dragons here
class DiopterBot(discord.Client):
    async def on_ready(self):
        print('Logged in as {0.user}'.format(self))

    async def cm_to_diopters(self, channel, cm_value, differentials=0):
        cm_value = abs(float(cm_value))
        differentials = float(differentials)
        try:
            result = round((100/cm_value), 2)
        except ZeroDivisionError:
            await channel.send("You can't see anything? :grimacing:")
            return
        formatted_cms = format(cm_value, '.2f')
        formatted_raw_result = format(result, '.2f')
        result_with_diffs = result - differentials
        if result_with_diffs % 0.25 >= 0.125:
            formatted_result = format(0.25 * ((result_with_diffs // 0.25) + 1), '.2f')
        else:
            formatted_result = format(0.25 * (result_with_diffs // 0.25), '.2f')
        result = format(result, '.2f')
        differentials_formatted = format(differentials, '.2f')
        result_with_diffs = format(result_with_diffs, '.2f')
        if differentials == 0:
            await channel.send("To calculate diopters, do 100 divided by the cm value, and add on a minus sign:\n`100/{}cm = -{} diopters\nMyopia of eye approximately -{}`\nFor help with DiopterBot, type `diopterbot`".format(formatted_cms, formatted_raw_result, formatted_result))
        elif differentials < 0:
            await channel.send("To calculate diopters, do 100 divided by the cm value, and add on a minus sign.\nBecause you measured with differentials, add the strength of your differentials as well:\n`100/{}cm = -{} diopters\n-{}{} = -{}\nMyopia of eye approximately -{}`\nFor help with DiopterBot, type `diopterbot`".format(formatted_cms, result, result, differentials_formatted, result_with_diffs, formatted_result))
        elif differentials > 0:
            await channel.send("To calculate diopters, do 100 divided by the cm value, and add on a minus sign.\nBecause you measured with plus lens, add the strength of your plus lens as well:\n`100/{}cm = -{} diopters\n-{}+{} = -{}\nMyopia of eye approximately -{}`\nFor help with DiopterBot, type `diopterbot`".format(formatted_cms, result, result, differentials_formatted, result_with_diffs, formatted_result))

    async def diopters_to_cm(self, channel, diopter_value, differentials=0):
        diopter_value = float(diopter_value)
        differentials = float(differentials)
        if diopter_value > differentials and differentials != 0:
            await channel.send(
                "AHHHHHHH MY EYES :sob::sob::sob:")
            return
        diopter_value = abs(float(diopter_value))
        diopters_and_diffs = diopter_value + differentials
        try:
            result = round((100/float(diopter_value + differentials)), 2)
        except ZeroDivisionError:
            await channel.send(":infinity:\nIn theory, these are not your differentials but full strength glasses that correct you to perfect vision.\nYou can see ∞!")
            return
        diopter_value_formatted = format(diopter_value, '.2f')
        # differentials_formatted = format(differentials, '.2f')
        diopters_and_diffs_formatted = format(diopters_and_diffs, '.2f')
        if differentials == 0:
            await channel.send("To calculate diopters to cm, do 100 divided by the diopter value, ignoring the sign:\n`100/{} = {}cm`\nYou should be able to see {}cm with -{} myopia!\nFor help with DiopterBot, type `diopterbot`".format(diopter_value_formatted, result, result, diopter_value_formatted))
        elif differentials < 0:
            await channel.send("When wearing differentials, or any minus lens, the effective myopia of your eye reduces by the strength of the differentials, or glasses. We do the calculation with a diopter value of -{} instead of -{} because of this.\nTo calculate diopters from cm, do 100 divided by the diopter value, ignoring the sign:\n`100/{} = {}cm`\nYou should be able to see {}cm with -{} myopia!\nFor help with DiopterBot, type `diopterbot`".format(diopters_and_diffs_formatted, diopter_value_formatted, diopters_and_diffs_formatted, result, result, diopters_and_diffs_formatted))
        elif differentials > 0:
            await channel.send("If you are wearing plus lens the effective myopia of your eye increases by the strength of the lens. We do the calculation with a diopter value of -{} instead of -{} because of this.\nTo calculate diopters from cm, do 100 divided by the diopter value, ignoring the sign:\n`100/{} = {}cm`\nYou should be able to see {}cm with -{} myopia!\nFor help with DiopterBot, type `diopterbot`".format(diopters_and_diffs_formatted, diopter_value_formatted, diopters_and_diffs_formatted, result, result, diopters_and_diffs_formatted))

    async def diopterbot_help(self, channel):
        await channel.send(
            "DiopterBot can calculate the diopter value from a cm value that you give it, and vice versa. It can also perform calculations with differentials and tells you how to work out calculations for the future.\n\nTo use DiopterBot, type `convert (value) (differentials)`, only giving a value for differentials if you want to include this in the calculation. Examples:\n`convert 7cm` will convert 7cm into diopters\n`convert -2` will tell you the number of cms you can see with -2 myopia\n`convert 20cm -1` will tell you your myopia value if you measured 20cm with a -1 lens (differential) in that eye.")

    async def on_message(self, message):
        if message.content == self.user:
            return

        if message.content.strip().startswith('convert'):
            raw = message.content.lower()
            request = raw.split()
            # print(request)
            # print(len(request))
            if request[0] == 'convert' and len(request) < 2:
                await self.diopterbot_help(message.channel)
            if not 1 < len(request) < 4:
                return
            if len(request) == 2:
                if request[1] == 'help':
                    await self.diopterbot_help(message.channel)
                elif request[1].endswith('c') or request[1].endswith('cm') or request[1].endswith('cms'):
                    cm_value = request[1].split('c')[0]
                    await self.cm_to_diopters(message.channel, cm_value)
                elif request[1].startswith('-') or request[1].replace('.', '', 1).isdigit():
                    if request[1].endswith('d') or request[1].endswith('diopters') or request[1].endswith('dioptres'):
                        diopter_value = request[1].split('d')[0]
                    else:
                        diopter_value = request[1]
                    await self.diopters_to_cm(message.channel, diopter_value)
                elif request[1].endswith('d') or request[1].endswith('diopters') or request[1].endswith('dioptres'):
                    diopter_value = request[1].split('d')[0]
                    await self.diopters_to_cm(message.channel, diopter_value)
            elif len(request) == 3:
                if request[2].startswith('centi') or request[2].startswith('cm') or request[2].startswith('cms'):
                    try:
                        float(request[1])
                    except ValueError:
                        return
                    cm_value = request[1]
                    await self.cm_to_diopters(message.channel, cm_value)
                elif request[2].startswith('d'):
                    try:
                        float(request[1])
                    except ValueError:
                        return
                    diopter_value = request[1]
                    await self.diopters_to_cm(message.channel, diopter_value)
                elif request[1].endswith('cm') or request[1].endswith('cms') and request[2].startswith('-') or request[2].isdigit():
                    cm_value = request[1].split('c')[0]
                    await self.cm_to_diopters(message.channel, cm_value, differentials=request[2])
                elif request[1].startswith('-') or request[1].isdigit() and request[2].startswith('-') or request[2].isdigit():
                    diopter_value = request[1]
                    await self.diopters_to_cm(message.channel, diopter_value, differentials=request[2])

        if message.content.strip().startswith('diopterbot') and len(message.content.split()) < 3:
            await self.diopterbot_help(message.channel)

client = DiopterBot()
client.run('TOKEN')

import discord
import random
import asyncio
import logging
from discord import app_commands
from discord.ext import commands
from key import TOKEN

bot = commands.Bot(command_prefix = "!?!?!?!?!!!!!?!???@!@#!@#", intents = discord.Intents.all())
bot.remove_command('help')

logging.basicConfig(level=logging.INFO)

easter_egg_played = False
easter_egg_file_exists = True

try:
    easter_eggs_file = open('easter_eggs.txt')
    easter_eggs = easter_eggs_file.readlines()
    easter_eggs_file.close()
except FileNotFoundError:
    easter_egg_file_exists = False

@bot.event
async def on_ready():
    print("DiopterBot running")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

async def easter_egg(interaction):
    global easter_egg_played
    if not easter_egg_played and easter_egg_file_exists:
        egg = random.randint(0, (len(easter_eggs) - 1))
        await interaction.response.send_message(easter_eggs[egg])
    else:
        await interaction.response.send_message("¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁ ÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàá âãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀā ĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġ ĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁ łŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠš ŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž", delete_after=0)
    easter_egg_played = True
    await asyncio.sleep(1200)
    easter_egg_played = False

@bot.tree.command(name="cm-to-diopters", description="Converts a cm value to the diopter equivalent")
@app_commands.describe(close_up_correction = "differentials")
async def cm_to_diopters(interaction, cm: float, close_up_correction: float = 0.0):
    cm = abs(cm)
    if cm > 1000 or abs(close_up_correction) > 100:
        await easter_egg(interaction)
        return
    try:
        result = round((-100/cm), 2)
    except ZeroDivisionError:
        await interaction.response.send_message("You can't see anything? :face_with_monocle:")
        return
    result_with_diffs = result + (close_up_correction * -1)
    if result_with_diffs % 0.25 >= 0.125:
        formatted_result = format(0.25 * ((result_with_diffs // 0.25) + 1), '.2f')
    else:
        formatted_result = format(0.25 * (result_with_diffs // 0.25), '.2f')

    formatted_cms = format(cm, '.2f')
    formatted_raw_result = format(result, '.2f')
    result = format(result, '.2f')
    differentials_formatted = format(close_up_correction, '.2f')
    result_with_diffs = format(result_with_diffs, '.2f')

    myopia_or_hyperopia = 'Myopia'
    if float(formatted_result) > 0:
        formatted_result = '+' + formatted_result
        result_with_diffs = '+' + result_with_diffs
        myopia_or_hyperopia = 'Hyperopia'

    if close_up_correction == 0:
        await interaction.response.send_message(f"To calculate diopters, do 100 divided by the cm value, and add on a minus sign:\n`100 / {formatted_cms}cm = {formatted_raw_result} diopters\nMyopia of eye approximately {formatted_result} diopters`")
    elif close_up_correction < 0:
        await interaction.response.send_message(f"To calculate diopters, do 100 divided by the cm value, and add on a minus sign:\n`100 / {formatted_cms}cm = {result} diopters`\nBecause you measured with close-up glasses, add the strength of your close-up glasses as well:`\n{result} - ({differentials_formatted}) = {result_with_diffs} diopters\n{myopia_or_hyperopia} of eye approximately {formatted_result} diopters`")
    elif close_up_correction > 0:
        await interaction.response.send_message(f"To calculate diopters, do 100 divided by the cm value, and add on a minus sign:\n`100 / {formatted_cms}cm = {result} diopters`\nBecause you measured with plus lenses, subtract the strength of your plus lenses as well:`\n{result} - (+{differentials_formatted}) = {result_with_diffs} diopters\n{myopia_or_hyperopia} of eye approximately {formatted_result} diopters`")

@bot.tree.command(name="diopters-to-cm", description="Converts a diopter value to the cm equivalent")
@app_commands.describe(close_up_correction = "differentials")
async def diopters_to_cm(interaction, diopters: float, close_up_correction: float = 0.0):
    diopters = -abs(diopters)
    if abs(diopters) > 100 or abs(close_up_correction) > 100:
        await easter_egg(interaction)
        return
    if diopters > close_up_correction and close_up_correction != 0:
        await easter_egg(interaction)
        return
    diopters_and_diffs = diopters - close_up_correction
    try:
        result = abs(round((100/diopters_and_diffs), 2))
    except ZeroDivisionError:
        await interaction.response.send_message(":infinity:\nIn theory, these are not your close-up glasses but full strength glasses that correct you to perfect vision.\nYou can see to ∞!")
        return
    diopter_value_formatted = format(abs(diopters), '.2f')
    diopters_and_diffs_formatted = format(diopters_and_diffs, '.2f')
    differentials_formatted = format(close_up_correction, '.2f')
    diopters_and_diffs_formatted_no_sign = format(abs(diopters_and_diffs), '.2f')
    if close_up_correction == 0:
        await interaction.response.send_message(f"To calculate diopters to cm, do 100 divided by the diopter value, ignoring the sign:\n`100 / {diopter_value_formatted} = {result}cm`\nYou should be able to see {result}cm with {diopters_and_diffs_formatted} myopia!")
    elif close_up_correction < 0:
        await interaction.response.send_message(f"When wearing close-up glasses, or any minus lens, the effective myopia of your eye reduces by the strength of the glasses, and we do the next calculation with that value:\n`-{diopter_value_formatted} - ({differentials_formatted}) = {diopters_and_diffs_formatted} effective myopia`\nTo calculate diopters from cm, do 100 divided by the diopter value, ignoring all signs:\n`100 / {diopters_and_diffs_formatted_no_sign} = {result}cm`\nYou should be able to see {result}cm with {diopters_and_diffs_formatted} myopia!")
    elif close_up_correction > 0:
        await interaction.response.send_message(f"If you are wearing plus lenses the effective myopia of your eye increases by the strength of the lens, and we do the next calculation with that value:\n`-{diopter_value_formatted} - (+{differentials_formatted}) = {diopters_and_diffs_formatted} effective myopia`\nTo calculate diopters from cm, do 100 divided by the diopter value, ignoring all signs:\n`100 / {diopters_and_diffs_formatted_no_sign} = {result}cm`\nYou should be able to see {result}cm with {diopters_and_diffs_formatted} myopia!")

@bot.tree.command(name="help", description="Provides help about DiopterBot")
async def diopterbot_help(interaction):
    await interaction.response.send_message(
        "DiopterBot can calculate the diopter value from a cm value that you give it, and vice versa. It can also perform calculations with close-up glasses (differentials) and tells you how to work out calculations in the future.\n\nTo use DiopterBot, use the relevant slash command (/) with the required value and optional close-up value.")

bot.run(TOKEN)
from random import randrange
import asyncio


async def bravery(message, client, jungle):

  # CHOOSE CHAMPION
  champions = open('BraveryFiles/leagueChampions.txt', 'r')
  championList = champions.readlines()
  champion = 'Champion: ' + championList[randrange(len(championList))]
  champions.close()

  # CHOOSE SPELL
  with open("BraveryFiles/leagueSpells.txt") as spells:
    spellList = spells.read().splitlines()
  if jungle:
    num1 = 6
  else:
    num1 = randrange(len(spellList))
  num2 = randrange(len(spellList))
  while (num2 == num1):
    num2 = randrange(len(spellList))
  spell = 'Spells: ' + spellList[num1] + ' + ' + spellList[num2] + '\n'
  spells.close()

  # CHOOSE RUNES
  runePath = randrange(5)
  runeSecondary = randrange(5)
  while (runeSecondary == runePath):
    runeSecondary = randrange(5)
  shards = open('BraveryFiles/leagueRuneShards.txt', 'r')
  shardList = shards.readlines()
  runePrimary = ''
  runeSecond = ''

  precision = open('BraveryFiles/leagueRunePrecision.txt', 'r')
  precisionList = precision.readlines()
  domination = open('BraveryFiles/leagueRuneDomination.txt', 'r')
  dominationList = domination.readlines()
  sorcery = open('BraveryFiles/leagueRuneSorcery.txt', 'r')
  sorceryList = sorcery.readlines()
  resolve = open('BraveryFiles/leagueRuneResolve.txt', 'r')
  resolveList = resolve.readlines()
  inspiration = open('BraveryFiles/leagueRuneInspiration.txt', 'r')
  inspirationList = inspiration.readlines()

  # DETERMINE RUNE PRIMARY
  if runePath == 0:
    runePrimary = 'Runes: ' + '\nPrimary: Precision' + '\n-Keystone: ' + precisionList[
      randrange(1, 5)] + '-Slot 1: ' + precisionList[randrange(
        7, 10)] + '-Slot 2: ' + precisionList[randrange(
          12, 15)] + '-Slot 3: ' + precisionList[randrange(17, 20)]
  if runePath == 1:
    runePrimary = 'Runes: ' + '\nPrimary: Domination' + '\n-Keystone: ' + dominationList[
      randrange(1, 5)] + '-Slot 1: ' + dominationList[randrange(
        7, 10)] + '-Slot 2: ' + dominationList[randrange(
          12, 15)] + '-Slot 3: ' + dominationList[randrange(17, 21)]
  if runePath == 2:
    runePrimary = 'Runes: ' + '\nPrimary: Sorcery' + '\n-Keystone: ' + sorceryList[
      randrange(1, 4)] + '-Slot 1: ' + sorceryList[randrange(
        6, 9)] + '-Slot 2: ' + sorceryList[randrange(
          11, 14)] + '-Slot 3: ' + sorceryList[randrange(16, 19)]
  if runePath == 3:
    runePrimary = 'Runes: ' + '\nPrimary: Resolve' + '\n-Keystone: ' + resolveList[
      randrange(1, 4)] + '-Slot 1: ' + resolveList[randrange(
        6, 9)] + '-Slot 2: ' + resolveList[randrange(
          11, 14)] + '-Slot 3: ' + resolveList[randrange(16, 19)]
  if runePath == 4:
    runePrimary = 'Runes: ' + '\nPrimary: Inspiration' + '\n-Keystone: ' + inspirationList[
      randrange(1, 4)] + '-Slot 1: ' + inspirationList[randrange(
        6, 9)] + '-Slot 2: ' + inspirationList[randrange(
          11, 14)] + '-Slot 3: ' + inspirationList[randrange(16, 19)]

  num1 = randrange(2)
  num2 = randrange(1, 3)
  while (num2 == num1):
    num2 = randrange(1, 3)

  # DETERMINE RUNE SECONDARY
  if runeSecondary == 0:
    if num1 == 0:
      if num2 == 1:
        runeSecond = 'Secondary: Precision' + '\n-Slot 1: ' + precisionList[
          randrange(7, 10)] + '-Slot 2: ' + precisionList[randrange(
            12, 15)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
      else:
        runeSecond = 'Secondary: Precision' + '\n-Slot 1: ' + precisionList[
          randrange(7, 10)] + '-Slot 2: ' + precisionList[randrange(
            17, 20)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
    else:
      runeSecond = 'Secondary: Precision' + '\n-Slot 1: ' + precisionList[
        randrange(12, 15)] + '-Slot 2: ' + precisionList[randrange(
          17, 20)] + '-Shard 1: ' + shardList[randrange(
            1, 4)] + '-Shard 2: ' + shardList[randrange(
              6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
  elif runeSecondary == 1:
    if num1 == 0:
      if num2 == 1:
        runeSecond = 'Secondary: Domination' + '\n-Slot 1: ' + dominationList[
          randrange(7, 10)] + '-Slot 2: ' + dominationList[randrange(
            12, 15)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
      else:
        runeSecond = 'Secondary: Domination' + '\n-Slot 1: ' + dominationList[
          randrange(7, 10)] + '-Slot 2: ' + dominationList[randrange(
            17, 21)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
    else:
      runeSecond = 'Secondary: Domination' + '\n-Slot 1: ' + dominationList[
        randrange(12, 15)] + '-Slot 2: ' + dominationList[randrange(
          17, 21)] + '-Shard 1: ' + shardList[randrange(
            1, 4)] + '-Shard 2: ' + shardList[randrange(
              6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
  elif runeSecondary == 2:
    if num1 == 0:
      if num2 == 1:
        runeSecond = 'Secondary: Sorcery' + '\n-Slot 1: ' + sorceryList[
          randrange(6, 9)] + '-Slot 2: ' + sorceryList[randrange(
            11, 14)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
      else:
        runeSecond = 'Secondary: Sorcery' + '\n-Slot 1: ' + sorceryList[
          randrange(6, 9)] + '-Slot 2: ' + sorceryList[randrange(
            16, 19)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
    else:
      runeSecond = 'Secondary: Sorcery' + '\n-Slot 1: ' + sorceryList[
        randrange(11, 14)] + '-Slot 2: ' + sorceryList[randrange(
          16, 19)] + '-Shard 1: ' + shardList[randrange(
            1, 4)] + '-Shard 2: ' + shardList[randrange(
              6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
  elif runeSecondary == 3:
    if num1 == 0:
      if num2 == 1:
        runeSecond = 'Secondary: Resolve' + '\n-Slot 1: ' + resolveList[
          randrange(6, 9)] + '-Slot 2: ' + resolveList[randrange(
            11, 14)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
      else:
        runeSecond = 'Secondary: Resolve' + '\n-Slot 1: ' + resolveList[
          randrange(6, 9)] + '-Slot 2: ' + resolveList[randrange(
            16, 19)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
    else:
      runeSecond = 'Secondary: Resolve' + '\n-Slot 1: ' + resolveList[
        randrange(11, 14)] + '-Slot 2: ' + resolveList[randrange(
          16, 19)] + '-Shard 1: ' + shardList[randrange(
            1, 4)] + '-Shard 2: ' + shardList[randrange(
              6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
  elif runeSecondary == 4:
    if num1 == 0:
      if num2 == 1:
        runeSecond = 'Secondary: Inspiration' + '\n-Slot 1: ' + inspirationList[
          randrange(6, 9)] + '-Slot 2: ' + inspirationList[randrange(
            11, 14)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
      else:
        runeSecond = 'Secondary: Inspiration' + '\n-Slot 1: ' + inspirationList[
          randrange(6, 9)] + '-Slot 2: ' + inspirationList[randrange(
            16, 19)] + '-Shard 1: ' + shardList[randrange(
              1, 4)] + '-Shard 2: ' + shardList[randrange(
                6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
    else:
      runeSecond = 'Secondary: Inspiration' + '\n-Slot 1: ' + inspirationList[
        randrange(11, 14)] + '-Slot 2: ' + inspirationList[randrange(
          16, 19)] + '-Shard 1: ' + shardList[randrange(
            1, 4)] + '-Shard 2: ' + shardList[randrange(
              6, 9)] + '-Shard 3: ' + shardList[randrange(11, 14)]
  shards.close()
  precision.close()
  domination.close()
  sorcery.close()
  resolve.close()
  inspiration.close()

  # CHOOSE ABILITY UPGRADE ORDER
  abilities = ['Q', 'W', 'E']
  num1 = randrange(3)
  num2 = randrange(3)
  num3 = randrange(3)
  while (num2 == num1):
    num2 = randrange(3)
  while (num3 == num1 or num3 == num2):
    num3 = randrange(3)
  abilityOrder = 'Ability Upgrade Order: ' + abilities[
    num1] + ' -> ' + abilities[num2] + ' -> ' + abilities[num3]

  # CHOOSE WARD
  vision = [
    'Default Ward', 'Oracle Lens',
    'Blue Trinket (stay with default at beginning)'
  ]
  ward = '\nWard to Use: ' + vision[randrange(len(vision))]

  # CHOOSE ITEM
  itemCategories = [
    'fighter', 'marksman', 'assassin', 'mage', 'tank', 'support'
  ]
  boots = open('BraveryFiles/leagueItemBoots.txt', 'r')
  bootList = boots.readlines()
  fighter = open('BraveryFiles/leagueItemFighter.txt', 'r')
  fighterList = fighter.readlines()
  marksman = open('BraveryFiles/leagueItemMarksman.txt', 'r')
  marksmanList = marksman.readlines()
  assassin = open('BraveryFiles/leagueItemAssassin.txt', 'r')
  assassinList = assassin.readlines()
  mage = open('BraveryFiles/leagueItemMage.txt', 'r')
  mageList = mage.readlines()
  tank = open('BraveryFiles/leagueItemTank.txt', 'r')
  tankList = tank.readlines()
  support = open('BraveryFiles/leagueItemSupport.txt', 'r')
  supportList = support.readlines()

  # checking conditions for a response
  def check(response):
    return response.channel == message.channel and response.author == message.author

  await message.channel.send(
    champion + spell + runePrimary + runeSecond + abilityOrder + ward +
    '\nPick a category for items: Fighter, Marksman, Assassin, Mage, Tank, Support'
  )
  try:
    response = await client.wait_for("message", check=check, timeout=20)
    for item in itemCategories:
      if response.content.lower() == item:
        if item == 'fighter':
          num1 = randrange(8, 25)
          num2 = randrange(8, 25)
          num3 = randrange(8, 25)
          num4 = randrange(8, 25)
          while (num2 == num1):
            num2 = randrange(8, 25)
          while (num3 == num1 or num3 == num2):
            num3 = randrange(8, 25)
          while (num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(8, 25)
          await message.channel.send('Order of Items: \n' + '1. ' +
                                     fighterList[randrange(1, 6)] + '2. ' +
                                     bootList[randrange(len(bootList))] +
                                     '3. ' + fighterList[num1] + '4. ' +
                                     fighterList[num2] + '5. ' +
                                     fighterList[num3] + '6. ' +
                                     fighterList[num4])
          break
        if item == 'marksman':
          num1 = randrange(7, 25)
          num2 = randrange(7, 25)
          num3 = randrange(7, 25)
          num4 = randrange(7, 25)
          while (num2 == num1):
            num2 = randrange(7, 25)
          while (num3 == num1 or num3 == num2):
            num3 = randrange(7, 25)
          while (num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(7, 25)
          await message.channel.send('Order of Items: \n' + '1. ' +
                                     marksmanList[randrange(1, 5)] + '2. ' +
                                     bootList[randrange(len(bootList))] +
                                     '3. ' + marksmanList[num1] + '4. ' +
                                     marksmanList[num2] + '5. ' +
                                     marksmanList[num3] + '6. ' +
                                     marksmanList[num4])
          break
        if item == 'assassin':
          num1 = randrange(6, 21)
          num2 = randrange(6, 21)
          num3 = randrange(6, 21)
          num4 = randrange(6, 21)
          while (num2 == num1):
            num2 = randrange(6, 21)
          while (num3 == num1 or num3 == num2):
            num3 = randrange(6, 21)
          while (num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(6, 21)
          await message.channel.send('Order of Items: \n' + '1. ' +
                                     assassinList[randrange(1, 4)] + '2. ' +
                                     bootList[randrange(len(bootList))] +
                                     '3. ' + assassinList[num1] + '4. ' +
                                     assassinList[num2] + '5. ' +
                                     assassinList[num3] + '6. ' +
                                     assassinList[num4])
          break
        if item == 'mage':
          num1 = randrange(11, 25)
          num2 = randrange(11, 25)
          num3 = randrange(11, 25)
          num4 = randrange(11, 25)
          while (num2 == num1):
            num2 = randrange(11, 25)
          while (num3 == num1 or num3 == num2):
            num3 = randrange(11, 25)
          while (num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(11, 25)
          await message.channel.send('Order of Items: \n' + '1. ' +
                                     mageList[randrange(1, 9)] + '2. ' +
                                     bootList[randrange(len(bootList))] +
                                     '3. ' + mageList[num1] + '4. ' +
                                     mageList[num2] + '5. ' + mageList[num3] +
                                     '6. ' + mageList[num4])
          break
        if item == 'tank':
          num1 = randrange(9, 27)
          num2 = randrange(9, 27)
          num3 = randrange(9, 27)
          num4 = randrange(9, 27)
          while (num2 == num1):
            num2 = randrange(9, 27)
          while (num3 == num1 or num3 == num2):
            num3 = randrange(9, 27)
          while (num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(9, 27)
          await message.channel.send('Order of Items: \n' + '1. ' +
                                     tankList[randrange(1, 7)] + '2. ' +
                                     bootList[randrange(len(bootList))] +
                                     '3. ' + tankList[num1] + '4. ' +
                                     tankList[num2] + '5. ' + tankList[num3] +
                                     '6. ' + tankList[num4])
          break
        if item == 'support':
          num1 = randrange(8, 18)
          num2 = randrange(8, 18)
          num3 = randrange(8, 18)
          num4 = randrange(8, 18)
          while (num2 == num1):
            num2 = randrange(8, 18)
          while (num3 == num1 or num3 == num2):
            num3 = randrange(8, 18)
          while (num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(8, 18)
          await message.channel.send('Order of Items: \n' + '1. ' +
                                     supportList[randrange(1, 6)] + '2. ' +
                                     bootList[randrange(len(bootList))] +
                                     '3. ' + supportList[num1] + '4. ' +
                                     supportList[num2] + '5. ' +
                                     supportList[num3] + '6. ' +
                                     supportList[num4])
          break
    else:
      await message.channel.send('This is not a valid category!')
  except asyncio.TimeoutError:
    await message.channel.send('You failed to answer in time!')
  boots.close()
  fighter.close()
  marksman.close()
  assassin.close()
  mage.close()
  tank.close()
  support.close()

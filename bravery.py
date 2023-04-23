from random import randrange
import asyncio

async def bravery(message, client):

  # CHOOSE CHAMPION
  champions = open('BraveryFiles/leagueChampions.txt', 'r')
  championList = champions.readlines()
  await message.channel.send('Champion: ' + championList[randrange(len(championList))])
  champions.close()

  # CHOOSE SPELL
  with open("BraveryFiles/leagueSpells.txt") as spells:
    spellList = spells.read().splitlines()
  num1 = randrange(len(spellList))
  num2 = randrange(len(spellList))
  while(num2 == num1):
    num2 = randrange(len(spellList))
  await message.channel.send('Spells: ' + spellList[num1] + ' + ' + spellList[num2])
  spells.close()

  # CHOOSE RUNES
  runePath = randrange(5)
  runeSecondary = randrange(5)
  while(runeSecondary == runePath):
    runeSecondary = randrange(5)
  runeSecondarySlots = []
  shards = open('BraveryFiles/leagueRuneShards.txt', 'r')
  shardList = shards.readlines()

  if runeSecondary == 0:
    num1 = randrange(2)
    num2 = randrange(1,3)
    while(num2 == num1):
      num2 = randrange(1,3)
    if num1 == 0:
      if num2 == 1:
        runeSecondarySlots = [randrange(7,10),randrange(12,15)]
      else:
        runeSecondarySlots = [randrange(7,10),randrange(17,20)]
    else:
      runeSecondarySlots = [randrange(12,15), randrange(17,20)]
  elif runeSecondary == 1:
    num1 = randrange(2)
    num2 = randrange(1,3)
    while(num2 == num1):
      num2 = randrange(1,3)
    if num1 == 0:
      if num2 == 1:
        runeSecondarySlots = [randrange(7,10),randrange(12,15)]
      else:
        runeSecondarySlots = [randrange(7,10),randrange(17,21)]
    else:
      runeSecondarySlots = [randrange(12,15), randrange(17,21)]
  elif runeSecondary == 2 or runeSecondary == 3 or runeSecondary == 4:
    num1 = randrange(2)
    num2 = randrange(1,3)
    while(num2 == num1):
      num2 = randrange(1,3)
    if num1 == 0:
      if num2 == 1:
        runeSecondarySlots = [randrange(6,9),randrange(11,14)]
      else:
        runeSecondarySlots = [randrange(6,9),randrange(16,19)]
    else:
      runeSecondarySlots = [randrange(11,14), randrange(16,19)]
    
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
  
  if runePath == 0:
    await message.channel.send('Runes: ' + '\nPrimary: Precision' + '\n-Keystone: ' + precisionList[randrange(1,5)] + '-Slot 1: ' + precisionList[randrange(7,10)] + '-Slot 2: ' + precisionList[randrange(12,15)] + '-Slot 3: ' + precisionList[randrange(17,20)])
    if runeSecondary == 1:
      await message.channel.send('Secondary: Domination' + '\n-Slot 1: ' + dominationList[runeSecondarySlots[0]] + '-Slot 2: ' + dominationList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 2:
      await message.channel.send('Secondary: Sorcery' + '\n-Slot 1: ' + sorceryList[runeSecondarySlots[0]] + '-Slot 2: ' + sorceryList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 3:
      await message.channel.send('Secondary: Resolve' + '\n-Slot 1: ' + resolveList[runeSecondarySlots[0]] + '-Slot 2: ' + resolveList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 4:
      await message.channel.send('Secondary: Inspiration' + '\n-Slot 1: ' + inspirationList[runeSecondarySlots[0]] + '-Slot 2: ' + inspirationList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    
  if runePath == 1:
    await message.channel.send('Runes: ' + '\nPrimary: Domination' + '\n-Keystone: ' + dominationList[randrange(1,5)] + '-Slot 1: ' + dominationList[randrange(7,10)] + '-Slot 2: ' + dominationList[randrange(12,15)] + '-Slot 3: ' + dominationList[randrange(17,21)])
    if runeSecondary == 0:
      await message.channel.send('Secondary: Precision' + '\n-Slot 1: ' + precisionList[runeSecondarySlots[0]] + '-Slot 2: ' + precisionList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 2:
      await message.channel.send('Secondary: Sorcery' + '\n-Slot 1: ' + sorceryList[runeSecondarySlots[0]] + '-Slot 2: ' + sorceryList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 3:
      await message.channel.send('Secondary: Resolve' + '\n-Slot 1: ' + resolveList[runeSecondarySlots[0]] + '-Slot 2: ' + resolveList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 4:
      await message.channel.send('Secondary: Inspiration' + '\n-Slot 1: ' + inspirationList[runeSecondarySlots[0]] + '-Slot 2: ' + inspirationList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    
  if runePath == 2:
    await message.channel.send('Runes: ' + '\nPrimary: Sorcery' +'\n-Keystone: ' + sorceryList[randrange(1,4)] + '-Slot 1: ' + sorceryList[randrange(6,9)] + '-Slot 2: ' + sorceryList[randrange(11,14)] + '-Slot 3: ' + sorceryList[randrange(16,19)])
    if runeSecondary == 1:
      await message.channel.send('Secondary: Domination' + '\n-Slot 1: ' + dominationList[runeSecondarySlots[0]] + '-Slot 2: ' + dominationList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 0:
      await message.channel.send('Secondary: Precision' + '\n-Slot 1: ' + precisionList[runeSecondarySlots[0]] + '-Slot 2: ' + precisionList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 3:
      await message.channel.send('Secondary: Resolve' + '\n-Slot 1: ' + resolveList[runeSecondarySlots[0]] + '-Slot 2: ' + resolveList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 4:
      await message.channel.send('Secondary: Inspiration' + '\n-Slot 1: ' + inspirationList[runeSecondarySlots[0]] + '-Slot 2: ' + inspirationList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])

  if runePath == 3:
    await message.channel.send('Runes: ' + '\nPrimary: Resolve' +'\n-Keystone: ' + resolveList[randrange(1,4)] + '-Slot 1: ' + resolveList[randrange(6,9)] + '-Slot 2: ' + resolveList[randrange(11,14)] + '-Slot 3: ' + resolveList[randrange(16,19)])
    if runeSecondary == 1:
      await message.channel.send('Secondary: Domination' + '\n-Slot 1: ' + dominationList[runeSecondarySlots[0]] + '-Slot 2: ' + dominationList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 2:
      await message.channel.send('Secondary: Sorcery' + '\n-Slot 1: ' + sorceryList[runeSecondarySlots[0]] + '-Slot 2: ' + sorceryList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 0:
      await message.channel.send('Secondary: Precision' + '\n-Slot 1: ' + precisionList[runeSecondarySlots[0]] + '-Slot 2: ' + precisionList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 4:
      await message.channel.send('Secondary: Inspiration' + '\n-Slot 1: ' + inspirationList[runeSecondarySlots[0]] + '-Slot 2: ' + inspirationList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])

  if runePath == 4:
    await message.channel.send('Runes: ' + '\nPrimary: Inspiration' +'\n-Keystone: ' + inspirationList[randrange(1,4)] + '-Slot 1: ' + inspirationList[randrange(6,9)] + '-Slot 2: ' + inspirationList[randrange(11,14)] + '-Slot 3: ' + inspirationList[randrange(16,19)])
    if runeSecondary == 1:
      await message.channel.send('Secondary: Domination' + '\n-Slot 1: ' + dominationList[runeSecondarySlots[0]] + '-Slot 2: ' + dominationList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 2:
      await message.channel.send('Secondary: Sorcery' + '\n-Slot 1: ' + sorceryList[runeSecondarySlots[0]] + '-Slot 2: ' + sorceryList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 3:
      await message.channel.send('Secondary: Resolve' + '\n-Slot 1: ' + resolveList[runeSecondarySlots[0]] + '-Slot 2: ' + resolveList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
    elif runeSecondary == 0:
      await message.channel.send('Secondary: Precision' + '\n-Slot 1: ' + precisionList[runeSecondarySlots[0]] + '-Slot 2: ' + precisionList[runeSecondarySlots[1]] + '-Shard 1: ' + shardList[randrange(1,4)] + '-Shard 2: ' + shardList[randrange(6,9)] + '-Shard 3: ' + shardList[randrange(11,14)])
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
  while(num2 == num1):
    num2 = randrange(3)
  while(num3 == num1 or num3 == num2):
    num3 = randrange(3)
  await message.channel.send('Ability Upgrade Order: ' + abilities[num1] + ' -> ' + abilities[num2] + ' -> ' + abilities[num3])

  # CHOOSE WARD
  vision = ['Default Ward', 'Oracle Lens', 'Blue Trinket (stay with default at beginning)']
  await message.channel.send('Ward to Use: ' + vision[randrange(len(vision))])

  # CHOOSE ITEM
  itemCategories = ['fighter', 'marksman', 'assassin', 'mage', 'tank', 'support']
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


  await message.channel.send('Pick a category for items: Fighter, Marksman, Assassin, Mage, Tank, Support')
  try:
    response = await client.wait_for("message", timeout=20)
    for item in itemCategories:
      if response.content.lower() == item:
        if item == 'fighter':
          num1 = randrange(8,25)
          num2 = randrange(8,25)
          num3 = randrange(8,25)
          num4 = randrange(8,25)
          while(num2 == num1):
            num2 = randrange(8,25)
          while(num3 == num1 or num3 == num2):
            num3 = randrange(8,25)
          while(num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(8,25)
          await message.channel.send('Order of Items: \n' + '1. ' + fighterList[randrange(1,6)] + '2. ' + bootList[randrange(len(bootList))] + '3. ' + fighterList[num1] + '4. ' + fighterList[num2] + '5. ' + fighterList[num3] + '6. ' + fighterList[num4])
          break
        if item == 'marksman':
          num1 = randrange(7,25)
          num2 = randrange(7,25)
          num3 = randrange(7,25)
          num4 = randrange(7,25)
          while(num2 == num1):
            num2 = randrange(7,25)
          while(num3 == num1 or num3 == num2):
            num3 = randrange(7,25)
          while(num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(7,25)
          await message.channel.send('Order of Items: \n' + '1. ' + marksmanList[randrange(1,5)] + '2. ' + bootList[randrange(len(bootList))] + '3. ' + marksmanList[num1] + '4. ' + marksmanList[num2] + '5. ' + marksmanList[num3] + '6. ' + marksmanList[num4])
          break
        if item == 'assassin':
          num1 = randrange(6,21)
          num2 = randrange(6,21)
          num3 = randrange(6,21)
          num4 = randrange(6,21)
          while(num2 == num1):
            num2 = randrange(6,21)
          while(num3 == num1 or num3 == num2):
            num3 = randrange(6,21)
          while(num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(6,21)
          await message.channel.send('Order of Items: \n' + '1. ' + assassinList[randrange(1,4)] + '2. ' + bootList[randrange(len(bootList))] + '3. ' + assassinList[num1] + '4. ' + assassinList[num2] + '5. ' + assassinList[num3] + '6. ' + assassinList[num4])
        if item == 'mage':
          num1 = randrange(11,25)
          num2 = randrange(11,25)
          num3 = randrange(11,25)
          num4 = randrange(11,25)
          while(num2 == num1):
            num2 = randrange(11,25)
          while(num3 == num1 or num3 == num2):
            num3 = randrange(11,25)
          while(num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(11,25)
          await message.channel.send('Order of Items: \n' + '1. ' + mageList[randrange(1,9)] + '2. ' + bootList[randrange(len(bootList))] + '3. ' + mageList[num1] + '4. ' + mageList[num2] + '5. ' + mageList[num3] + '6. ' + mageList[num4])
        if item == 'tank':
          num1 = randrange(9,27)
          num2 = randrange(9,27)
          num3 = randrange(9,27)
          num4 = randrange(9,27)
          while(num2 == num1):
            num2 = randrange(9,27)
          while(num3 == num1 or num3 == num2):
            num3 = randrange(9,27)
          while(num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(9,27)
          await message.channel.send('Order of Items: \n' + '1. ' + tankList[randrange(1,7)] + '2. ' + bootList[randrange(len(bootList))] + '3. ' + tankList[num1] + '4. ' + tankList[num2] + '5. ' + tankList[num3] + '6. ' + tankList[num4])
        if item == 'support':
          num1 = randrange(8,18)
          num2 = randrange(8,18)
          num3 = randrange(8,18)
          num4 = randrange(8,18)
          while(num2 == num1):
            num2 = randrange(8,18)
          while(num3 == num1 or num3 == num2):
            num3 = randrange(8,18)
          while(num4 == num1 or num4 == num2 or num4 == num3):
            num4 = randrange(8,18)
          await message.channel.send('Order of Items: \n' + '1. ' + supportList[randrange(1,6)] + '2. ' + bootList[randrange(len(bootList))] + '3. ' + supportList[num1] + '4. ' + supportList[num2] + '5. ' + supportList[num3] + '6. ' + supportList[num4])
    else:
      await message.channel.send('This is not a valid category!')
  except asyncio.TimeoutError:
    await message.channel.send('You failed to answer in time!')
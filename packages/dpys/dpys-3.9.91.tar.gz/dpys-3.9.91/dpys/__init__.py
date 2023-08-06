import os
import discord
import asyncio
import datetime
import aiosqlite


print("""
===========================================================================================

 DPYS is a really good library if you know how to use it.

-------------------------------------------------------------------------------------------

 We recommend that you read https://sites.google.com/view/dpys before you use the library.
 
===========================================================================================
""")
async def reload(bat, dir, client):
    os.chdir(dir)
    os.startfile(bat)
    await client.close()
class admin():
    async def mute(ctx, member, *args, role_add=1, role_remove=1, reason=None, **kwargs):
        if ctx.guild.get_role(role_add) in member.roles:
            embed = discord.Embed(color = 0xD40C00, description = f"**{member.name}#{member.discriminator} is already muted.**")
            await ctx.send(embed=embed, delete_after=5)
        else:
            await member.add_roles(ctx.guild.get_role(role_add))
            if role_remove != 1:
                await member.remove_roles(ctx.guild.get_role(role_remove))
            if reason == None:
                embed = discord.Embed(color = 0x32c12c, description = f"**Muted {member.name}#{member.discriminator}.**")
                await ctx.send(embed=embed, delete_after=7)
            else:
                embed = discord.Embed(color = 0x32c12c, description = f"**Muted {member.name}#{member.discriminator}. Reason: {reason}**")
                await ctx.send(embed=embed, delete_after=7)

    async def unmute(ctx, member, *args, role_add=1, role_remove=1, **kwargs):
        if ctx.guild.get_role(role_remove) not in member.roles:
            embed = discord.Embed(color = 0xD40C00, description = f"**{member.name}#{member.discriminator} is not muted.**")
            await ctx.send(embed=embed, delete_after=5)
        else:
            await member.remove_roles(ctx.guild.get_role(role_remove))
            if role_add != 1:
                await member.add_roles(ctx.guild.get_role(role_add))
            embed = discord.Embed(color = 0x32c12c, description = f"**Unmuted {member.name}#{member.discriminator}.**")
            await ctx.send(embed=embed, delete_after=7)

    async def clear(ctx, amount=None):
        if amount == None:
            amount = 99999999999999999
        else:
            amount = int(amount)
        limit = datetime.datetime.now() - datetime.timedelta(weeks=2)
        await ctx.message.delete()
        purged = await ctx.channel.purge(limit=amount ,after=limit)
        purged = len(purged)
        embed = discord.Embed(color = 0x32c12c, description = f"**Cleared {purged} messages.**")
        await ctx.send(embed=embed, delete_after=5)
        return purged

    async def kick(ctx, member, reason=None):
        await member.kick(reason=reason)
        if reason is None:
            embed = discord.Embed(color = 0x32c12c, description = f"**Kicked {member.name}#{member.discriminator}.**")
            await ctx.send(embed=embed, delete_after=7)
        else:
            embed = discord.Embed(color = 0x32c12c, description = f"**Kicked {member.name}#{member.discriminator}. Reason: {reason}**")
            await ctx.send(embed=embed, delete_after=7)

    async def ban(ctx, member, reason=None):
        await member.ban(reason=reason)
        if reason is None:
            embed = discord.Embed(color = 0x32c12c, description = f"**Banned {member.name}#{member.discriminator}.**")
            await ctx.send(embed=embed, delete_after=7)
        else:
            embed = discord.Embed(color = 0x32c12c, description = f"**Banned {member.name}#{member.discriminator}. Reason: {reason}**")
            await ctx.send(embed=embed, delete_after=7)

    async def softban(ctx, member, reason=None):
        await member.ban(reason=reason)
        if reason is None:
            embed = discord.Embed(color = 0x32c12c, description = f"**Soft banned {member.name}#{member.discriminator}.**")
            await ctx.send(embed=embed, delete_after=7)
        else:
            embed = discord.Embed(color = 0x32c12c, description = f"**Soft banned {member.name}#{member.discriminator}. Reason: {reason}**")
            await ctx.send(embed=embed, delete_after=7)
        await member.unban()

    async def unban(ctx, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users: 
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(color = 0xD40C00, description = f"**Unbanned {member.name}#{member.discriminator}.**")
                await ctx.send(embed=embed, delete_after=7)
            else:
                embed = discord.Embed(color = 0xD40C00, description = f"**{member.name}#{member.discriminator} is not banned.**")
                await ctx.send(embed=embed, delete_after=5)
class curse():
    async def add_banned_word(ctx, word, dir):
        arg = word
        os.chdir(dir)
        word = word.lower()
        guildid = str(ctx.guild.id)
        db = await aiosqlite.connect("curse.db")
        await db.execute(f"""CREATE TABLE if NOT EXISTS curses(
        curse TEXT,
        guild TEXT
        )""")
        await db.commit()
        async with db.execute("SELECT curse FROM curses WHERE guild = ?", (guildid,)) as cursor:
            async for entry in cursor:
                curse = entry[0]
                words = word.replace(" ", "")
                words = words.split(",")
                for x in words:
                    if x == curse:
                        if "," in arg:
                            msg = f"**One of those words are already in the list.**"
                        else:
                            msg = f"**That word is already in the list.**"
                        embed = discord.Embed(color = 0xD40C00, description = msg)
                        await ctx.send(embed=embed, delete_after=5)
                        return
            word = word.replace(" ", "")
            word = word.split(",")
            for x in word:
                if word.count(x) > 1:
                    embed = discord.Embed(color = 0xD40C00, description = "**Words cannot be added twice.**")
                    await ctx.send(embed=embed, delete_after=5)
                    return
                await db.execute("INSERT INTO curses (curse,guild) VALUES (?,?)", (x,guildid))
            await db.commit()
        await db.close()
        embed = discord.Embed(color = 0x32c12c, description = "**Added to the list.**")
        await ctx.send(embed=embed, delete_after=7)
    async def remove_banned_word(ctx, word, dir):
            db = await aiosqlite.connect("curse.db")
            guildid = str(ctx.guild.id)
            os.chdir(dir)
            try:
                word = word.lower()
                word = word.replace(" ", "")
                word = word.split(",")
                async with db.execute("SELECT curse FROM curses WHERE guild = ?", (guildid,)) as cursor:
                    in_db = False
                    async for entry in cursor:
                        curse = entry[0]
                        for x in word:
                            if x == curse:
                                in_db = True
                if in_db == False:
                    if len(word) > 1:
                        embed = discord.Embed(color = 0xD40C00, description = "**None of those words are in the list.**")
                        await ctx.send(embed=embed, delete_after=5)
                    else:
                        embed = discord.Embed(color = 0xD40C00, description = "**That word is not in the list.**")
                        await ctx.send(embed=embed, delete_after=5)
                    return 
                for x in word:
                    await db.execute("DELETE FROM curses WHERE curse = ? and guild = ?", (x,guildid))
                    await db.commit()
                await db.close()
                embed = discord.Embed(color = 0x32c12c, description = "**Removed from the list.**")
                await ctx.send(embed=embed, delete_after=5)
            except:
                embed = discord.Embed(color = 0xD40C00, description = "**A list has not been created yet.**")
                await ctx.send(embed=embed, delete_after=5)
                await db.close()
    async def message_filter(message, dir, admin: int=1):
        if message.author.bot or message.guild is None:
            return
        os.chdir(dir)
        guildid = str(message.guild.id)
        if message.author.bot:
            return
        else:
            if admin != 1:
                adminrole = message.guild.get_role(admin)
                if adminrole in message.author.roles or message.author.top_role.position > adminrole.position or message.author.bot:
                    return
                else:    
                    try:
                        messagecontent = message.content.lower()
                        db = await aiosqlite.connect("curse.db")
                        async with db.execute("SELECT curse FROM curses WHERE guild = ?", (guildid,)) as cursor:
                            async for entry in cursor:
                                if entry[0] in messagecontent.split():
                                    await message.delete()
                                    await message.channel.send("Do not say that here!", delete_after=5)
                        await db.close()
                    except:
                        await db.close()
                        return

            else:
                    try:
                        messagecontent = message.content.lower()
                        db = await aiosqlite.connect("curse.db")
                        async with db.execute("SELECT curse FROM curses WHERE guild = ?", (guildid,)) as cursor:
                            async for entry in cursor:
                                if entry[0] in messagecontent.split():
                                    await message.delete()
                                    await message.channel.send("Do not say that here!", delete_after=5)
                        await db.close()
                    except:
                        await db.close()
                        return
    async def message_edit_filter(after, dir, admin: int=1):
        message = after
        if message.author.bot or message.guild is None:
            return
        os.chdir(dir)
        guildid = str(message.guild.id)
        if message.author.bot:
            return
        else:
            if admin != 1:
                adminrole = message.guild.get_role(admin)
                if adminrole in message.author.roles or message.author.top_role.position > adminrole.position or message.author.bot:
                    return
                else:    
                    try:
                        messagecontent = message.content.lower()
                        db = await aiosqlite.connect("curse.db")
                        async with db.execute("SELECT curse FROM curses WHERE guild = ?", (guildid,)) as cursor:
                            async for entry in cursor:
                                if entry[0] in messagecontent.split():
                                    await message.delete()
                                    await message.channel.send("Do not say that here!", delete_after=5)
                        await db.close()
                    except:
                        await db.close()
                        return

            else:
                    try:
                        messagecontent = message.content.lower()
                        db = await aiosqlite.connect("curse.db")
                        async with db.execute("SELECT curse FROM curses WHERE guild = ?", (guildid,)) as cursor:
                            async for entry in cursor:
                                if entry[0] in messagecontent.split():
                                    await message.delete()
                                    await message.channel.send("Do not say that here!", delete_after=5)
                        await db.close()
                    except:
                        await db.close()
                        return

    async def clear_words(ctx, dir):
        guildid = str(ctx.guild.id)
        os.chdir(dir)
        try:
            db = await aiosqlite.connect("curse.db")
            await db.execute("DELETE FROM curses WHERE guild = ?", (guildid,))
            await db.commit()
            await ctx.send("Cleared all curses from this server", delete_after=7)
            await db.close()
        except:
            embed = discord.Embed(color = 0xD40C00, description = "**There is not a curse list for this server. Create one by doing !addword followed by a list of words or a single word.**")
            await ctx.send(embed=embed, delete_after=5)
            await db.close() 
class mute_on_join():
    async def mute_add(ctx, member, dir):
        os.chdir(dir)
        guildid = str(ctx.guild.id)
        member = str(member.id)
        try:
            db = await aiosqlite.connect("muted.db")
            await db.execute(f"""CREATE TABLE if NOT EXISTS muted(
            name TEXT PRIMARY KEY,
            guild TEXT
            )""")
            await db.commit()
            await db.execute("INSERT INTO muted (name,guild) VALUES (?,?)", (member,guildid))
            await db.commit()
            await db.close()
        except:
            await db.close()
    
        

    async def mute_remove(ctx, member, dir):
        member = str(member.id)
        guildid = str(ctx.guild.id)
        os.chdir(dir)
        try:
            db = await aiosqlite.connect("muted.db")
            await db.execute("DELETE FROM muted WHERE name = ? and guild = ?", (member,guildid))
            await db.commit()
            await db.close()
        except:
            await db.close()
            return

    async def mute_on_join(member, role, dir):
        user = member
        guildid = str(member.guild.id)
        muted_role = member.guild.get_role(role)
        os.chdir(dir)
        member = str(member.id)
        try:
            db = await aiosqlite.connect("muted.db")
            async with db.execute("SELECT name FROM muted WHERE guild = ?", (guildid,)) as cursor:
                async for entry in cursor:
                    if entry[0] == member:
                        await user.add_roles(muted_role)
            await db.close()
        except:
            await db.close()

    async def manual_unmute_check(after, roleid, dir):
        os.chdir(dir)
        if after.bot:
            return
        guildid = str(after.guild.id)
        role = after.guild.get_role(roleid)
        db = await aiosqlite.connect("muted.db")
        memberid = str(after.id)
        try:
            if role not in after.roles:
                await db.execute("DELETE FROM muted WHERE guild = ? and name = ?", (guildid,memberid))
                await db.commit()
                await db.close()
        except:
            pass
class warnings():
    async def warn(ctx, member, dir, reason=None):
        os.chdir(dir)
        reason = str(reason)
        guildid = str(ctx.guild.id)
        user = member
        member = str(member.id)
        db = await aiosqlite.connect("warnings.db")
        await db.execute("""CREATE TABLE if NOT EXISTS warnings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        guild TEXT,
        reason TEXT
        )""")
        await db.commit()
        await db.execute("INSERT INTO warnings (member_id,guild,reason) VALUES (?,?,?)", (member,guildid,reason))
        await db.commit()
        await db.close()
        if reason == None:
            embed = discord.Embed(color = 0x32c12c, description = f"**Warned {user.name}#{user.discriminator}.**")
            await ctx.send(embed=embed, delete_after=7)
        else:
            embed = discord.Embed(color = 0x32c12c, description = f"**Warned {user.name}#{user.discriminator}. Reason: {reason}**")
            await ctx.send(embed=embed, delete_after=7)
    async def warnings_list(ctx, member, dir):
            os.chdir(dir)
            guildid = str(ctx.guild.id)
            user = member
            member = str(member.id)
            try:
                db = await aiosqlite.connect("warnings.db")
                async with db.execute("SELECT reason FROM warnings WHERE guild = ? and member_id = ?", (guildid,member)) as cursor:
                    embed = discord.Embed(color = 0x0000FF, title = f"{user.name}#{user.discriminator}'s Warnings")
                    number = 0
                    async for entry in cursor:
                        number += 1
                        embed.add_field(name=f"#{number} warning", value=f"Reason: {entry[0]}", inline=False)
                    if number > 0:
                        embed.set_footer(text=f"Total Warnings | {number}")
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(color = 0xD40C00, description = f"**{user.name}#{user.discriminator} has no warnings.**")
                        await ctx.send(embed=embed, delete_after=5)
                await db.close()
            except:
                embed = discord.Embed(color = 0xD40C00, description = f"**{user.name}#{user.discriminator} has no warnings.**")
                await ctx.send(embed=embed, delete_after=5)
                await db.close()
    async def unwarn(ctx, member, dir, number):
        os.chdir(dir)
        user = member
        guild = str(ctx.guild.id)
        member = str(member.id)
        number = str(number)
        number = number.lower()
        db = await aiosqlite.connect("warnings.db")
        async with db.execute("SELECT reason FROM warnings WHERE guild = ? and member_id = ?", (guild,member)) as cursor:
            count = 0
            async for entry in cursor:
                count += 1
        if count < 1:
            embed = discord.Embed(color = 0xD40C00, description = f"**{user.name}#{user.discriminator} has no warnings.**")
            await ctx.send(embed=embed, delete_after=5)
            return
        if number == "all":
            await db.execute("DELETE FROM warnings WHERE guild = ? and member_id = ?", (guild,member))
            await db.commit()
            await db.close()
            embed = discord.Embed(color = 0x32c12c, description = f"**Cleared all warnings from {user.name}#{user.discriminator}.**")
            await ctx.send(embed=embed, delete_after=7)
            return
        else:
                try:
                    if "," in number:
                        number = number.replace(" ", "")
                        number_list = number.split(",")
                        number_list = list(map(int, number_list))
                        number_list = sorted(number_list, reverse=True)
                        dict = {}
                        async with db.execute("SELECT id,row_number() OVER (ORDER BY id) FROM warnings WHERE guild = ? and member_id = ?", (guild,member)) as cursor:
                            async for entry in cursor:
                                id,pos = entry
                                pos = str(pos)
                                dict.update({pos:id})
                        for x in number_list:
                            await db.execute("DELETE FROM warnings WHERE id = ?", (dict[str(x)],))
                        await db.commit()
                        await db.close()
                        number_list = list(map(str, number_list))
                        number_list = ", ".join(number_list)
                        await ctx.send(f"Cleared warnings {number_list} from {user.mention}.", delete_after=7)
                        embed = discord.Embed(color = 0x32c12c, description = f"**Cleared warnings {number_list} from .{user.name}#{user.discriminator}.**")
                        await ctx.send(embed=embed, delete_after=7)
                    else:
                        number = int(number)
                        dict = {}
                        async with db.execute("SELECT id,row_number() OVER (ORDER BY id) FROM warnings WHERE guild = ? and member_id = ?", (guild,member)) as cursor:
                            async for entry in cursor:
                                id,pos = entry
                                pos = str(pos)
                                dict.update({pos:id})
                        await db.execute("DELETE FROM warnings WHERE id = ?", (dict[str(number)],))
                        await db.commit()
                        await db.close()
                        embed = discord.Embed(color = 0x32c12c, description = f"**Cleared {user.name}#{user.discriminator}'s' #{number} warning.**")
                        await ctx.send(embed=embed, delete_after=7)
                except:
                    if number == "all":
                        embed = discord.Embed(color = 0xD40C00, description = f"**{user.name}#{user.discriminator} has no warnings.**")
                        await ctx.send(embed=embed, delete_after=5)
                    else:
                        embed = discord.Embed(color = 0xD40C00, description = f"**{user.name}#{user.discriminator} does not have that many warnings.**")
                        await ctx.send(embed=embed, delete_after=5)
    async def punish(ctx, member, dir, *args, one=None, two=None, three=None, four=None, five=None, six=None, seven=None, eight=None, nine=None, ten=None, eleven=None, twelve=None, thirteen=None, fourteen=None, fifteen=None, remove_role=None, add_role=None, **kwargs):
                    os.chdir(dir)
                    memberid = str(member.id)
                    guild = str(ctx.guild.id)
                    db = await aiosqlite.connect("warnings.db")
                    async with db.execute("SELECT reason FROM warnings WHERE guild = ? and member_id = ?", (guild,memberid)) as cursor:
                        warnings_number = 0
                        async for entry in cursor:
                            warnings_number += 1
                    if warnings_number == 1:
                        warnings_number_str = one
                        message = "You received your first warning."
                    if warnings_number == 2:
                        warnings_number_str = two
                        message = "You received your second warning."
                    if warnings_number == 3:
                        warnings_number_str = three
                        message = "You received your third warning."
                    if warnings_number == 4:
                        warnings_number_str = four
                        message = "You received your fourth warning."
                    if warnings_number == 5:
                        warnings_number_str = five
                        message = "You received your fith warning."
                    if warnings_number == 6:
                        warnings_number_str = six
                        message = "You received your sixth warning."
                    if warnings_number == 7:
                        warnings_number_str = seven
                        message = "You received your seventh warning."
                    if warnings_number == 8:
                        warnings_number_str = eight
                        message = "You received your eighth warning."
                    if warnings_number == 9:
                        warnings_number_str = nine
                        message = "You received your ninth warning."
                    if warnings_number == 10:
                        warnings_number_str = ten
                        message = "You received your tenth warning."
                    if warnings_number == 11:
                        warnings_number_str = eleven
                        message = "You received your eleventh warning."
                    if warnings_number == 12:
                        warnings_number_str = twelve
                        message = "You received your twelfth warning."
                    if warnings_number == 13:
                        warnings_number_str = thirteen
                        message = "You received your thirteenth warning."
                    if warnings_number == 14:
                        warnings_number_str = fourteen
                        message = "You received your fourteenth warning."
                    if warnings_number == 15:
                        warnings_number_str = fifteen
                        message = "You received your fifteenth warning."
                    if warnings_number_str == None:
                        return
                    if "temp" in warnings_number_str:
                        pun_time = warnings_number_str[5:]
                        pun, time = pun_time.split("_")
                        time = time.lower()
                        if pun == "ban":
                            if "s" in time:
                                time = int(time[:-1])
                                await member.ban(reason=message)
                                await asyncio.sleep(time)
                                member.unban()
                                return
                            if "m" in time:
                                time = int(time[:-1])*60
                                await member.ban(reason=message)
                                await asyncio.sleep(time)
                                member.unban()
                                return
                            if "h" in time:
                                time = int(time[:-1])*3600
                                await member.ban(reason=message)
                                await asyncio.sleep(time)
                                member.unban()
                                return
                            if "d" in time:
                                time = int(time[:-1])*86400
                                await member.ban(reason=message)
                                await asyncio.sleep(time)
                                member.unban()
                                return
                            
                        else:
                            add_role = ctx.guild.get_role(add_role)
                            if remove_role != None:
                                remove_role = ctx.guild.get_role(remove_role)
                                if add_role in member.roles:
                                    return
                                else:
                                    if "s" in time:
                                        time = int(time[:-1])
                                        await member.add_roles(add_role)
                                        await member.remove_roles(remove_role)
                                        await mute_on_join.mute_add(ctx, member, dir)
                                        await asyncio.sleep(time)
                                        await member.add_roles(remove_role)
                                        await member.remove_roles(add_role)
                                        await mute_on_join.mute_remove(ctx, member, dir)
                                        return
                                    if "m" in time:
                                        time = int(time[:-1])*60
                                        await member.add_roles(add_role)
                                        await member.remove_roles(remove_role)
                                        await mute_on_join.mute_add(ctx, member, dir)
                                        await asyncio.sleep(time)
                                        await member.add_roles(remove_role)
                                        await member.remove_roles(add_role)
                                        await mute_on_join.mute_remove(ctx, member, dir)
                                        return
                                    if "h" in time:
                                        time = int(time[:-1])*3600
                                        await member.add_roles(add_role)
                                        await member.remove_roles(remove_role)
                                        await mute_on_join.mute_add(ctx, member, dir)
                                        await asyncio.sleep(time)
                                        await member.add_roles(remove_role)
                                        await member.remove_roles(add_role)
                                        await mute_on_join.mute_remove(ctx, member, dir)
                                        return
                                    if "d" in time:
                                        time = int(time[:-1])*86400
                                        await member.add_roles(add_role)
                                        await member.remove_roles(remove_role)
                                        await mute_on_join.mute_add(ctx, member, dir)
                                        await asyncio.sleep(time)
                                        await member.add_roles(remove_role)
                                        await member.remove_roles(add_role)
                                        await mute_on_join.mute_remove(ctx, member, dir)
                                        return
                            else:
                                    if "s" in time:
                                        time = int(time[:-1])
                                        await member.add_roles(add_role)
                                        await mute_on_join.mute_add(ctx, member, dir)
                                        await asyncio.sleep(time)
                                        await member.remove_roles(add_role)
                                        await mute_on_join.mute_remove(ctx, member, dir)
                                        return
                                    if "m" in time:
                                        time = int(time[:-1])*60
                                        await member.add_roles(add_role)
                                        await mute_on_join.mute_add(ctx, member, dir)
                                        await asyncio.sleep(time)
                                        await member.remove_roles(add_role)
                                        await mute_on_join.mute_remove(ctx, member, dir)
                                        return
                                    if "h" in time:
                                        time = int(time[:-1])*3600
                                        await member.add_roles(add_role)  
                                        await mute_on_join.mute_add(ctx, member, dir)                                 
                                        await asyncio.sleep(time)
                                        await member.remove_roles(add_role)
                                        await mute_on_join.mute_remove(ctx, member, dir)
                                        return
                                    if "d" in time:
                                        time = int(time[:-1])*86400
                                        await member.add_roles(add_role)
                                        await mute_on_join.mute_add(ctx, member, dir)
                                        await asyncio.sleep(time)                                   
                                        await member.remove_roles(add_role)
                                        await mute_on_join.mute_remove(ctx, member, dir)
                                        return
                    else:
                        if warnings_number_str == "ban":
                            await member.ban(reason=message)
                            return
                        if warnings_number_str == "kick":
                            await member.kick(reason=message)
                            return
                        if warnings_number_str == "mute":
                            add_role = ctx.guild.get_role(add_role)
                            if remove_role != None:
                                remove_role = ctx.guild.get_role(remove_role)
                                if add_role in member.roles:
                                    return
                                else:
                                    await member.add_roles(add_role)
                                    await member.remove_roles(remove_role)
                                    await mute_on_join.mute_add(ctx, member, dir)
                            else:
                                await member.add_roles(add_role)
                                await mute_on_join.mute_add(ctx, member, dir)
class rr():
    async def command(ctx, emoji, dir, role, *args, title, description, **kwargs):
        os.chdir(dir)
        db = await aiosqlite.connect("rr.db")
        await db.execute("""CREATE TABLE IF NOT EXISTS rr(
        msg_id TEXT,
        emoji UNICODE,
        role TEXT,
        guild TEXT,
        channel TEXT
        )""")
        await db.commit()
        embed = discord.Embed(title = title, color = 0x0000FF, description = description)
        msg = await ctx.send(embed=embed)
        if "," in emoji:
            emoji = emoji.replace(" ", "")
            emoji_list = emoji.split(",")
            role = role.replace(" ", "")
            role_list = role.split(",")
            number = 0
            for x in emoji_list:
                role = role_list[number]
                if "@" not in role:
                    embed = discord.Embed(color = 0xD40C00, description = "**Invalid Role**")
                    await ctx.send(embed=embed, delete_after=5)
                    return
                role = role.replace("<", "")
                role = role.replace(">", "")
                role = role.replace("@", "")
                role = role.replace("&", "")
                number += 1
                await msg.add_reaction(x)
                await db.execute("INSERT INTO rr (msg_id,emoji,role,guild,channel) VALUES (?,?,?,?,?)", (str(msg.id),x,str(role),str(ctx.guild.id),str(ctx.channel.id)))
            await db.commit()
            await db.close()
        else:
            await msg.add_reaction(emoji)
            if "@" not in role:
                embed = discord.Embed(color = 0xD40C00, description = "**Invalid Role**")
                await ctx.send(embed=embed, delete_after=15)
                return
            role = role.replace("<", "")
            role = role.replace(">", "")
            role = role.replace("@", "")
            role = role.replace("&", "")
            await db.execute("INSERT INTO rr (msg_id,emoji,role,guild,channel) VALUES (?,?,?,?,?)", (str(msg.id),emoji,str(role),str(ctx.guild.id),str(ctx.channel.id)))
            await db.commit()
            await db.close()

    async def add(payload, dir, client):
        os.chdir(dir)
        if payload.member.bot:
            return
        guild = client.get_guild(payload.guild_id)
        db = await aiosqlite.connect("rr.db")
        async with db.execute("SELECT emoji,role FROM rr WHERE guild = ? and msg_id = ?", (str(guild.id),str(payload.message_id))) as cursor:
            async for entry in cursor:
                emoji,role = entry
                role = guild.get_role(int(role))
                if str(payload.emoji) == emoji:
                    await payload.member.add_roles(role)
        await db.close()

    async def remove(payload, dir, client):
        os.chdir(dir)
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.bot:
            return
        db = await aiosqlite.connect("rr.db")
        async with db.execute("SELECT emoji,role FROM rr WHERE guild = ? and msg_id = ?", (str(guild.id),str(payload.message_id))) as cursor:
            async for entry in cursor:
                emoji,role = entry
                role = guild.get_role(int(role))
                if str(payload.emoji) == emoji:
                    await member.remove_roles(role)
        await db.close()

    async def clear_all(ctx, dir):
        os.chdir(dir)
        guild = str(ctx.guild.id)
        db = await aiosqlite.connect("rr.db")
        await db.execute("DELETE FROM rr WHERE guild = ?", (guild,))
        await db.commit()
        await db.close()
        embed = discord.Embed(color = 0x32c12c, description = "**Deleted all reaction role info for this server.**")
        await ctx.send(embed=embed, delete_after=7)
        

    async def clear_one(ctx, dir, message_id):
        os.chdir(dir)
        guild = str(ctx.guild.id)
        message_id = str(message_id)
        db = await aiosqlite.connect("rr.db")
        message_id = message_id.replace(" ", "")
        message_id = message_id.split(",")
        for x in message_id:
            await db.execute("DELETE FROM rr WHERE guild = ? and msg_id = ?", (guild,x))
        await db.commit()
        await db.close()
        message_id = ", ".join(message_id)
        embed = discord.Embed(color = 0x32c12c, description = f"**Delted reaction role info for {message_id}**")
        await ctx.send(embed=embed, delete_after=7)

    async def clear_rr(message, dir):
        os.chdir(dir)
        guild = str(message.guild.id)
        id = str(message.id)
        db = await aiosqlite.connect("rr.db")
        async with db.execute("SELECT msg_id FROM rr WHERE guild = ?", (guild,)) as cursor:
            async for entry in cursor:
                msg_id = entry[0]
                if msg_id == id:
                    await db.execute("DELETE FROM rr WHERE msg_id = ? and guild = ?", (msg_id,guild))
                    await db.commit()
                    return
        await db.close()
        
    async def display(ctx, dir):
        limit = "limit"
        os.chdir(dir)
        guild = str(ctx.guild.id)
        db = await aiosqlite.connect("rr.db")
        embed = discord.Embed(title="Reaction Roles", color = 0x0000FF)
        async with db.execute("SELECT msg_id FROM rr  WHERE guild = ? GROUP BY msg_id", (guild,)) as cursor:
            number = 0
            async for entry in cursor:
                number += 1
                async with db.execute("SELECT role,emoji,channel,msg_id FROM rr WHERE guild = ? and msg_id = ?", (guild,entry[0])) as f:
                    msg = ""
                    msg_limit = ""
                    async for entry in f:
                        role,emoji,channel,msg_id = entry
                        channel = ctx.guild.get_channel(int(channel))
                        role = ctx.guild.get_role(int(role))
                        try:
                            role = role.mention
                        except:
                            role = "@deleted-role"
                        try:
                            channel = channel.mention
                        except:
                            channel = "#deleted-channel"
                        msg += f"Emoji: {emoji} Role: {role}\n"
                    msg_limit += f"Channel: {channel} Message ID: {msg_id}\n"
                    msg += f"Channel: {channel} Message ID: {msg_id}\n"
                if len(msg) > 1010:
                    embed.add_field(name=f"Reaction Role #{number}", inline=False, value=msg_limit)
                    limit = "True"
                else:
                    embed.add_field(name=f"Reaction Role #{number}", inline=False, value=msg)
        if number > 0:
            if limit == "limit":
                embed.set_footer(text=f"Total Reaction Roles | {number}")
            else:
                embed.set_footer(text=f"Total Reaction Roles | {number}")
                limit_embed = discord.Embed(color = 0xD40C00, description = "One of your reaction roles went over the Discord limit. It will still work perfectly but only essential data will be displayed in this command to save space.")
                await ctx.reply(embed=limit_embed, delete_after=7)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color = 0xD40C00, description = "**There are no reaction roles in this server.**")
            await ctx.send(embed=embed, delete_after=5)
        await db.close()

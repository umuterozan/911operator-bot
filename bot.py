import discord
import asyncio
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

client = discord.Client(intents = discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [825065007372304414, 822859118469054475]

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="/pager"))
    print("911 Operator BOT başarıyla oturum açtı!")

@slash.slash(
    name="pager",
    description="Seçtiğiniz departmanlara çağrı gönderin",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="departman",
            description="Departman seçimi yapın",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="MEDIC",
                    value="<@&876804556170883133> <@&854440827547156550>"
                ),
                create_choice(
                    name="CORONER",
                    value="<@&867833985191510067>"
                ),
                create_choice(
                    name="POLICE",
                    value="<@&867817539219226695>"
                )
            ]
        ),
        create_option(
            name="olay",
            description="Detaylı şekilde olayı yazın",
            required=True,
            option_type=3
        ),
        create_option(
            name="departman2",
            description="İsteğe bağlı 2. departman seçimi yapın",
            required=False,
            option_type=3,
            choices=[
                create_choice(
                    name="MEDIC",
                    value="<@&876804556170883133> <@&854440827547156550>"
                ),
                create_choice(
                    name="CORONER",
                    value="<@&867833985191510067>"
                ),
                create_choice(
                    name="POLICE",
                    value="<@&867817539219226695>"
                )
            ]
        )
    ]
)
async def _pager(ctx:SlashContext, departman:str, olay:str, departman2:str=""):
    allowed_mentions = discord.AllowedMentions(roles = True)
    message = f"**— PAGER —**\n> **Alıcı:** {departman} {departman2}\n> **Mesaj:** {olay}\n\n**— CEVAPLAYANLAR —**\n"
    response = await ctx.send(content=message, allowed_mentions=allowed_mentions)
    await response.add_reaction("🇨")

    while True:
        try:
            reaction, user = await client.wait_for(
                'reaction_add',
                check = lambda reaction, user: reaction.message.id == response.id,
                timeout = 300.0
            )
            role_CORONER = discord.utils.find(lambda r: r.name == 'CORONER', ctx.message.guild.roles)
            role_MEDIC = discord.utils.find(lambda r: r.name == 'LSMD', ctx.message.guild.roles)
            role_POLICE = discord.utils.find(lambda r: r.name == 'LSPD', ctx.message.guild.roles)

            if role_CORONER in user.roles:
                message += f"🚐 CORONER, çağrı için <@{user.id}> yönlendiriliyor.\n"
                
            elif role_MEDIC in user.roles:
                message += f"🚑 MEDIC, çağrı için <@{user.id}> yönlendiriliyor.\n"
            
            elif role_POLICE in user.roles:
                message += f"🚓 POLICE, çağrı için <@{user.id}> yönlendiriliyor.\n"

            else:
                pass

            await response.edit(content=message)
        
        except asyncio.TimeoutError:
            await response.edit(content=message+"\n⏲️ **5 dakika geçtiği için pager zaman aşımına uğradı.**")
            return


client.run("TOKEN")
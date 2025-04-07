import discord
from discord.ext import commands
from discord.ui import View, Button
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

DONO_ID = 951181188406587442
CARGO_ID = 1358640660055593060
WHATSAPP_NUMERO = "31990813676"
CHAVE_PIX = "breningamingps@gmail.com"
IMAGEM_PRODUTO = "https://media.discordapp.net/attachments/1267586350815772686/1353909935901118474/IMG_9144.png"
MENSAGEM_TICKET = "Envie o comprovante de pagamento aqui para receber seu produto!"

produtos = {
    "1 dia": 20,
    "7 dias": 50,
    "30 dias": 90
}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def painel(ctx):
    embed = discord.Embed(
        title="FFH4x-ios-17-18",
        description="Escolha um plano abaixo para realizar a compra",
        color=0x2ecc71
    )
    embed.set_image(url=IMAGEM_PRODUTO)

    view = View()
    for plano, preco in produtos.items():
        view.add_item(Button(label=f"{plano} - R${preco}", style=discord.ButtonStyle.green, custom_id=plano))

    view.add_item(Button(label="Comprar com saldo", style=discord.ButtonStyle.blurple, custom_id="saldo"))

    await ctx.send(embed=embed, view=view)

@bot.event
async def on_interaction(interaction):
    if interaction.type.name == "component":
        plano = interaction.data['custom_id']
        user = interaction.user

        if plano == "saldo":
            await interaction.response.send_message("Você escolheu comprar com saldo. (Sistema de saldo aqui)", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"Criei um ticket para você enviar o comprovante de pagamento para `{CHAVE_PIX}`.
"
                f"Plano escolhido: **{plano}**
"
                f"O valor é **R${produtos[plano]}**

"
                f"Após o pagamento, envie o comprovante no ticket.",
                ephemeral=True
            )
            guild = interaction.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                user: discord.PermissionOverwrite(read_messages=True)
            }
            canal = await guild.create_text_channel(name=f"ticket-{user.name}", overwrites=overwrites)
            await canal.send(f"{user.mention}
{MENSAGEM_TICKET}")

bot.run(os.getenv("TOKEN"))
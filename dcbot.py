import importlib
import subprocess
import sys
from datetime import datetime

# ----------------------------
# Ellenőrizzük a szükséges könyvtárakat
# ----------------------------
required = ["discord", "colorama"]

def check_dependencies():
    missing = []
    installed = []

    for package in required:
        try:
            importlib.import_module(package)
            installed.append(package)
        except ImportError:
            missing.append(package)

    from colorama import init, Fore
    init(autoreset=True)

    if not missing:
        print(Fore.GREEN + "✅ A program kompatibilis, minden szükséges könyvtár telepítve van.")
        return True
    else:
        print(Fore.RED + "❌ Hiányzó könyvtárak:", missing)
        print(Fore.YELLOW + "Telepített könyvtárak:", installed)
        choice = input("Szeretné, ha a program telepítené a legfrissebbet a hiányzó könyvtárakból? (Y/N): ").strip().lower()
        if choice == "y":
            for package in missing:
                print(Fore.CYAN + f"Telepítés: {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", package])
            print(Fore.GREEN + "✅ Minden hiányzó könyvtár telepítve lett.")
            return True
        else:
            print(Fore.RED + "❌ A hiányzó könyvtárak miatt a program nem fog működni.")
            return False

if not check_dependencies():
    sys.exit(1)

# ----------------------------
# Discord bot importok és beállítások
# ----------------------------
import discord
from discord.ext import commands
from colorama import Fore, init
init(autoreset=True)

# Intents
intents = discord.Intents.default()

# Bot inicializálása
bot = commands.Bot(command_prefix="!", intents=intents)

# Guild ID (Gyorsabb a bot ettől, mivel a szervered a prioritás.)
GUILD_ID = SZERVERED_ID-JE_IDE
GUILD = discord.Object(id=GUILD_ID)

# ----------------------------
# Segédfüggvény logoláshoz
# ----------------------------
def log(msg, color=Fore.WHITE):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(color + f"[{timestamp}] {msg}")

# ----------------------------
# Bot események
# ----------------------------
@bot.event
async def on_ready():
    log(f"Bejelentkezve: {bot.user}", Fore.GREEN)
    try:
        synced = await bot.tree.sync(guild=GUILD)
        log(f"{len(synced)} parancs szinkronizálva a szerveren: {[cmd.name for cmd in synced]}", Fore.CYAN)
    except Exception as e:
        log(f"Hiba a parancsok szinkronizálásánál: {e}", Fore.RED)

@bot.event
async def on_command_error(ctx, error):
    log(f"Hiba a parancs '{ctx.command}' futtatásakor: {error}", Fore.RED)

# ----------------------------
# Slash parancsok
# ----------------------------
@bot.tree.command(name="aktivalas", description="Discord Aktív Fejlesztő jelvény igénylésének lépései", guild=GUILD)
async def aktivalas(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Sikeresen lefuttattad az /aktivalas parancsot!",
        description=(
            "- Lépj fel ide: **https://discord.com/developers/active-developer** és igényeld a jelvényt.\n"
            "- Az ellenőrzés akár 24 órát is igénybe vehet, addig nem claimelheted."
        ),
        color=0x34DB98
    )
    embed.set_footer(text="Készítette: lkr")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    log(f"/aktivalas parancs használva {interaction.user}", Fore.MAGENTA)

@bot.tree.command(name="ping", description="Teszt parancs a bot állapotához", guild=GUILD)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong! A bot aktív.", ephemeral=True)
    log(f"/ping parancs használva {interaction.user}", Fore.MAGENTA)

# ----------------------------
# Bot indítása
# ----------------------------
bot.run("BOT_TOKEN_IDE")

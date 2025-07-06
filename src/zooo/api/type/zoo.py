import json
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

from tcrutils.compare import able
from tcrutils.types import UnixTimestampInt as _UnixTimestampInt

from ._base import _BM, Field, NPCProfileInfo, ProfileID, ProfileInfo, UserInfo, _HexInt, _MEmoji, pd

if True:  # Enums
	from enum import Enum as _Enum
	from enum import IntFlag as _IntFlag
	from enum import StrEnum as _StrEnum

	class AnimalName(_StrEnum):
		OX = "Ox"
		BAT = "Bat"
		CAT = "Cat"
		COW = "Cow"
		DOG = "Dog"
		FLY = "Fly"
		FOX = "Fox"
		PIG = "Pig"
		BEAR = "Bear"
		CRAB = "Crab"
		DOVE = "Dove"
		DUCK = "Duck"
		FISH = "Fish"
		FROG = "Frog"
		SEAL = "Seal"
		WORM = "Worm"
		CAMEL = "Camel"
		CHICK = "Chick"
		HIPPO = "Hippo"
		HORSE = "Horse"
		KOALA = "Koala"
		MOUSE = "Mouse"
		SHEEP = "Sheep"
		SKUNK = "Skunk"
		SLOTH = "Sloth"
		SNAIL = "Snail"
		SQUID = "Squid"
		WHALE = "Whale"
		ZEBRA = "Zebra"
		BEAVER = "Beaver"
		BEETLE = "Beetle"
		LIZARD = "Lizard"
		PARROT = "Parrot"
		RABBIT = "Rabbit"
		SHRIMP = "Shrimp"
		SPIDER = "Spider"
		TURKEY = "Turkey"
		CHICKEN = "Chicken"
		CRICKET = "Cricket"
		GIRAFFE = "Giraffe"
		GORILLA = "Gorilla"
		HAMSTER = "Hamster"
		LEOPARD = "Leopard"
		PENGUIN = "Penguin"
		SNOWMAN = "Snowman"
		ELEPHANT = "Elephant"
		HEDGEHOG = "Hedgehog"
		DINOSAUR = "Dinosaur"
		CROCODILE = "Crocodile"
		CATERPILLAR = "Caterpillar"
		OWL = "Owl"
		RAT = "Rat"
		RAM = "Ram"
		BEE = "Bee"
		GOAT = "Goat"
		SWAN = "Swan"
		WOLF = "Wolf"
		BIRD = "Bird"
		DEER = "Deer"
		LION = "Lion"
		BOAR = "Boar"
		DODO = "Dodo"
		PANDA = "Panda"
		OTTER = "Otter"
		TIGER = "Tiger"
		EAGLE = "Eagle"
		RHINO = "Rhino"
		BISON = "Bison"
		BUNNY = "Bunny"
		T_REX = "T-Rex"
		SHARK = "Shark"
		SNAKE = "Snake"
		LLAMA = "Llama"
		MOOSE = "Moose"
		POODLE = "Poodle"
		TURTLE = "Turtle"
		DRAGON = "Dragon"
		BADGER = "Badger"
		MONKEY = "Monkey"
		DONKEY = "Donkey"
		LADYBUG = "Ladybug"
		ROOSTER = "Rooster"
		LOBSTER = "Lobster"
		MAMMOTH = "Mammoth"
		UNICORN = "Unicorn"
		RACCOON = "Raccoon"
		PEACOCK = "Peacock"
		DOLPHIN = "Dolphin"
		OCTOPUS = "Octopus"
		MOSQUITO = "Mosquito"
		KANGAROO = "Kangaroo"
		CHIPMUNK = "Chipmunk"
		FLAMINGO = "Flamingo"
		SCORPION = "Scorpion"
		BUTTERFLY = "Butterfly"
		COCKROACH = "Cockroach"
		ORANGUTAN = "Orangutan"
		JELLYFISH = "Jellyfish"
		PUFFERFISH = "Pufferfish"
		POLAR_BEAR = "Polar Bear"
		SNOWIER_MAN = "Snowier Man"
		TROPICAL_FISH = "Tropical Fish"
		BACTRIAN_CAMEL = "Bactrian Camel"

	class CosmeticName(_StrEnum):
		MOAI = "Moai"
		TORII = "Torii"
		CROWN = "Crown"
		GRASS = "Grass"
		COZY_BED = "Cozy Bed"
		COSMETIC = "Cosmetic"
		FOX_FIRE = "Fox Fire"
		PAW_BEANS = "Paw Beans"
		BULLS_EYE = "Bull's Eye"
		TAIL_FLUFF = "Tail Fluff"
		TIME_SAVER = "Time Saver"
		MATRYOSHKA = "Matryoshka"
		POLAR_STAR = "Polar Star"
		DISCO_BALL = "Disco Ball"
		TACO_SHELL = "Taco Shell"
		FUNKY_FOXX = "Funky Foxx"
		ANTI_TROPHY = "Anti-Trophy"
		ENDER_PEARL = "Ender Pearl"
		RETRO_ALIEN = "Retro Alien"
		WALL_OF_TEXT = "Wall of Text"
		GAME_BREAKER = "Game Breaker"
		PRAYER_BEADS = "Prayer Beads"
		BATTERY_ACID = "Battery Acid"
		SILVER_FLUFF = "Silver Fluff"
		MAGICAL_MOON = "Magical Moon"
		ROBOTOP_BADGE = "RoboTop Badge"
		HEAVENLY_CLOUD = "Heavenly Cloud"
		TRAVEL_JOURNAL = "Travel Journal"
		CHERRY_BLOSSOM = "Cherry Blossom"
		GOLDEN_FEATHER = "Golden Feather"
		ARTIST_PALETTE = "Artist Palette"
		ZOOKEEPER_MEDAL = "Zookeeper Medal"
		GAME_OBLITERATOR = "Game Obliterator"
		PROGRAMMING_SOCKS = "Programming Socks"
		VISIBLE_CONFUSION = "Visible Confusion"
		NON_FUNCTIONAL_TOKEN = "Non-Functional Token"
		OLD_NAIL = "Old Nail"
		BLINDFOLD = "Blindfold"
		OX_TROPHY = "Ox Trophy"
		TIDAL_WAVE = "Tidal Wave"
		FOX_TROPHY = "Fox Trophy"
		DOG_TROPHY = "Dog Trophy"
		BAT_TROPHY = "Bat Trophy"
		CAT_TROPHY = "Cat Trophy"
		COW_TROPHY = "Cow Trophy"
		FLY_TROPHY = "Fly Trophy"
		PIG_TROPHY = "Pig Trophy"
		ANCIENT_AXE = "Ancient Axe"
		BEAR_TROPHY = "Bear Trophy"
		CRAB_TROPHY = "Crab Trophy"
		DOVE_TROPHY = "Dove Trophy"
		DUCK_TROPHY = "Duck Trophy"
		FISH_TROPHY = "Fish Trophy"
		FROG_TROPHY = "Frog Trophy"
		SEAL_TROPHY = "Seal Trophy"
		WORM_TROPHY = "Worm Trophy"
		KOALA_TROPHY = "Koala Trophy"
		SHEEP_TROPHY = "Sheep Trophy"
		CAMEL_TROPHY = "Camel Trophy"
		CHICK_TROPHY = "Chick Trophy"
		HIPPO_TROPHY = "Hippo Trophy"
		HORSE_TROPHY = "Horse Trophy"
		MOOSE_TROPHY = "Moose Trophy"
		MOUSE_TROPHY = "Mouse Trophy"
		SKUNK_TROPHY = "Skunk Trophy"
		SLOTH_TROPHY = "Sloth Trophy"
		SNAIL_TROPHY = "Snail Trophy"
		SQUID_TROPHY = "Squid Trophy"
		WHALE_TROPHY = "Whale Trophy"
		ZEBRA_TROPHY = "Zebra Trophy"
		KILLER_RABBIT = "Killer Rabbit"
		PARROT_TROPHY = "Parrot Trophy"
		BEAVER_TROPHY = "Beaver Trophy"
		BEETLE_TROPHY = "Beetle Trophy"
		LIZARD_TROPHY = "Lizard Trophy"
		RABBIT_TROPHY = "Rabbit Trophy"
		SHRIMP_TROPHY = "Shrimp Trophy"
		SPIDER_TROPHY = "Spider Trophy"
		TURKEY_TROPHY = "Turkey Trophy"
		HAMSTER_TROPHY = "Hamster Trophy"
		CHICKEN_TROPHY = "Chicken Trophy"
		CRICKET_TROPHY = "Cricket Trophy"
		GIRAFFE_TROPHY = "Giraffe Trophy"
		GORILLA_TROPHY = "Gorilla Trophy"
		LEOPARD_TROPHY = "Leopard Trophy"
		PENGUIN_TROPHY = "Penguin Trophy"
		SNOWMAN_TROPHY = "Snowman Trophy"
		ELEPHANT_TROPHY = "Elephant Trophy"
		HEDGEHOG_TROPHY = "Hedgehog Trophy"
		DINOSAUR_TROPHY = "Dinosaur Trophy"
		CHARM_OF_LEGENDS = "Charm of Legends"
		CROCODILE_TROPHY = "Crocodile Trophy"
		SPECIAL_SNOWFLAKE = "Special Snowflake"
		CATERPILLAR_TROPHY = "Caterpillar Trophy"
		LE_FISHE_AU_CHOCOLAT = "Le Fishe au Chocolat"
		OWL_TROPHY = "Owl Trophy"
		RAM_TROPHY = "Ram Trophy"
		RAT_TROPHY = "Rat Trophy"
		BEE_TROPHY = "Bee Trophy"
		WOLF_TROPHY = "Wolf Trophy"
		GOAT_TROPHY = "Goat Trophy"
		SWAN_TROPHY = "Swan Trophy"
		BIRD_TROPHY = "Bird Trophy"
		DEER_TROPHY = "Deer Trophy"
		LION_TROPHY = "Lion Trophy"
		BOAR_TROPHY = "Boar Trophy"
		DODO_TROPHY = "Dodo Trophy"
		PANDA_TROPHY = "Panda Trophy"
		OTTER_TROPHY = "Otter Trophy"
		TIGER_TROPHY = "Tiger Trophy"
		EAGLE_TROPHY = "Eagle Trophy"
		RHINO_TROPHY = "Rhino Trophy"
		BISON_TROPHY = "Bison Trophy"
		BUNNY_TROPHY = "Bunny Trophy"
		T_REX_TROPHY = "T-Rex Trophy"
		SHARK_TROPHY = "Shark Trophy"
		SNAKE_TROPHY = "Snake Trophy"
		LLAMA_TROPHY = "Llama Trophy"
		DONKEY_TROPHY = "Donkey Trophy"
		DRAGON_TROPHY = "Dragon Trophy"
		POODLE_TROPHY = "Poodle Trophy"
		TURTLE_TROPHY = "Turtle Trophy"
		BADGER_TROPHY = "Badger Trophy"
		MONKEY_TROPHY = "Monkey Trophy"
		RACCOON_TROPHY = "Raccoon Trophy"
		LADYBUG_TROPHY = "Ladybug Trophy"
		ROOSTER_TROPHY = "Rooster Trophy"
		LOBSTER_TROPHY = "Lobster Trophy"
		MAMMOTH_TROPHY = "Mammoth Trophy"
		UNICORN_TROPHY = "Unicorn Trophy"
		PEACOCK_TROPHY = "Peacock Trophy"
		DOLPHIN_TROPHY = "Dolphin Trophy"
		OCTOPUS_TROPHY = "Octopus Trophy"
		CHIPMUNK_TROPHY = "Chipmunk Trophy"
		MOSQUITO_TROPHY = "Mosquito Trophy"
		KANGAROO_TROPHY = "Kangaroo Trophy"
		FLAMINGO_TROPHY = "Flamingo Trophy"
		SCORPION_TROPHY = "Scorpion Trophy"
		BUTTERFLY_TROPHY = "Butterfly Trophy"
		COCKROACH_TROPHY = "Cockroach Trophy"
		ORANGUTAN_TROPHY = "Orangutan Trophy"
		JELLYFISH_TROPHY = "Jellyfish Trophy"
		POLAR_BEAR_TROPHY = "Polar Bear Trophy"
		PUFFERFISH_TROPHY = "Pufferfish Trophy"
		SNOWIER_MAN_TROPHY = "Snowier Man Trophy"
		TROPICAL_FISH_TROPHY = "Tropical Fish Trophy"
		BACTRIAN_CAMEL_TROPHY = "Bactrian Camel Trophy"
		YETI_TROPHY = "Yeti Trophy"
		MANTIS_TROPHY = "Mantis Trophy"
		KRAKEN_TROPHY = "Kraken Trophy"
		WYVERN_TROPHY = "Wyvern Trophy"
		KITSUNE_TROPHY = "Kitsune Trophy"
		PEGASUS_TROPHY = "Pegasus Trophy"
		MERMAID_TROPHY = "Mermaid Trophy"
		GRYPHON_TROPHY = "Gryphon Trophy"
		BASILISK_TROPHY = "Basilisk Trophy"
		MINOTAUR_TROPHY = "Minotaur Trophy"

	class GoalName(_StrEnum):
		TRADER = "Trader"
		DEALER = "Dealer"
		BROKER = "Broker"
		VESSEL = "Vessel"
		RESCUER = "Rescuer"
		CURATOR = "Curator"
		ARTISAN = "Artisan"
		PRODIGY = "Prodigy"
		DEVOTEE = "Devotee"
		HUSTLER = "Hustler"
		EXPLORER = "Explorer"
		ASCENDER = "Ascender"
		RECYCLER = "Recycler"
		ZOOKEEPER = "Zookeeper"
		COMMANDER = "Commander"
		COLLECTOR = "Collector"
		INNOVATOR = "Innovator"
		ADVENTURER = "Adventurer"
		CAPITALIST = "Capitalist"
		MULTITASKER = "Multitasker"
		INTELLECTUAL = "Intellectual"
		REHABILITATOR = "Rehabilitator"
		AGRICULTURIST = "Agriculturist"
		ARCHAEOLOGIST = "Archaeologist"
		ADMINISTRATOR = "Administrator"
		SUPER_EXPLORER = "Super Explorer"
		PSEUDO_EXPLORER = "Pseudo Explorer"

	class ItemName(_StrEnum):
		ACE = "Ace"
		EGG = "Egg"
		BALL = "Ball"
		BONE = "Bone"
		CAKE = "Cake"
		CORN = "Corn"
		LURE = "Lure"
		WAND = "Wand"
		BROOM = "Broom"
		JOKER = "Joker"
		NAZAR = "Nazar"
		SCARF = "Scarf"
		SUSHI = "Sushi"
		PIZZA = "Pizza"
		LOTUS = "Lotus"
		CANOE = "Canoe"
		FLUTE = "Flute"
		SCALE = "Scale"
		COUPON = "Coupon"
		BAMBOO = "Bamboo"
		COFFEE = "Coffee"
		COOKIE = "Cookie"
		CHAINS = "Chains"
		NEEDLE = "Needle"
		COMPASS = "Compass"
		FEATHER = "Feather"
		GLASSES = "Glasses"
		PRESENT = "Present"
		BATTERY = "Battery"
		PUSHPIN = "Pushpin"
		PEBBLES = "Pebbles"
		GOGGLES = "Goggles"
		CALENDAR = "Calendar"
		CONTRACT = "Contract"
		SAILBOAT = "Sailboat"
		BACKPACK = "Backpack"
		COCKTAIL = "Cocktail"
		LOOT_BOX = "Loot Box"
		OMELETTE = "Omelette"
		ETHEREUM = "Ethereum"
		MEGAPHONE = "Megaphone"
		RICE_BALL = "Rice Ball"
		STOPWATCH = "Stopwatch"
		WILD_CARD = "Wild Card"
		AETHERIUM = "Aetherium"
		PINEAPPLE = "Pineapple"
		FOIL_CARD = "Foil Card"
		TELESCOPE = "Telescope"
		SCRAP_BIN = "Scrap Bin"
		GREEN_TEA = "Green Tea"
		EIGHT_BALL = "8 Ball"
		CHAIN_LINK = "Chain Link"
		PAINTBRUSH = "Paintbrush"
		SAFETY_PIN = "Safety Pin"
		SHINY_COIN = "Shiny Coin"
		SPIDER_WEB = "Spider Web"
		SUNGLASSES = "Sunglasses"
		BLANK_CARD = "Blank Card"
		CAKE_SLICE = "Cake Slice"
		EYEDROPPER = "Eyedropper"
		ZOO_TOKEN_TM = "Zoo Token™"
		ALARM_CLOCK = "Alarm Clock"
		FIXED_CLOCK = "Fixed Clock"
		SCREWDRIVER = "Screwdriver"
		GREEN_ONION = "Green Onion"
		BROKEN_CLOCK = "Broken Clock"
		CRYSTAL_BALL = "Crystal Ball"
		ENERGY_DRINK = "Energy Drink"
		MIRACLE_HERB = "Miracle Herb"
		MYSTERY_MEAT = "Mystery Meat"
		SPROUT_SCOPE = "Sprout Scope"
		MAGIC_MIRROR = "Magic Mirror"
		RICE_CRACKER = "Rice Cracker"
		MIRACLE_SEED = "Miracle Seed"
		CARD_PYRAMID = "Card Pyramid"
		HIKING_BOOTS = "Hiking Boots"
		CARDBOARD_BOX = "Cardboard Box"
		UNSTABLE_WAND = "Unstable Wand"
		ANIMAL_SPIRIT = "Animal Spirit"
		FORTUNE_COOKIE = "Fortune Cookie"
		BROWSER_COOKIE = "Browser Cookie"
		BOOSTER_COOKIE = "Booster Cookie"
		BLUE_CHECKMARK = "Blue Checkmark"
		BASE_MYSTERY_EGG = "Base Mystery Egg"
		INVERTED_PYRAMID = "Inverted Pyramid"
		BLANK_MYSTERY_EGG = "Blank Mystery Egg"
		GOLDEN_MYSTERY_EGG = "Golden Mystery Egg"

	class LeaderName(_StrEnum):
		YETI = "Yeti"
		MANTIS = "Mantis"
		KRAKEN = "Kraken"
		WYVERN = "Wyvern"
		KITSUNE = "Kitsune"
		PEGASUS = "Pegasus"
		MERMAID = "Mermaid"
		GRYPHON = "Gryphon"
		BASILISK = "Basilisk"
		MINOTAUR = "Minotaur"

	class QuestName(_StrEnum):
		LONG = "Long Quest"
		SHORT = "Short Quest"
		RISKY = "Risky Quest"
		MEDIUM = "Medium Quest"
		ANCIENT = "Ancient Quest"
		PEACEFUL = "Peaceful Quest"
		PERILOUS = "Perilous Quest"
		LEGENDARY = "Legendary Quest"

	class RelicName(_StrEnum):
		SACK = "Sack"
		CANDLE = "Candle"
		API_KEY = "API Key"
		LANTERN = "Lantern"
		NECKLACE = "Necklace"
		SATELLITE = "Satellite"
		JUICE_BOX = "Juice Box"
		HOURGLASS = "Hourglass"
		FLASHLIGHT = "Flashlight"
		MOVING_BOX = "Moving Box"
		FRYING_PAN = "Frying Pan"
		BUBBLE_TEA = "Bubble Tea"
		FIRECRACKER = "Firecracker"
		TWIN_CHERRY = "Twin Cherry"
		CURSED_DICE = "Cursed Dice"
		MECHANIC_CAP = "Mechanic Cap"
		SHOPPING_CART = "Shopping Cart"
		DECEARING_EGG = "Decearing Egg"
		CHECKERED_FLAG = "Checkered Flag"
		VIRTUAL_MACHINE = "Virtual Machine"
		MAGNIFYING_GLASS = "Magnifying Glass"
		MAGICAL_SEEDLING = "Magical Seedling"

	class ThemeID(_StrEnum):
		DUO = "duo"
		NEON = "neon"
		SHINY = "shiny"
		COSMIC = "cosmic"
		DREAMY = "dreamy"
		SAKURA = "sakura"
		SUNKEN = "sunken"
		SUNSET = "sunset"
		MURPHY = "murphy"
		DOCTAH = "doctah"
		ANALOG = "analog"
		POLARIS = "polaris"
		FOX_BOY = "colon"
		ROBOTOP = "robotop"
		MIDNIGHT = "midnight"
		INVERTED = "inverted"
		BLISSFUL = "blissful"
		GENRETRO = "genretro"
		BAREBONES = "barebones"
		BASIC_DARK = "none"
		POWERSHELL = "powershell"
		UNDERCOVER = "undercover"
		BASIC_LIGHT = "light"
		SQUARE_GAME = "gd"
		HOT_DOG_STAND = "hotdog"

	class ThemeName(_StrEnum):
		DUO = "Duo"
		NEON = "Neon"
		SHINY = "Shiny"
		COSMIC = "Cosmic"
		DREAMY = "Dreamy"
		SAKURA = "Sakura"
		SUNKEN = "Sunken"
		SUNSET = "Sunset"
		MURPHY = "Murphy"
		DOCTAH = "Doctah"
		ANALOG = "Analog"
		POLARIS = "Polaris"
		FOX_BOY = "Fox Boy"
		ROBOTOP = "RoboTop"
		MIDNIGHT = "Midnight"
		INVERTED = "Inverted"
		BLISSFUL = "Blissful"
		GENRETRO = "So Retro"
		BAREBONES = "Barebones"
		BASIC_DARK = "Basic Dark"
		POWERSHELL = "Powershell"
		UNDERCOVER = "Undercover"
		BASIC_LIGHT = "Basic Light"
		SQUARE_GAME = "Square Game"
		HOT_DOG_STAND = "Hot Dog Stand"

	class ThemeCategory(_IntFlag):
		NONE = 0
		BASIC = 1 << 0
		JOKE = 1 << 1
		EMPTY = 1 << 2

	class PinType(_Enum):
		RED = "red"
		BLUE = "blue"
		GREEN = "green"
		PURPLE = "purple"
		HEART = "heart"
		STAR = "star"

	class AchievementName(_StrEnum):
		BURDENED = "Burdened"
		BASS_PRO = "Bass Pro"
		TUNED_UP = "Tuned Up"
		COSMIC_DOLPHIN = "Cosmic Dolphin"
		LOYAL_CUSTOMER = "Loyal Customer"
		FULLY_AUTOMATIC = "Fully Automatic"
		TRINKET_COLLECTOR = "Trinket Collector"
		PROFESSIONAL_PAINTER = "Professional Painter"

	class AchievementGroup(_Enum):
		"""The reveal (?) group of an achievement."""

		UNGROUPED = "ungrouped"
		"""Given to all achievements which dont provide a "group" key in their API response's object."""
		EARLY = "early"
		LEADER = "leader"
		EARLY_PLUS = "early+"
		TERMINAL = "terminal"
		TERMINAL_PLUS = "terminal+"


if True:  # Functionality classes

	class _ZooObtainable(_BM):
		"""Represents obtainable object in Zoo, not used standalone, only subclassed."""

		obtained: bool = True
		"""Whether or not this item has been obtained in this profile, if False it means it has been derived either due to direct request or parsing (that is: This profile does not have this item/animal/cosmetic/etc. and if possible, it's amount is 0, if there's no 'amount' field you have to rely on this field)."""


if True:  # Zoo

	class ZooUser(_BM):
		"""Basic information about the user of this profile."""

		avatar_url: str = Field(alias="avatar")
		"""Avatar URL of this user."""
		npc: bool = False
		"""Whether this profile is an NPC profile. (roboturt, )"""

	class ZooUniqueAnimals(_BM):
		"""Unique common, rare or all animals in this profile."""

		common: int
		"""Unique common animals in this profile."""
		rare: int
		"""Unique rare animals in this profile."""
		total: int
		"""Total unique animals in this profile."""

	class ZooTotalAnimals(_BM):
		"""Common or rare total (non-unique) animals in this profile."""

		common: int
		"""Common animals in this profile."""
		rare: int
		"""Rare animals in this profile."""

	class ZooAnimal(_ZooObtainable, _MEmoji):
		"""Represents a single animal in a zoo profile."""

		name: AnimalName
		"""Name of this animal."""
		amount: int = 0
		"""Amount of this animal."""
		emoji: str
		"""Emoji of this animal."""
		emoji_name: str
		"""Name of the emoji of this animal."""
		family: str
		"""In the api it's saved under `'family'`.

		This means:
		- if rare, the `emoji_name` of the common variant
		- if common, equal to the `emoji_name`
		"""
		rare: bool
		"""Whether or not this animal is rare."""
		pinned: None | PinType = None
		"""Type of pin, if any."""

	class ZooItem(_ZooObtainable, _MEmoji):
		"""Represents an item in a zoo profile."""

		name: ItemName
		"""Name of the item."""
		amount: int | float = 0
		"""Amount of this item. Rarely may be float (example: Ethereum item)."""
		emoji: str
		"""Emoji of the item."""
		highlight: bool
		"""Whether or not this item is highlighted in the items list."""
		description: str | None = None
		"""Description of this item.

		May be None if not authorised with a cookie (`.owner`).
		"""
		times_used: int = 0
		"""How many times has this item been used on this profile."""
		not_counted: bool = False
		"""Whether this item is not counted towards the item totals (Example: Pebbles, Zoo Tokens™)."""
		unlisted: bool = False
		"""TODO: what does this do? note to myself: seems to be set on most but not all not_counted items..."""

	class ZooRelic(_ZooObtainable, _MEmoji):
		"""Represents a relic in a zoo profile."""

		name: RelicName
		"""Name of this relic."""
		emoji: str
		"""Emoji of this relic."""
		description: str | None
		"""Description of this relic.

		May be None if not authorised with a cookie (`.owner`).
		"""
		special: bool
		"""Whether or not this relic is tagged as 'special' (is displayed with empahsis on the website)."""

	class ZooCosmetic(_ZooObtainable, _MEmoji):
		"""Represents a cosmetic in a zoo profile."""

		name: CosmeticName
		"""Name of this cosmetic."""
		emoji: str
		"""Emoji of this cosmetic."""
		trophy: int = 0
		"""Whether or not this cosmetic is a trophy.

		- `0`: Not a trophy
		- `1`: Common trophy
		- `2`: Rare trophy
		- `3`: Leader trophy
		"""
		description: str | None = None  # Huh??? why are all the other descriptions None when not provided and this is just missing
		"""Description of this cosmetic.

		May be None if not authorised with a cookie (`.owner`).
		"""
		has_effect: bool
		"""Whether or not this cosmetic is of the effect type (multiple can be equipped if enough slots type) or emoji type (one can be equipped type)."""
		leader_charm: bool = False
		"""Whether or not this cosmetic is tagged as a leader charm cosmetic."""

	class ZooLeader(_ZooObtainable, _MEmoji):
		"""Represents a leader in a zoo profile."""

		name: LeaderName
		"""Name of this leader."""
		emoji: str
		"""Emoji of this leader."""
		triggered: int = 0
		"""How many times has this leader been triggered on this profile."""
		xp: int = 0
		"""XP of this leader."""
		level: int = 0
		"""Level of this leader."""

	class ZooListedQuest(_ZooObtainable, _MEmoji):
		"""Represents one of the discovered by the user quests in a zoo profile. Not to be confused with `Zoo.quest` which is a the ongoing quest in that profile."""

		name: QuestName
		"""Name of this quest."""
		type: str
		"""Type of this quest."""
		emoji: str
		"""Emoji of this quest."""
		days: int
		"""Days it takes to complete this quest."""
		completed: int | None = None
		"""How many times this quest has been completed on this profile (None if not obtained.)."""

	class ZooGoal(_ZooObtainable, _MEmoji):
		"""Represents a goal in a zoo profile."""

		def __init__(self, **data):
			if "description" in data:
				data["desc"] = data.pop("description")
			super().__init__(**data)

		name: GoalName
		"""Name of this goal."""
		emoji: str
		"""Emoji of this goal."""
		tier: str | None = None
		"""Roman numeral for the tier number of this goal."""
		tier_number: int = 0
		"""Tier number of this goal."""
		target: int | None = None
		"""Target amount of (`self.units`) to ascend to the next tier of this goal."""
		description: str | None = Field(alias="desc", default=None)  # For consistency with other attributes
		"""Description of this goal's activity in imperative mood with the target number already preset.

		Example: 'Offer 7 items'
		"""
		count: int = 0
		"""The amount of (`self.units`) already done by the player in this goal.

		NOTE: This may be higher than the target amount if the player already completed the activity on the highest tier (`.complete is True`).
		"""
		complete: bool = False
		"""Whether or not this user already completed the target activity on the highest tier."""
		unit: str
		"""The unit of how many `self.target`s one needs to complete for a given tier"""

	class ZooCurrentQuest(_BM):
		"""Represents the ongoing quest in a zoo profile. Not to be confused with `Zoo.quests` which is a list of the discovered by the user quests in that profile."""

		type: str
		"""Type of this quest."""
		animal: str
		"""The rare animal that is assigned to this quest."""
		family: str
		"""The family of the rare animal that is assigned to this quest.

		Family is the `emoji_name` of the common variant of this rare animal.
		"""

	class ZooCurseNames(_BM):
		"""Names of this curse's `type` and `cure` as separate strings."""

		type: str
		"""Name of this curse's type."""
		cure: str
		"""Name of this curse's cure."""

	class ZooCurseEffectsType(_BM):
		"""Effects & name of this curse's type."""

		name: str
		"""Name of this curse's type."""
		description: str
		"""Description of this curse's type's effects."""
		weak: str | None
		"""Description of the extra effects of this curse's type's weakness. May be None if the curse is not weakened."""

	class ZooCurseEffectsCure(_BM):
		"""Effects & name of this curse's cure."""

		name: str
		"""Name of this curse's cure."""
		description: str
		"""Description of this curse's cure's effects."""
		weak: str | None
		"""Description of the extra effects of this curse's cure's weakness. May be None if the curse is not weakened."""

	class ZooCurseEffects(_BM):
		"""Effects of this curse's `type` and `cure`."""

		type: ZooCurseEffectsType
		"""Effects of this curse's type."""
		cure: ZooCurseEffectsCure
		"""Effects of this curse's cure."""

	class ZooCurse(_BM):
		"""Represents an active curse on this profile."""

		name: str
		"""Full displayname of this curse, example: `'Shackled Curse of Disobedience'`."""
		names: ZooCurseNames
		"""Names of this curse `type` and `cure` as separate strings."""
		weak: bool
		"""Whether or not this curse has been weakened."""
		effects: ZooCurseEffects
		"""Effects of this curse's `type` and `cure`."""

	class ZooTerminalFishy(_BM):
		"""Info about the `$ fishy` minigame of this profile."""

		common: int = Field(alias="commonFish")
		"""Number of common fish."""
		uncommon: int = Field(alias="uncommonFish")
		"""Number of uncommon fish."""
		rare: int = Field(alias="rareFish")
		"""Number of rare fish."""
		trash: int
		"""Number of trash."""
		pebbles: int
		"""Number of pebbles."""

	class ZooTerminalGarden(_BM):
		"""Info about the `$ garden` of this profile."""

		unlocked: bool
		"""Whether or not the garden is unlocked in this profile."""

	class ZooTerminalCards(_BM):
		"""Info about the cards of this profile."""

		total: int
		"""Total number of cards."""
		common: int = Field(alias="c", default=0)
		"""Number of common cards."""
		rare: int = Field(alias="r", default=0)
		"""Number of rare cards."""
		ultra_rare: int = Field(alias="l", default=0)
		"""Number of ultra rare (leader) cards."""
		discontinued: int = Field(alias="d", default=0)
		"""Number of discontinued cards (e.g. Snowman)."""
		special: int = Field(alias="s", default=0)
		"""Number of special cards (e.g. Murphy)"""

		@pd.model_validator(mode="before")
		@classmethod
		def _flatten_rarities(cls, values):
			"""Extract 'rarities' and merge its contents into the main dictionary.

			## BEFORE

			```
			{"total": 1234, "rarities": {
				"c": 1000,
				"r": 234,
			}}
			```

			## AFTER

			```
			{"total": 1234, "c": 1000, "r" 234}
			```
			"""
			rarities = values.pop("rarities", {})
			if isinstance(rarities, dict):
				values.update(rarities)
			return values

	class ZooTerminalFusionFusions(_BM):
		"""Info about the fusions of this profile."""

		common_common: int
		"""Number of common + common fusions in this profile."""
		common_rare: int
		"""Number of common + rare (or rare + common) fusions in this profile."""
		rare_rare: int
		"""Number of rare + rare fusions in this profile."""
		total: int
		"""Total number of fusions in this profile."""
		score: int
		"""Total zoo score of fusions in this profile."""

	class ZooTerminalFusionNFBs(_BM):
		"""Info about the NFBs of this profile."""

		common: int
		"""Number of common NFBs in this profile."""
		rare: int
		"""Number of rare NFBs in this profile."""
		total: int
		"""Total number of NFBs in this profile."""
		score: int
		"""Total zoo score of NFBs in this profile."""

	class ZooTerminalFusion(_BM):
		tokens_per_rescue: int
		"""Zoo Tokens™ per rescue of this profile (already multiplied by the nfb_multiplier)."""
		tokens_from_fusions: int
		"""Zoo Tokens™ per rescue of this profile not counting the nfb_multiplier."""
		nfb_multiplier: float
		"""Zoo Tokens™ per rescue multiplier by NFBs in this profile. Units: %, example: `23.5` = `+23.5%` or `+0.235*x` or `*1.235`."""
		fusions: ZooTerminalFusionFusions
		"""Info about the fusions of this profile."""
		nfbs: ZooTerminalFusionNFBs
		"""Info about the NFBs of this profile."""

	class ZooTerminal(_BM):
		"""Represents the terminal-related data of this profile."""

		unlocked: bool = False
		"""Whether or not this profile has the terminal unlocked."""
		admin: bool = False
		"""Whether or not this profile unlocked the terminal administrator access via the `$ adminunlock` command."""
		commands_found: int = 0
		"""Amount of findable commands found in this profile."""
		mechanic_points: int = 0
		"""Amount of murphy points this profile contains."""
		fishy: ZooTerminalFishy | None = None
		"""Info about the `$ fishy` minigame of this profile."""
		garden: ZooTerminalGarden | None = None
		"""Info about the `$ garden` of this profile."""
		cards: ZooTerminalCards | None = None
		"""Info about the cards of this profile."""
		fusion: ZooTerminalFusion | None = None
		"""Info about the fusions & NFBs of this profile."""

	class ZooStat(_BM):
		"""Represents a stat in an NPC profile."""

		name: str
		"""Name of the stat."""
		amount: int
		"""Amount of that stat."""

	class ZooSettings(_BM):
		"""The user-selected `/settings` of this profile."""

		alt_timestamp: bool
		""""Timestamp Type"

		How the timestamp for upcoming rescues should be formatted

		- `True`: x hours x minutes
		- `False`: hh:mm:ss
		"""

		show_animal_totals: bool
		""""Show Animal Totals"

		When rescuing an animal, also show the total of it that you have

		- `True`: Yes, show totals on rescue
		- `False`: No, don't show totals on rescue
		"""
		fast_confirmations: bool
		"""(inverse of) "Extra Confirmations"

		(inverse of) Require an extra button press before confirming important actions (e.g. using an item or equipping something)

		- `True`: No extra confirmation
		- `False`: Extra confirmations
		"""
		disable_notifications: bool
		"""(inverse of) "Consume Rescue Notifications"

		(inverse of) If rescue notifications should be used and consumed

		- `True`: Don't consume rescue notifications
		- `False`: Consume rescue notifications
		"""
		disable_auto_rescues: bool
		"""(inverse of) "Consume Auto-Rescues"

		(inverse of) If auto-rescues should be used and consumed

		- `True`: Don't consume auto-rescues
		- `False`: Consume auto-rescues
		"""
		disable_quest_notifications: bool
		"""(inverse of) "Quest Notifications"

		(inverse of) If the bot should DM you when a quest finishes

		- `True`: Don't send quest notification DMs
		- `False`: Send quest notification DMs
		"""
		disable_custom_color: bool
		"""(inverse of) "Custom Embed Color"

		(inverse of) Enables custom embed colors set by certain items

		- `True`: Don't use custom embed colors
		- `False`: Use custom embed colors
		"""
		hide_cosmetics: bool
		"""(inverse of) "Public Cosmetics" (This is a web-version-only setting at the time of writing this sentence)

		If enabled, only the profile owner can view your cosmetics on the web page (if they are logged in).

		- `True`: Don't show cosmetics to everyone
		- `False`: Show cosmetics to everyone
		"""

		disable_rescue_quotes: bool
		"""(inverse of) "Rescue Quotes".

		If enabled, there will be no rescue quotes on this profile's rescues.

		- `True`: Don't show rescue quotes
		- `False`: Show rescue quotes
		"""

		disable_unstarted_quest_reminder: bool
		"""(inverse of) "Unstarted Quest Reminder".

		If enabled, there will be no reminder about unstarted quests on rescue.

		- `True`: Don't show unstarted quest reminder
		- `False`: Show unstarted quest reminder
		"""

	class ZooUnlockedThemeAchievementReveal(_BM):
		"""Required stat to reveal this achievement."""

		name: str
		"""Name of the action required to reveal this achievement."""
		property: str | None
		"""Presumably the internal property name of the value required to reveal this achievement."""
		value: int | None
		"""The required value to reveal this achievement"""
		special: bool
		"""I have zero idea what this bool does. It is unnamed (appears in an `[json array]` along with other stuff), i added a name 'special' in this python API wrapper."""

	class ZooUnlockedThemeAchievement(_BM):
		"""An achievement tied to an unlocked theme."""

		name: AchievementName
		"""The name of this achievement"""
		group: AchievementGroup = AchievementGroup.UNGROUPED
		"""The reveal (?) group of this achievement"""
		reveal: ZooUnlockedThemeAchievementReveal | None = None

		obtaining_description: str | None = Field(default=None, alias="desc")
		"""(presumably) Either `.obtaining_description` (this) or `.obtained_description` is present on the API returned object."""
		obtained_description: str | None = Field(default=None, alias="obtainedDesc")
		"""(presumably) Either `.obtaining_description` or `.obtained_description` (this) is present on the API returned object."""

		@pd.model_validator(mode="before")
		@classmethod
		def _combine_stat_reveal(cls, values: dict[str, Any]):
			"""Combine the keys 'stat' and 'reveal' into a single struct, returned as key 'reveal'."""
			if "stat" not in values and "reveal" not in values:
				return values

			if "stat" not in values or "reveal" not in values:
				raise ValueError(f'either both or none of keys "stat" and "reveal" must be in ZooUnlockedThemeAchievement(**data), got: {values}')

			stat: list = values.pop("stat")
			reveal: list = values.pop("reveal")

			if not isinstance(stat, list) or not isinstance(reveal, list) or len(stat) != len(reveal):
				raise ValueError(f'keys "stat" and "reveal" must be lists and the same length, otherwise fix combine_stat_reveal model validator, got: {values}')

			if not stat or not reveal:
				raise ValueError(f'neither of "stat" and "reveal" can be an empty list, got: {values}')

			if stat[0] != reveal[0]:
				raise ValueError(f'keys "stat" and "reveal" must have the same first element, otherwise fix combine_stat_reveal model validator, got: {values}')

			name: str = stat[0]

			if not isinstance(name, str):
				raise TypeError(f"stat[0] (same as reveal[0]) must be a string, got: {values}")

			if len(stat) == 3:
				if stat[2] != reveal[2]:
					raise ValueError(f'keys "stat" and "reveal" must not be 3-element OR have the same third element, otherwise fix combine_stat_reveal model validator, got: {values}')

			values["reveal"] = {
				"name": name,
				"property": stat[1] if len(stat) > 1 else None,
				"value": reveal[1] if len(reveal) > 1 else None,
				"special": stat[2] if len(stat) > 2 else False,
			}

			return values

	class ZooUnlockedTheme(_BM, _MEmoji):
		"""Represents one of the unlocked themes in a zoo profile (Not to be confused with the `Zoo.theme` which represents the currently selected theme)."""

		def __init__(self, **data):
			if "unlockedBy" in data:
				data["unlockDesc"] = data.pop("unlockedBy")

			super().__init__(**data)

		name: ThemeName
		"""Name of this theme."""
		id: ThemeID
		"""Internal ID of this theme."""
		category: ThemeCategory = ThemeCategory.NONE
		"""The category(ies) this theme belongs to. (eg. 'basic', 'joke', 'empty'). A theme may be a part of one, multiple or zero (ThemeCategory.NONE) categories at a time."""
		emoji: str
		"""Emoji of this theme."""
		color: _HexInt
		"""Hex color of this theme."""
		no_cache: bool = False
		"""(presumably) Don't cache the result on reload on the webpage, kinda like the Duo theme changes color based on your profile color...?"""
		unlocked_by: str = Field(alias="unlockDesc")
		"""Unlock description of this theme.

		Example: 'earning 2,500 Murphy Points'
		"""
		achievement: ZooUnlockedThemeAchievement | None = None
		"""The /goals -> achievement tied to this theme, if any."""

		@pd.field_validator("color", mode="before")
		@classmethod
		def _v_color(cls, v):
			if v is None:
				return None
			return _HexInt(str(v).removeprefix("#"), base=16)

		@pd.model_validator(mode="before")
		@classmethod
		def _combine_categories(cls, values):
			values["category"] = ThemeCategory.NONE

			for k, v in {
				"basic": ThemeCategory.BASIC,
				"empty": ThemeCategory.EMPTY,
				"joke": ThemeCategory.JOKE,
			}.items():
				if k in values:
					values["category"] |= v
					del values[k]

			return values

	class ZooSecretInfoPromises(_BM):
		"""Represents promises given to this profile by Zoo.

		TODO: Maybe there are more fields here, i cant think of any atm.
		NOTE: to the above todo ^^^ the backpack item effect seems to be a promise as well.
		"""

		type: str | None = None
		"""If not None, this animal type is promised to be found on the next rescue. (Known Sources: Items like: Sushi, Crystal Ball)"""
		pair: bool = False
		"""If True, a pair is promised to be found on the next rescue. (Known Sources: Glasses, Sunglasses)"""
		animal: str | None = None
		"""If not None, this animal ('s emoji name i believe) is promised to be found on the next rescue. (Known Sources: Ace)"""
		lucky_relics: bool = False
		"""If True, "Guarantees the best outcome for all luck-based effects on your next rescue.", despite it being named "lucky *relics*" it applies to other things too. (known Sources: Backpack)"""
		extra_promises: int = 0
		"""If this is `>=1`, instead of reseting promises, keep them and decrement this number instead. (Known Sources: Goggles)"""

	class ZooSecretInfoQuestBoosts(_BM):
		"""Represents quest promises given to this profile by Zoo.

		TODO: Maybe there are more fields here, i cant think of any atm.

		NOTE: This seems to NOT contain:
		- Quest offering effects
		- Leader XP upgrade effects

		I've only ever seen this contain the telescope item effects.
		"""

		extra_rewards: int = 0
		"""By how much increase the quality of the rewards.

		Old version: ~~How many extra rewards (animals, items, curse days) are added to the default amount.~~

		Reason: Telescope item was used.
		"""
		length: int = 0
		"""By how much *increase* the length of the quest.

		Reason: Telescope item was used.
		"""
		rare_curse: bool = False
		"""Whether or not the curse chance weight is divided by 4.

		Reason: Safety Pin item was used.
		"""
		high_roll: bool = False
		"""Whether or not the quest rewards will be in top 25% of the given range.

		Reason: Pushpin item was used.
		"""
		no_relic: bool = False
		"""Whether or not the relic chance is set to 0.

		Reason: Pushpin item was used.
		"""

	class ZooSecretInfoShop(_BM):
		"""Represents secret info related to the shop in this profile."""

		credits: int
		"""The current amount of shop credits in this profile."""
		max_credits: int
		"""The maximum amount of shop credits this profile can have."""
		next_credit: _UnixTimestampInt | None
		"""[UNIX] When the next credit will be given to this profile."""
		last_purchase: _UnixTimestampInt | None
		"""[UNIX] When the last purchase was made by this profile."""

		@pd.field_validator("next_credit", mode="before")
		@classmethod
		def _v_next_credit(cls, v):
			if v is None:
				return None
			return _UnixTimestampInt(v)

		@pd.field_validator("last_purchase", mode="before")
		@classmethod
		def _v_last_purchase(cls, v):
			if v is None:
				return None
			return _UnixTimestampInt(v)

	class ZooSecretInfoCooldowns(_BM):
		"""Represents the cooldowns as part of the secret info."""

		rescue: _UnixTimestampInt | None = None
		"""[UNIX] When the next rescue is available."""
		relic: _UnixTimestampInt | None = None
		"""[UNIX] When the next relic switch is available."""
		leader: _UnixTimestampInt | None = None
		"""[UNIX] When the next leader switch is available."""
		profile: _UnixTimestampInt | None = None
		"""[UNIX] When the next profile switch is available."""
		card_pull: _UnixTimestampInt | None = None
		"""[UNIX] When the next card pull is available."""
		pet: _UnixTimestampInt | None = None
		"""[UNIX] When the next `$ pet` is available."""
		fishy: _UnixTimestampInt | None = None
		"""[UNIX] When the next `$ fishy` is available."""
		sisyphus: _UnixTimestampInt | None = None
		"""[UNIX] When the next `$ sisyphus` is available.

	NOTE: This is `None` if user either:
	- has not used `$ sisyphus` yet
	- Or the last time they used `$ sisyphus` the boulder fell down
	The latter  Q is probably a way to make the inner workings of this silly thing simpler but feels like a bug.
	"""

		@pd.field_validator("*", mode="before")
		@classmethod
		def _v_rescue(cls, v):
			if v is None:
				return None
			return _UnixTimestampInt(v)

	class ZooSecretInfoTerminal(_BM):
		"""Represents secret info related to the terminal in this profile."""

		directory: str
		"""The current terminal directory, for example `'/var/scams'`."""
		commands: list[str]
		"""A list of all "collectable" (by that i mean they show up here and in `$help` i guess) terminal commands that were found on this profile."""
		next_fusion: int = 0
		"""Number of rescues until the next fusion can be made."""

		@pd.field_validator("directory", mode="before")
		@classmethod
		def _v_directory(cls, v):
			if v is None:
				return "/root/Zoo/terminal"

			return v

	class ZooSecretInfoGarden(_BM):
		"""Represents secret info related to the garden in this profile."""

		next_plant: _UnixTimestampInt | None
		"""[UNIX] When that player may plant a new seedling."""
		watered: bool
		"""Whether or not the player already used up their watering ability this rescue."""
		longest_plant: int
		"""Miliseconds since that plant matured."""
		sprinkler: int = 0
		"""Current sprinkler slot, 0 if not in use."""

		@pd.field_validator("next_plant", mode="before")
		@classmethod
		def _v_next_plant(cls, v):
			if v is None:
				return None
			return _UnixTimestampInt(v)

	class ZooSecretInfo(_BM):
		"""[API KEY] Represents secret info related to this profile."""

		sort: int
		"""User's preferred sorting method, in who knows which menu (needs testing)."""
		color: _HexInt | None
		"""Is that literally just Zoo.color but int and not str(hex(this))??"""
		promises: ZooSecretInfoPromises = Field(alias="promise")
		"""Represents promises given to this profile by Zoo."""
		quest_end: _UnixTimestampInt | None
		"""[UNIX] If this profile has a quest in progress, this is the unix timestamp when it will be complete."""
		quest_boosts: ZooSecretInfoQuestBoosts
		"""Represents quest promises given to this profile by Zoo."""
		curse_end: _UnixTimestampInt | None
		"""[UNIX] If this profile has a curse, this is the unix timestamp when it will naturally expire."""
		mechanic_end: _UnixTimestampInt | None
		"""[UNIX] If this profile has a mechanic upgrade in progress, this is the unix timestamp when it will be complete."""
		shop: ZooSecretInfoShop
		"""Represents secret info related to the shop in this profile."""
		cooldowns: ZooSecretInfoCooldowns
		"""Represents the cooldowns as part of the secret info."""
		terminal: ZooSecretInfoTerminal
		"""Represents secret info related to the terminal in this profile"""
		garden: ZooSecretInfoGarden | None = None
		"""Represents secret info related to the garden in this profile."""

		@pd.field_validator("color", mode="before")
		@classmethod
		def _v_color(cls, v):
			if v is None:
				return None
			return _HexInt(v)

		@pd.field_validator("quest_end", mode="before")
		@classmethod
		def _v_quest_end(cls, v):
			if v is None:
				return None
			return _UnixTimestampInt(v)

		@pd.field_validator("curse_end", mode="before")
		@classmethod
		def _v_curse_end(cls, v):
			if v is None:
				return None
			return _UnixTimestampInt(v)

		@pd.field_validator("mechanic_end", mode="before")
		@classmethod
		def _v_mechanic_end(cls, v):
			if v is None:
				return None
			return _UnixTimestampInt(v)

	class _ZooExtra(_BM):
		invisible: bool = False
		"""Whether or not this profile is invisible (Under the 💀 Curse of Invisibility)"""

		distancing_curse: bool = False
		"""Whether or not this profile is under the 💀 Curse of Distancing

		~~Presumably the displayed margin in css px on the zoo website (if this profile is under the 💀 Curse of Distancing)~~.
		Edit: Colon's pretty sure it's supposed to be a bool, source: 9tbh #zoo-talk https://discord.com/channels/461575285364752384/1010033674424684625/1390120921863426060
		"""

		@pd.field_validator("distancing_curse", mode="before")
		@classmethod
		def _v_distancing_curse(cls, v):
			if isinstance(v, int):
				return bool(v)  # presumably if it's 0, then the curse is not active, though it's omitted then
			if isinstance(v, bool):  # in case Colon ever updates this value to be bool
				return v
			return v  # raise pydantic validation error if it happens to ever not be int or bool yet still present

	class Zoo(_BM):
		"""Represents a user-owned Zoo (profile) acquired from the `/api/profile` endpoint or `zooo.Client.fetch_zoo()`."""

		id: ProfileInfo | NPCProfileInfo
		"""Full str ID of this profile, for example `'1234123412341234_kitsune'`."""
		selected_profile: str
		"""Profile ID of the selected profile of this user at the time of the API request."""
		profiles: list[ProfileID]
		"""List of all (visible) profile IDs owned by this user."""
		user: ZooUser
		"""Basic information about this profile's owner."""
		name: str
		"""Zoo name of this profile."""
		nickname: str
		"""Terminal nickname of this Zoo profile's user."""
		color: _HexInt | None
		"""Embed color of this profile."""
		owner: bool
		"""Whether or not this Zoo was requested with authorisation (`cookie` fields should be available)."""
		private: bool
		"""Whether or not this Zoo was private at the time of the API request."""
		theme: ThemeID | None = Field(alias="profileTheme")
		"""Current profile theme of this profile at the time of the API request."""
		secret_info: ZooSecretInfo | None = None
		"""[API KEY] Represents the so called 'secret info' of this profile.

		This contains:
		- cooldowns
		- terminal extra info
		- garden extra info
		- rescue & quest promises
		- ...

		If this profile doesnt have the API KEY relic equipped, this will simply be `None`.
		"""
		score: int
		"""Zoo score of this profile at the time of the API request."""
		completion: float
		"""Completion percentage of this profile."""
		unique_animals: ZooUniqueAnimals
		"""Unique common, rare or all animals in this profile."""
		total_animals: ZooTotalAnimals
		"""Common or rare total (non-unique) animals in this profile."""
		pinned_animal_score: dict[PinType, int]
		"""Score as returned by the API (not computed), on a pin-by-pin basis. For example animals pinned with the red pin have this much score amongst them.

		If the item is not a part of the dictionary, its pin count is 0, use pinned_animal_score.get(..., 0)
		"""
		total_items: int
		"""Total number of items in this profile."""
		total_cosmetics: int
		"""Total number of cosmetics in this profile."""
		total_trophies: int
		"""Total number of trophies in this profile."""
		total_leader_xp: int
		"""Total number of leader XP in this profile."""
		unspent_leader_xp: int
		"""Unspent number of leader XP in this profile."""
		equipped_relics: list[str]
		"""Names of equipped relics in this profile."""
		equipped_cosmetics: list[str]
		"""Names of equipped cosmetics in this profile."""
		equipped_cosmetic: str | None
		"""Equipped (emoji/non-effect) cosmetic in this profile."""
		equipped_leader: str | None
		"""Equipped leader in this profile."""
		cosmetic_icon: str | None
		"""Icon of `equipped_cosmetic` in this profile (emoji but may be discord emoji syntax.)."""
		notifications: int
		"""Number of unspent rescue notifications in this profile."""
		auto_rescues: int
		"""Number of unspent auto-rescues in this profile."""
		animals: list[ZooAnimal]
		"""List of unparsed animals (zero-amount = excluded) in this profile."""
		items: list[ZooItem]
		"""List of unparsed items (zero-amount = excluded) in this profile."""
		relics: list[ZooRelic]
		"""List of unparsed relics (unobtained = excluded) in this profile."""
		cosmetics: list[ZooCosmetic]
		"""List of unparsed cosmetics (unobtained = excluded) in this profile."""
		leaders: list[ZooLeader]
		"""List of unparsed leaders (unobtained = excluded) in this profile."""
		quests: list[ZooListedQuest]
		"""List of unparsed quests (undiscovered = excluded) in this profile."""
		quest: ZooCurrentQuest | None
		"""The current quest in this profile."""
		curse: ZooCurse | None
		"""The current curse in this profile."""
		terminal: ZooTerminal = {"unlocked": False}
		"""Represents the terminal-related data of this profile."""
		stats: list[ZooStat]
		"""List of stats for this profile. (I think this never gets used outside of NPC (`Zoo.user.npc`) profiles)"""
		goals: list[ZooGoal]
		"""List of unparsed (undiscovered = excluded) goals in this profile."""
		goal_tiers: int = 0
		"""Total goal tiers achieved by this profile."""
		goal_completes: int = Field(alias="goalsComplete")  # For consistency with 'goal_tiers'
		"""Total goals completed achieved by this profile."""
		extra_data: list[list]  # pydantic wont let me do list[list[str, str] | list[str, str, int]]
		"""Extra data: list[list[str, str] | list[str, str, int]], that means: a list of {a list that can contain 2 strings or 2 strings and 1 int}

		This is used to store data such as:
		- Terminal admin
		- Garden repaired
		- Fusions: X
		- etc.

		This is the data shown at the right side of the screen when opening the profile in a web browser.

		Example (from Colon's profile):
		```py
		[
			['<:leader_xp:1169766775441854545>', 'Total Leader XP', 244],
			['🔶', 'Unspent Leader XP', 6],
			['💠', 'Leader XP Upgrades', 19],
			['🔑', 'Terminal admin'],
			['🚿', 'Garden repaired'],
			['🎴', 'Cards', 644],
			['🔧', 'Murphy Points', 4270],
			['<:pebbles:1228931536460709928>', 'Pebbles', 68],
			['↔️', 'Fusions', 39],
			['<:zootoken_tm:1228931474590404619>', 'Zoo Tokens™', 198095],
			['<:aetherium:1228931467237916702>', 'Aetherium', 2],
			['<:egg_base:1228934812153155685>', 'NFBs owned', 30],
			['💵', 'Net worth', 8257],
			['<:fluff:1078401638370385960>', 'Made the game'],
		]
		```
		"""
		settings: ZooSettings
		"""The user-selected `/settings` of this profile."""
		unlocked_themes: list[ZooUnlockedTheme] = Field(default_factory=list)
		"""A list of unlocked themes in this profile.

		May be `[]` if not authorised with a cookie (`.owner`).
		"""
		extra: _ZooExtra = Field(default_factory=dict)
		"""A mapping of extras/random properties idk, not to be confused with extra_data, which contains a list of formatted strings to be displayed on the website."""

		# the '_apiKey' field has been yanked out because it's useless and mostly it's None but sometimes a dict congratulating you on finding the key. I decided it's not needed here.

		@pd.field_validator("id", mode="before")
		@classmethod
		def _converter_id(cls, value):
			try:
				return NPCProfileInfo(value)
			except ValueError:
				return ProfileInfo.from_str(value)

		@pd.field_validator("color", mode="before")
		@classmethod
		def _converter_to_hexint(cls, v):
			if v is None:
				return None
			return _HexInt(v, base=16)

		@pd.field_validator("pinned_animal_score", mode="before")
		@classmethod
		def _fill_in_missing_pin_enum_variants(cls, v):
			if not isinstance(v, MutableMapping):
				return {}

			v = {PinType(key) if isinstance(key, str) else key: val for key, val in v.items()}

			for variant in PinType:
				if variant not in v:
					v[variant] = 0

			return v

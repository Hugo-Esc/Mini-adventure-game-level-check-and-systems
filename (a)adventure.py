import random
import os, time
import time, sys

# GAME COLORS
class colors():
    GREEN = "\033[32m"
    DARK_SHADE = "\033[2m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    WHITE = "\033[0m"
    CYAN = "\033[36m"
    PURPLE = "\033[35m"
    GRAY = "\033[30m"
    ORANGE = "\033[38;5;208m"
    # 40-49 = highlight
    ITALIZE = "\033[3m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DOUBLE_UNDERLINE = "\033[21m"
    STRIKE_THROUGH = "\033[9m"

# Player Class
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.max_health = 100
        self.health = 100
        self.gold = 0
        self.xp = 0
        self.potions = 1  # Start with 1 potion

    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        print(f"\n{colors.ORANGE}{self.name} leveled up! You are now level {self.level}.")
    
    def use_potion(self):
        if self.potions > 0:
            heal_amount = 30
            self.health = min(self.health + heal_amount, self.max_health)
            self.potions -= 1
            print(f"\nYou used a potion and healed {colors.GREEN}{heal_amount} HP!")
            print(f"HP: {self.health}/{self.max_health}")
            print(f"{colors.PURPLE}Potions left: {self.potions}")
        else:
            print("\nYou have no potions left!")

#check: savegame.txt
def save_game(player, current_map):
    with open("savegame.txt", "w") as file:
        file.write(player.name + "\n")
        file.write(str(player.level) + "\n")
        file.write(str(player.max_health) + "\n")
        file.write(str(player.health) + "\n")
        file.write(str(player.gold) + "\n")
        file.write(str(player.xp) + "\n")
        file.write(str(player.potions) + "\n")
        file.write(str(current_map) + "\n")
    print(f"\n{colors.ORANGE}Game Saved Successfully!")

def load_game():
    try:
        with open("savegame.txt", "r") as file:
            lines = file.readlines()

        name = lines[0].strip()
        player = Player(name)
        player.level = int(lines[1])
        player.max_health = int(lines[2])
        player.health = int(lines[3])
        player.gold = int(lines[4])
        player.xp = int(lines[5])
        player.potions = int(lines[6])
        current_map = int(lines[7])

        print(f"\n{colors.ORANGE}Save file loaded successfully!")
        return player, current_map
    except FileNotFoundError:
        print(f'\n{colors.RED}No save file found.')
        return None, None

def battle(player):
    enemy_health = random.randint(40, 60) + (player.level * 5)
    print(f'{colors.RED}\nAn enemy appears!')
    print(f"Enemy HP: {enemy_health}")

    while player.health > 0 and enemy_health > 0:
        action = input(f"\n{colors.WHITE}Press ENTER to attack or type 'p' to use potion: ").lower()
        if action == "p":
            player.use_potion()
            continue

        damage = random.randint(10, 20) + (player.level * 2)
        enemy_health -= damage
        print(f"You deal {damage} damage!")
        if enemy_health <= 0:
            print("Enemy defeated!")
            break
        enemy_damage = random.randint(5, 15) + (player.level * 2)
        player.health -= enemy_damage
        player.health = max(player.health, 0)
        print(f"Enemy deals {enemy_damage} damage!")
        print(f"{colors.GREEN}Your HP: {player.health}/{player.max_health}")

    if player.health <= 0:
        print(f"\n{colors.RED}You were defeated...")
        return False

    # Rewards
    gold_reward = random.randint(15, 30)
    xp_reward = random.randint(20, 40)
    player.gold += gold_reward
    player.xp += xp_reward
    time.sleep(2)
    os.system("cls" if os.name == "nt" else "clear")
    print(f"\nYou gained {colors.YELLOW}{gold_reward} gold!{colors.WHITE}")
    print(f"You gained {colors.BLUE}{xp_reward} XP!{colors.WHITE}")

    # Level check
    if player.xp >= player.level * 100:
        player.xp = 0
        player.level_up()
    return True  # Player survived

def roundabout_path(player):
    event = random.random()

    if event < 0.4:
        return battle(player)
    elif event < 0.7:
        gold_found = random.randint(20, 50)
        player.gold += gold_found
        print(f"\nYou found {colors.YELLOW}{gold_found} gold!")
        return True
    
    elif event < 0.9:
        player.potions += 1
        print("\nYou found a potion!")
        print(f"{colors.PURPLE}Potions: {player.potions}")
        return True
    else:
        heal_amount = random.randint(15, 30)
        player.health = min(player.health + heal_amount, player.max_health)
        print(f"\nYou found herbs and healed {colors.GREEN}{heal_amount} HP!")
        return True

#Dark forest map
def dark_forest(player):
    print(f"\n{colors.GRAY}You enter the Dark Forest...")
    print("The enemies here are stronger.")

    alive = battle(player)
    if not alive:
        return False

    print(f"\n{colors.WHITE}You survive the forest encounter.")
    print("The path ahead leads deeper...")
    return True

#Shop function
def shop(player):
    print(f"\n{colors.CYAN}Welcome to the Shop!")
    print(f'{colors.YELLOW}Gold: {player.gold}{colors.WHITE}')
    print("1. Buy Potion (25 gold)")
    print("2. Heal to Full (40 gold)")
    print("3. Leave Shop")

    choice = input("\nWhat would you like to do? ")

    if choice == "1":
        if player.gold >= 25:
            player.gold -= 25
            player.potions += 1
            print("\nYou bought a potion!")
            print(f"{colors.PURPLE}Potions: {player.potions}")
        else:
            print(f'\n{colors.RED}Not enough gold.')

    elif choice == "2":
        if player.gold >= 40:
            player.gold -= 40
            player.health = player.max_health
            print(f"\n{colors.GREEN}You are fully healed!")
        else:
            print(f'\n{colors.RED}Not enough gold.')

    elif choice == "3":
        print("\nYou leave the shop.")
        time.sleep(3)
        os.system("cls" if os.name == "nt" else "clear")
    else:
        print("\nInvalid choice.")
    return True

def second_road(player, current_map):
    print(f"\n{colors.RED}You arrive at the Mountain Pass.")
    print("Enemies here are stronger.")
    print(f"\n{colors.WHITE}1. Climb the Steep Trail (High Risk)")
    print("2. Explore the Abandoned Camp (Reward Chance)")
    print("3. Check Stats")
    print("4. Return to Previous Road")
    print("5. Enter the Demon King's Castle (Level 5 Required)")
    print("6. Save Game")

    choice = input("\nWhat do you choose? ")

    if choice == "1":
        print("\nYou climb the steep mountain trail...")
        alive = strong_battle(player)
        return alive, 2
    elif choice == "2":
        print("\nYou explore the abandoned camp...")
        alive =  mountain_event(player)
        return alive, 2
    elif choice == "3":
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{colors.ORANGE}{player.name}'s Stats:")
        print(f'{colors.CYAN}Level: {player.level}')
        print(f'{colors.GREEN}HP: {player.health}/{player.max_health}')
        print(f'{colors.YELLOW}Gold: {player.gold}')
        print(f'{colors.BLUE}XP: {player.xp}')
        print(f'{colors.PURPLE}Potions: {player.potions}')
        return True, 2

    elif choice == "4":
        print("\nYou travel back to the Main Road.")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
        return True, 1
    elif choice == "5":
        if player.level >= 5:
            print(f"\n{colors.PURPLE}You approach the Demon King's Castle...")
            return True, 3
        else:
            print(f"\n{colors.RED}A dark force blocks your path. You are not strong enough.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            return True, 2
    
    elif choice == "6":
        save_game(player, current_map)
        return True, 2
    else:
        print("Invalid choice.")
        return True, 2

def strong_battle(player):
    enemy_health = random.randint(70, 100) + (player.level * 8)
    print(f"\n{colors.RED}A powerful enemy appears!")

    while player.health > 0 and enemy_health > 0:
        action = input(f"\n{colors.WHITE}Press ENTER to attack or type 'p' to use potion: ").lower()

        if action == "p":
            player.use_potion()
            continue
        damage = random.randint(15, 25) + (player.level * 3)
        enemy_health -= damage
        print(f"You deal {damage} damage!")

        if enemy_health <= 0:
            print("Enemy defeated!")
            break

        enemy_damage = random.randint(10, 20) + (player.level * 3)
        player.health -= enemy_damage
        player.health = max(player.health, 0)
        print(f"Enemy deals {enemy_damage} damage!")
        print(f"{colors.GREEN}Your HP: {player.health}/{player.max_health}")

    if player.health <= 0:
        print(f"\n{colors.RED}You were defeated...")
        return False
    player.gold += random.randint(40, 70)
    player.xp += random.randint(40, 70)
    time.sleep(1.5)
    os.system("cls" if os.name == "nt" else "clear")
    print(f"\n{colors.YELLOW}You earned greater rewards!")

    if player.xp >= player.level * 100:
        player.xp = 0
        player.level_up()
    return True

def mountain_event(player):
    event = random.random()

    if event < 0.5:
        print("\nA hidden enemy attacks!")
        return strong_battle(player)
    elif event < 0.8:
        gold_found = random.randint(50, 100)
        player.gold += gold_found
        print(f"\nYou found {colors.YELLOW}{gold_found} gold in the camp!")
        return True
    else:
        player.potions += 2
        print(f"\nYou found 2 potions!")
        print(f"{colors.PURPLE}Potions: {player.potions}")
        return True

def boss_castle(player, current_map):
    print(f"{colors.PURPLE}You stand inside the Demon King's Castle.")
    print(f"\n{colors.RED}1. Confront the Demon King")
    print(f"{colors.BLUE}2. Retreat to Mountain Pass")

    choice = input(f"\n{colors.WHITE}What do you choose? ")

    if choice == "1":
        alive = boss_battle(player)
        if alive:
            print(f"\n{colors.YELLOW}The Demon King has fallen!")
            print(f"{colors.YELLOW}You have saved the kingdom!")
            return False, 3   # End game (win)
        else:
            return False, 3   # End game (death)

    elif choice == "2":
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
        print("\nYou retreat back to the Mountain Pass.")
        return True, 2
    else:
        print("Invalid choice.")
        return True, 3

def boss_battle(player):
    boss_health = 200 + (player.level * 10)
    print(f"\n{colors.PURPLE}The Demon King appears!")
    print(f"{colors.RED}Boss HP: {boss_health}")

    while player.health > 0 and boss_health > 0:
        action = input(f"\n{colors.WHITE}Press ENTER to attack or type 'p' to use potion: ").lower()

        if action == "p":
            player.use_potion()
            continue
        damage = random.randint(20, 35) + (player.level * 4)
        boss_health -= damage
        print(f"You deal {damage} damage!")
        if boss_health <= 0:
            break

        boss_damage = random.randint(15, 30) + (player.level * 4)
        player.health -= boss_damage
        player.health = max(player.health, 0)

        print(f"The Demon King deals {boss_damage} damage!")
        print(f"{colors.GREEN}Your HP: {player.health}/{player.max_health}")

    if player.health <= 0:
        print(f"\n{colors.RED}You were slain by the Demon King...")
        return False
    return True

# Main road
def main_road(player, current_map):
    print(f'{colors.BLUE}\n\t-You stand on the main road-')
    print(f'{colors.WHITE}\n1. Take the Direct Path')
    print("2. Take the Roundabout Path")
    print("3. Check Stats")
    print("4. Venture to the Dark Forest (Level 3 Required)")
    print("5. Visit Shop")
    print("6. Travel to Mountain Pass (Level 3 Required)")
    print("7. Save Game")

    choice = input("\nWhat do you choose? ")

    if choice == "1":
        print(f'\n{colors.GRAY}You walk down the direct path...')
        alive = battle(player)
        return alive, 1
    elif choice == "2":
        alive = roundabout_path(player)
        return alive, 1
    elif choice == "3":
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{colors.ORANGE}{player.name}'s Stats:")
        print(f'{colors.CYAN}Level: {player.level}')
        print(f'{colors.GREEN}HP: {player.health}/{player.max_health}')
        print(f'{colors.YELLOW}Gold: {player.gold}')
        print(f'{colors.BLUE}XP: {player.xp}')
        print(f'{colors.PURPLE}Potions: {player.potions}')

    elif choice == "4":
        if player.level < 3:
            print(f"\n{colors.GRAY}You feel too weak to enter the Dark Forest...")
            print("You should train more before going there.")
            return True, 1
        else:
            alive = dark_forest(player)
            return alive, 1
        
    elif choice == "5":
        alive = shop(player)
        return alive, 1
    
    elif choice == "6":
        if player.level >= 3:
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")
            print(f"\n{colors.GRAY}You travel to the Mountain Pass...")
            return True, 2
        else:
            print(f"\n{colors.RED}You are not strong enough yet.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            return True, 1
    
    elif choice == "7":
        save_game(player, current_map)
        return True, 1
    else:
        print("Invalid choice.")
    return True, 1

# New game/reload game
print(f'\n\t\t{colors.RED}==== ADVENTURE GAME ===={colors.WHITE}')
print("1. New Game")
print("2. Load Game")

start_choice = input("\nChoose option: ")

if start_choice == "2":
    player, current_map = load_game()
    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
    
    #if first time playing
    if player is None:
        print("\nStarting new game instead...")
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        name = input(f'\nENTER WARRIOR NAME:{colors.ORANGE} ').strip().capitalize()
        player = Player(name)
        current_map = 1
        
else:
    name = input(f'\nENTER WARRIOR NAME:{colors.ORANGE} ').strip().capitalize()
    player = Player(name)
    current_map = 1
    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
    print(f"\n{player.name}'s stats: {colors.CYAN}Level {player.level}, {colors.GREEN}HP {player.health}/{player.max_health}, {colors.YELLOW}Gold {player.gold}, {colors.BLUE}XP {player.xp}")

# Game loop
alive = True

while alive:
    if current_map == 1:
        alive, current_map = main_road(player, current_map)
    elif current_map == 2:
        alive, current_map = second_road(player, current_map)
    elif current_map == 3:
        alive, current_map = boss_castle(player, current_map)

print(f"\n\t{colors.WHITE}=== GAME OVER ===")
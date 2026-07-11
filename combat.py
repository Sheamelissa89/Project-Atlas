def battle(player, enemy):
    print(f"A wild {enemy.name} appears!")

    while player.is_alive() and enemy.is_alive():
        player.attack(enemy)

        if enemy.is_alive():
            enemy.attack(player)

    if player.is_alive():
        print(f"{player.name} defeated the {enemy.name}!")
        player.gain_exp(enemy.exp_reward)
        player.receive_potions(enemy.potion_reward)
    else:
        print(f"{player.name} has fallen in battle.")
from .entity import Entity


class Enemy(Entity):
    def __init__(
        self,
        name,
        health=60,
        damage=15,
        exp_reward=50,
        gold_reward=10,
        potion_reward=0
    ):
        super().__init__(name, health, damage)

        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.potion_reward = potion_reward

    def give_rewards(self, player):
        print(f"{self.name} dropped rewards!")

        player.gain_exp(self.exp_reward)
        player.receive_gold(self.gold_reward)
        player.receive_potions(self.potion_reward)

    def show_status(self):
        print("===== ENEMY STATUS =====")
        print(f"Name: {self.name}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Damage: {self.damage}")
        print(f"EXP Reward: {self.exp_reward}")
        print(f"Gold Reward: {self.gold_reward}")
        print(f"Potion Reward: {self.potion_reward}")
        print("========================")

   

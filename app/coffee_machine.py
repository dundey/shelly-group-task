# coffee_machine.py

# Represents a cup with coffee and its content
class CupWithCoffee:
    def __init__(self):
        self.content = "coffee"  # Set the content to coffee

# Represents a cup with tea and its content
class CupWithTea:
    def __init__(self):
        self.content = "tea"  # Set the content to tea

# Represents a coffee machine and its functionalities
class CoffeeMachine:
    def __init__(self):
        # Initialize coin storage and count of coins by denomination
        self.coins = {'10st': 0, '20st': 0, '50st': 0, '1lv': 0}
        # Initialize the balance to track the total amount of money inserted
        self.balance = 0
        # Initialize containers with their initial volumes or quantities for water, coffee, tea, and waste
        self.containers = {'water': 5000.0, 'coffee': 100.0, 'tea': 50.0, 'waste': 0.0}  # In milliliters and grams
        
    # Accepts and stores coins in the machine
    def add_coin(self, coin: str) -> None:
        # Check if the coin is an accepted denomination and update storage and balance
        if coin in self.coins:
            self.coins[coin] += 1
            self._update_balance(coin)
            
    # Dispenses coffee if there is a sufficient balance
    def get_coffee(self) -> CupWithCoffee:
        if self.balance >= 20 and self.containers['coffee'] > 0 and self.containers['water'] >= 200:
            self.balance -= 20
            self.containers['coffee'] -= 10
            self.containers['water'] -= 200
            self.containers['waste'] += 10
            return CupWithCoffee()
        else:
            return None  # Return None if there is insufficient balance, coffee, or water
    
    # Dispenses tea if there is a sufficient balance
    def get_tea(self) -> CupWithTea:
        if self.balance >= 10 and self.containers['tea'] > 0 and self.containers['water'] >= 200:
            self.balance -= 10
            self.containers['tea'] -= 5
            self.containers['water'] -= 200
            self.containers['waste'] += 5
            return CupWithTea()
        else:
            return None  # Return None if there is insufficient balance, tea, or water
    
    # Handles change, which is not returned by this machine
    def get_change(self) -> None:
        pass
    
    # Checks the machine's power supply voltage
    def get_voltage(self) -> int:
        return 220  # Machine operates on 220V power
    
    # Checks the volume or quantity of materials in a specific container
    def get_volume_by_container(self, container: str) -> float:
        # Return the volume or quantity of the specified container
        return self.containers.get(container, 0.0)
    
    # Checks the number of coins stored by denomination
    def get_number_of_coins(self, coin: str) -> int:
        # Return the count of coins by specified denomination
        return self.coins.get(coin, 0)
    
    # Updates the balance based on the coin denomination added
    def _update_balance(self, coin: str) -> None:
        # Values assigned to each coin denomination
        coin_values = {'10st': 10, '20st': 20, '50st': 50, '1lv': 100}
        # Update balance according to the value of the coin added
        self.balance += coin_values.get(coin, 0)

    # Gets the current balance in the machine
    def get_balance(self) -> int:
        # Return the current balance
        return self.balance

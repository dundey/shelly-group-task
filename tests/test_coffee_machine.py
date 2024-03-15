# test_coffee_machine.py

import pytest
from app.coffee_machine import CoffeeMachine, CupWithCoffee, CupWithTea

@pytest.fixture
def machine():
    """Fixture to provide a fresh instance of CoffeeMachine for each test."""
    return CoffeeMachine()

def test_accepting_valid_coins(machine):
    """Ensure the machine accepts all valid coins and updates balance and coin storage accordingly."""
    valid_coins = ['10st', '20st', '50st', '1lv']
    for coin in valid_coins:
        machine.add_coin(coin)
    assert all(machine.get_number_of_coins(coin) == 1 for coin in valid_coins)
    assert machine.get_balance() == sum([10, 20, 50, 100])

def test_ignoring_invalid_coins(machine):
    """Verify the machine does not accept or store invalid coin denominations."""
    invalid_coins = ['1st', '2st', '5st', '2lev', '1eur']
    initial_balance = machine.get_balance()
    for coin in invalid_coins:
        machine.add_coin(coin)
    assert machine.get_balance() == initial_balance
    assert all(machine.get_number_of_coins(coin) == 0 for coin in invalid_coins)

def test_buying_coffee_with_exact_change(machine):
    """Check if a coffee can be bought with exact change and balance is correctly adjusted."""
    machine.add_coin('20st')
    coffee = machine.get_coffee()
    assert isinstance(coffee, CupWithCoffee)
    assert machine.get_balance() == 0

def test_buying_tea_with_exact_change(machine):
    """Check if tea can be bought with exact change and balance is correctly adjusted."""
    machine.add_coin('10st')
    tea = machine.get_tea()
    assert isinstance(tea, CupWithTea)
    assert machine.get_balance() == 0

def test_insufficient_balance_for_coffee(machine):
    """Ensure coffee cannot be bought with insufficient balance; machine should not dispense coffee."""
    machine.add_coin('10st')
    coffee = machine.get_coffee()
    assert coffee is None

def test_insufficient_balance_for_tea(machine):
    """Ensure tea cannot be bought with insufficient balance; machine should not dispense tea."""
    coffee = machine.get_tea()
    assert coffee is None

def test_get_change_after_adding_a_coin(machine):
    """Test getting change after adding a coin."""
    machine.add_coin('1lv')
    assert machine.get_change() is None
    assert machine.get_balance() == 100

def test_get_change_after_adding_a_coin_and_buy_coffee(machine):
    """Test getting change after adding balance, buying coffee, and trying to get change."""
    machine.add_coin('1lv')
    machine.get_coffee()
    machine.get_change()
    assert machine.get_change() is None
    assert machine.get_balance() == 80
    
def test_power_supply_voltage(machine):
    """Confirm the machine reports the correct operating voltage of 220V."""
    assert machine.get_voltage() == 220

def test_volume_decrease_and_waste_increase_after_dispensing_drinks(machine):
    """Check volumes of ingredients decreases and waste increases after dispensing drinks."""
    machine.add_coin('1lv')
    machine.get_coffee()
    machine.get_tea()
    assert machine.get_volume_by_container('water') == 4600.0
    assert machine.get_volume_by_container('coffee') == 90.0
    assert machine.get_volume_by_container('tea') == 45.0
    assert machine.get_volume_by_container('waste') == 15.0

def test_volume_check_for_nonexistent_container(machine):
    """Ensure querying volume for a nonexistent container returns 0.0."""
    assert machine.get_volume_by_container('milk') == 0.0

def test_coin_count_after_insertion(machine):
    """Test if the machine accurately counts the number of each coin inserted."""
    coins = ['10st', '10st', '20st']
    for coin in coins:
        machine.add_coin(coin)
    assert machine.get_number_of_coins('10st') == 2
    assert machine.get_number_of_coins('20st') == 1
    assert machine.get_number_of_coins('50st') == 0
    assert machine.get_number_of_coins('1lev') == 0

def test_coin_count_for_nonexistent_denomination(machine):
    """Ensure machine returns 0 for the count of a nonexistent coin denomination."""
    assert machine.get_number_of_coins('5st') == 0

def test_balance_exceeding_purchase_for_multiple_procuts(machine):
    """Test adding balance and attempting to buy multiple products exceeding the total added balance."""
    machine.add_coin('10st')
    machine.add_coin('20st')
    first_coffee = machine.get_coffee()
    second_coffee = machine.get_coffee()
    assert isinstance(first_coffee, CupWithCoffee)
    assert second_coffee is None
    assert machine.get_balance() == 10

def test_exact_balance_for_multiple_purchase(machine):
    """Test scenario where added balance matches the exact total cost of selected multiple products."""
    machine.add_coin('10st')
    machine.add_coin('20st')
    coffee = machine.get_coffee()
    tea = machine.get_tea()
    assert isinstance(coffee, CupWithCoffee)
    assert isinstance(tea, CupWithTea)
    assert machine.get_balance() == 0

def test_exceeding_available_coffee(machine):
    """Test dispensing coffee until the available quantity in the machine is exceeded."""
    coins = ['1lv', '1lv', '1lv']
    for coin in coins:
        machine.add_coin(coin)
    
    while True:
        tea = machine.get_coffee()
        if tea is None:
            break

    assert machine.get_volume_by_container('coffee') == 0.0
    assert machine.get_coffee() is None


def test_exceeding_available_tea(machine):
    """Test dispensing tea until the available quantity in the machine is exceeded."""
    coins = ['1lv', '1lv']
    for coin in coins:
        machine.add_coin(coin)
    
    while True:
        tea = machine.get_tea()
        if tea is None:
            break

    assert machine.get_volume_by_container('tea') == 0.0
    assert machine.get_tea() is None




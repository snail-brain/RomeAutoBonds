from brownie import config, Contract, interface, accounts, chain, SolarLibrary
from scripts.contracts import (
    bonds,
    staking,
    staking_helper,
    rome,
    sRome,
    frax,
    mim,
    wmovr,
    solarRouter,
    romeFrax,
)
account = accounts.add(config["wallets"]["from_key"])


def main():
    # swap_rome_to_frax(rome.balanceOf(account.address))
    # bond_frax()
    print(check_discounts())


# Staking


def stake(_amount):
    tx = staking_helper.stake(_amount, account.address, {"from": account})
    tx.wait(1)
    print(
        "Rome Balance: ",
        rome.balanceOf(account.address) / 10 ** rome.decimals(),
        "sRome Balance: ",
        sRome.balanceOf(account.address) / 10 ** sRome.decimals(),
    )


def un_stake(_amount):
    tx = staking.unstake(_amount, True, {"from": account})
    tx.wait(1)
    print(
        "Rome Balance: ",
        rome.balanceOf(account.address),
        "sRome Balance: ",
        sRome.balanceOf(account.address),
    )

# Swaps


def swap_rome_to_mim(_amount):
    path = [rome.address, frax.address, wmovr.address, mim.address]
    currentQuote = (solarRouter.getAmountsOut(_amount, path, 25)[3])
    min_amount = currentQuote - currentQuote * .005

    tx = solarRouter.swapExactTokensForTokens(
        _amount,
        min_amount,
        path,
        account.address,
        len(chain) + 10000000000,
        {"from": account},
    )
    tx.wait(1)

    print(
        "Current Quote: ", min_amount / 10 ** 18,
        "Mim Balance: ",
        mim.balanceOf(account.address) / 10 ** mim.decimals(),
        "Rome Balance: ",
        rome.balanceOf(account.address) / 10 ** rome.decimals(),
    )


def swap_rome_to_frax(_amount):
    path = [rome.address, frax.address]
    currentQuote = (solarRouter.getAmountsOut(_amount, path, 25)[1])
    min_amount = currentQuote - currentQuote * .005

    tx = solarRouter.swapExactTokensForTokens(
        _amount, min_amount, path, account.address, len(chain) + 10000000000, {"from": account})
    tx.wait(1)

    print(
        "Current Quote: ", min_amount / 10 ** 18,
        "Frax Balance: ",
        frax.balanceOf(account.address) / 10 ** mim.decimals(),
        "Rome Balance: ",
        rome.balanceOf(account.address) / 10 ** rome.decimals(),
    )


def swap_rome_to_movr(_amount):
    path = [rome.address, frax.address, wmovr.address]
    currentQuote = (solarRouter.getAmountsOut(_amount, path, 25)[2])
    min_amount = currentQuote - currentQuote * .005

    tx = solarRouter.swapExactTokensForTokens(
        _amount, min_amount, path, account.address, len(chain) + 10000000000, {"from": account})
    tx.wait(1)

    print(
        "Current Quote: ", min_amount / 10 ** 18,
        "wMOVR Balance: ",
        wmovr.balanceOf(account.address) / 10 ** wmovr.decimals(),
        "Rome Balance: ",
        rome.balanceOf(account.address) / 10 ** rome.decimals(),
    )


def add_rome_frax_liq(_amount):
    path = [rome.address, frax.address]
    currentQuote = (solarRouter.getAmountsOut(_amount / 2, path, 25)[1])
    min_amount = currentQuote - currentQuote * .005

    tx_swap = solarRouter.swapExactTokensForTokens(
        _amount / 2, min_amount, path, account.address, len(chain) + 10000000000, {"from": account})
    tx_swap.wait(1)

    print("Rome Balance: ", rome.balanceOf(account.address) / 10 ** rome.decimals(),
          "Frax Balance: ", frax.balanceOf(account.address) / 10 ** frax.decimals())

    tx_add = solarRouter.addLiquidity(rome.address, frax.address, rome.balanceOf(account.address), frax.balanceOf(
        account.address), rome.balanceOf(account.address) * .005, frax.balanceOf(account.address) * .005, account.address, len(chain) + 10000000000, {"from": account})
    tx_add.wait(1)

    print("Rome/Frax LP: ", romeFrax.balanceOf(account.address) / 10 ** 18)

# Bonds
# Assume I've already made the swap to the token to be bonded


# Frax
def bond_frax():
    bond_price = bonds[1].bondPrice()
    tx = bonds[1].deposit(frax.balanceOf(
        account.address), (bond_price + (bond_price * .005)), account.address, {"from": account})
    tx.wait(1)

    print("Frax Balance: ", frax.balanceOf(account.address),
          "Percent Vested: ", bonds[1].percentVestedFor(account.address))


# Mim
def bond_mim():
    bond_price = bonds[2].bondPrice()
    tx = bonds[2].deposit(mim.balanceOf(
        account.address), (bond_price + (bond_price * .005)), account.address, {"from": account})
    tx.wait(1)

    print("Mim Balance: ", mim.balanceOf(account.address))


# Wmovr
def bond_wmovr():
    bond_price = bonds[3].bondPrice()
    tx = bonds[3].deposit(wmovr.balanceOf(
        account.address), (bond_price + (bond_price * .005)), account.address, {"from": account})
    tx.wait(1)

    print("MOVR Balance: ", wmovr.balanceOf(account.address))


# Rome/Frax
def bond_rome_frax():
    bond_price = bonds[0].bondPrice()
    tx = bonds[0].deposit(romeFrax.balanceOf(
        account.address), (bond_price + (bond_price * .005)), account.address, {"from": account})
    tx.wait(1)

    print("Rome/Frax Balance: ", romeFrax.balanceOf(account.address))


# Check Bond Discounts
def check_discounts():
    discounts = []
    # Rome Price
    rome_price = solarRouter.getAmountsOut(
        1 * 10 ** rome.decimals(), [rome.address, frax.address], 25)[1]

    # Find discounts for each bond
    # Only consider bonds that are still for sale
    frax_discount = [
        (rome_price - bonds[1].bondPriceInUSD()) / rome_price, "frax"]
    if bonds[1].maxPayout() > 0:
        discounts.append(frax_discount)

    wmovr_discount = [
        (rome_price - bonds[3].bondPriceInUSD()) / rome_price, "wmovr"]
    if bonds[3].maxPayout() > 0:
        discounts.append(wmovr_discount)

    rome_frax_discount = [
        (rome_price - bonds[0].bondPriceInUSD()) / rome_price, "rome/frax"]
    if bonds[0].maxPayout() > 0:
        discounts.append(rome_frax_discount)

    mim_discount = [
        (rome_price - bonds[2].bondPriceInUSD()) / rome_price, "mim"]
    if bonds[2].maxPayout() > 0:
        discounts.append(mim_discount)

    # Find and return the best discount
    best_discount = 0
    for dis in discounts:
        if best_discount == 0:
            best_discount = dis
        elif best_discount[0] < dis[0]:
            best_discount = dis

    return best_discount


# Check If Bonding is worth

# Total Rome at End of Bonding Cycle if left staked
def rome_staked(_amount, _rate):
    total = _amount
    count = 15

    while count > -1:
        total += total * _rate
        count -= 1
    return total

# Total Rome at End of Bonding Cycle if bonded


def rome_bond_stake(_amount, _rate):
    total = 0
    count = 15
    add = _amount / 16

    while count > -1:
        total += add
        total += total * _rate
        count -= 1
    return total

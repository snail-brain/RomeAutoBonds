from brownie import config, accounts, chain
from scripts.contracts import *
account = accounts.add(config["wallets"]["from_key"])


def main():
    # swap_rome_to_frax(rome.balanceOf(account.address))
    # bond_frax()
    un_stake(sRome.balanceOf(account.address))
    add_rome_frax_liq(rome.balanceOf(account.address))
    bond(romeFrax, romeFraxBonds)


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


def make_swap(_amount, path, token):
    currentQuote = (solarRouter.getAmountsOut(
        _amount, path, 25)[len(path) - 1])
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

    print("Current Quote: ", min_amount / 10 ** 18,
          "Token Balance: ",
          token.balanceOf(account.address) / 10 ** token.decimals(),
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


def bond(token, bond):
    bond_price = bond.bondPrice()
    tx = bond.deposit(token.balanceOf(
        account.address), (bond_price + (bond_price * .005)), account.address, {"from": account})
    tx.wait(1)

    print("Token Balance: ", frax.balanceOf(account.address),
          "Percent Vested: ", bond.percentVestedFor(account.address))

# Check Bond Discounts


def check_discounts():
    discounts = []
    # Rome Price
    rome_price = solarRouter.getAmountsOut(
        1 * 10 ** rome.decimals(), [rome.address, frax.address], 25)[1]

    # Find discounts for each bond
    # Only consider bonds that are still for sale
    frax_discount = [
        (rome_price - fraxBonds.bondPriceInUSD()) / rome_price, frax, fraxBonds, [rome.address, frax.address]]
    if fraxBonds.maxPayout() > 0:
        discounts.append(frax_discount)

    wmovr_discount = [
        (rome_price - movrBonds.bondPriceInUSD()) / rome_price, wmovr, movrBonds, [rome.address, frax.address, wmovr.address]]
    if movrBonds.maxPayout() > 0:
        discounts.append(wmovr_discount)

    rome_frax_discount = [
        (rome_price - romeFraxBonds.bondPriceInUSD()) / rome_price, romeFrax, romeFraxBonds]
    if romeFraxBonds.maxPayout() > 0:
        discounts.append(rome_frax_discount)

    mim_discount = [
        (rome_price - mimBonds.bondPriceInUSD()) / rome_price, mim, mimBonds, [rome.address, frax.address, wmovr.address, mim.address]]
    if mimBonds.maxPayout() > 0:
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


def redeem_bonds():
    (payout_frax, vesting_frax, a, b) = fraxBonds.bondInfo(account.address)
    if payout_frax > 0:
        fraxBonds.redeem(account.address, True)

    (payout_mim, vesting_mim, c, d) = mimBonds.bondInfo(account.address)
    if payout_mim > 0:
        mimBonds.redeem(account.address, True)

    (payout_wmovr, vesting_wmovr, e, f) = movrBonds.bondInfo(account.address)
    if payout_wmovr > 0:
        movrBonds.redeem(account.address, True)

    (payout_rome_frax, vesting_rome_frax, g,
     h) = romeFraxBonds.bondInfo(account.address)
    if payout_rome_frax > 0:
        romeFraxBonds.redeem(account.address, True)

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
    solar_library,
)

account = accounts.add(config["wallets"]["from_key"])

rome_frax_pair = interface.ISolarPair("0x069C2065100b4D3D982383f7Ef3EcD1b95C05894")
(reserve1, reserve2, block) = rome_frax_pair.getReserves()
solar_router = interface.ISolarRouter02(solarRouter.address)


def main():
    # stake(rome.balanceOf(account.address))
    # swap_rome_to_mim(0.1 * 10 ** rome.decimals())
    path = [rome.address, frax.address, wmovr.address, mim.address]
    print(
        solar_library.getAmountsOut(
            "0x049581aEB6Fe262727f290165C29BDAB065a1B68",
            rome.balanceOf(account.address, path),
        )
    )


def stake(_amount):
    tx = staking_helper.stake(_amount, account.address, {"from": account})
    tx.wait(1)
    print(
        "Rome Balance: ",
        rome.balanceOf(account.address),
        "sRome Balance: ",
        sRome.balanceOf(account.address),
    )


def un_stake(_amount):
    sRome.approve(staking.address, sRome.balanceOf(account.address), {"from": account})
    tx = staking.unstake(_amount, True, {"from": account})
    tx.wait(1)
    print(
        "Rome Balance: ",
        rome.balanceOf(account.address),
        "sRome Balance: ",
        sRome.balanceOf(account.address),
    )


def swap_rome_to_mim(_amount):
    min_amount = (
        solar_router.quote(0.1 * 10 ** rome.decimals(), reserve2, reserve1)
        - 5 * 10 ** 18
    )

    path = [rome.address, frax.address, wmovr.address, mim.address]

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
        "Mim Balance: ",
        mim.balanceOf(account.address),
        "Rome Balance: ",
        rome.balanceOf(account.address),
    )

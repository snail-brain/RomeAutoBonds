from brownie import config, Contract, interface
from scripts.contracts import (
    bonds,
    staking,
    rome,
    frax,
    mim,
    wmovr,
    solarRouter,
    romeFrax,
)

solar_factory = interface.ISolarPair("0x069C2065100b4D3D982383f7Ef3EcD1b95C05894")
(reserve1, reserve2, block) = solar_factory.getReserves()
solar_router = interface.ISolarRouter02("0xAA30eF758139ae4a7f798112902Bf6d65612045f")

quote = solar_router.quote((1 * 10 ** 9), reserve2, reserve1)


print(quote / 10 ** 18)
print(type(rome.address))

# staking = Contract.from_abi("0x6f7D019502e17F1ef24AC67a260c65Dd23b759f1")


def main():
    pass

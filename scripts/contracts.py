from brownie import Contract
import json


with open("./ABIs/ROMEFRAXBondDepository.json") as json_file:
    a = json.load(json_file)
romeFraxBonds = Contract.from_abi(
    "ROMEFRAXBondDepository",
    "0x065588602bd7206B15f9630FDB2e81E4Ca51ad8A",
    a,
)

with open("./ABIs/FRAXBondDepository.json") as json_file:
    b = json.load(json_file)
fraxBonds = Contract.from_abi(
    "FRAXBondDepository", "0xE2F71c68db7ECC0c9A907AD2E40E2394c5CAc367", b
)

with open("./ABIs/MIMBondDepository.json") as json_file:
    c = json.load(json_file)
mimBonds = Contract.from_abi(
    "MIMBondDepository", "0x91a5184741FDc64f7507A7db6Aa3764a747f8089", c
)

with open("./ABIs/MOVRBondDepository.json") as json_file:
    d = json.load(json_file)
movrBonds = Contract.from_abi(
    "MOVRBondDepository", "0x54C6Afb58Aa21d11aEaFE6B199F9663e908345e4", d
)

with open("./ABIs/gOHMBondDepository.json") as json_file:
    gOHMBonds = Contract.from_abi(
        "gOHMBondDepository",
        "0xC82d354Cc96b5Cd0ee5B63569b5b51a2D3c5a895",
        json.load(json_file),
    )

with open("./ABIs/ROMEStaking.json") as json_file:
    f = json.load(json_file)
staking = Contract.from_abi(
    "ROMEStaking", "0x6f7D019502e17F1ef24AC67a260c65Dd23b759f1", f
)

with open("./ABIs/stakingHelper.json") as json_file:
    staking_helper = Contract.from_abi(
        "StakingHelper",
        "0x37f9A9436F5dB1ac9e346eAAB482f138DA0D8749",
        json.load(json_file),
    )

with open("./ABIs/Rome.json") as json_file:
    g = json.load(json_file)
rome = Contract.from_abi("Rome", "0x4a436073552044D5f2f49B176853ad3Ad473d9d6", g)

with open("./ABIs/sRome.json") as json_file:
    sRome = Contract.from_abi(
        "sRome", "0x89F52002E544585b42F8c7Cf557609CA4c8ce12A", json.load(json_file)
    )

with open("./ABIs/ROMEFRAX.json") as json_file:
    h = json.load(json_file)
romeFrax = Contract.from_abi(
    "RomeFrax", "0x069C2065100b4D3D982383f7Ef3EcD1b95C05894", h
)

with open("./ABIs/Frax.json") as json_file:
    frax = Contract.from_abi(
        "Frax", "0x1A93B23281CC1CDE4C4741353F3064709A16197d", json.load(json_file)
    )

with open("./ABIs/MIM.json") as json_file:
    mim = Contract.from_abi(
        "MIM", "0x0caE51e1032e8461f4806e26332c030E34De3aDb", json.load(json_file)
    )

with open("./ABIs/WMOVR.json") as json_file:
    wmovr = Contract.from_abi(
        "WMOVR", "0x98878B06940aE243284CA214f92Bb71a2b032B8A", json.load(json_file)
    )

with open("./ABIs/gOHM.json") as json_file:
    gohm = Contract.from_abi(
        "gOHM", "0x3bF21Ce864e58731B6f28D68d5928BcBEb0Ad172", json.load(json_file)
    )

with open("./ABIs/SolarRouter.json") as json_file:
    solarRouter = Contract.from_abi(
        "SolarRouter",
        "0xAA30eF758139ae4a7f798112902Bf6d65612045f",
        json.load(json_file),
    )

with open("./ABIs/distributor.json") as json_file:
    distributor = Contract.from_abi(
        "Distributor",
        "0x5BCF9C0A5fe546990248c5A3AD794409F471f28e",
        json.load(json_file),
    )


def main():
    pass

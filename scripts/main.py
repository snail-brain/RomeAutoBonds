from scripts.lib import *
from scripts.contracts import *
import json


# Find current block number
# Save next rebase block in text file? Or json?

with open("epochs.json", "r") as doody:
    x = json.load(doody)

saved_endBlock = x.get("next_rebase")
saved_next_action = x.get("make_plays")

(epochLength, epochNumber, endBlock, z) = staking.epoch()


def real_deal():
    best_deal = check_discounts()
    # Compare end-of-bond rome amount to default stake amount
    # Need staking reward rate


def main():
    if(saved_next_action > len(chain) - 1):
        redeem_bonds()
        stake(rome.balanceOf(account.address))
        # 3. Adjust json values

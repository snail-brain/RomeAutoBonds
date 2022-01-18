from scripts.lib import *
from scripts.contracts import *
import json

# Save next rebase block in text file? Or json?

with open("block_tracker.txt", "r") as txt:
    next_action_block = int(txt.read())

total_staked = staking.contractBalance()
(epoch_length, epoch_number, end_block, to_distribute) = staking.epoch()
staking_rate = to_distribute / total_staked


def real_deal():
    best_deal = check_discounts()
    print("Best deal: ", best_deal)
    total_rome = rome.balanceOf(account.address) + sRome.balanceOf(account.address)

    # Compare end-of-bond rome amount to default stake amount
    ending_rome_no_bond = rome_staked(total_rome, staking_rate)
    ending_rome_yes_bond = rome_bond_stake(
        total_rome + (total_rome * best_deal[0]), staking_rate
    )

    print("No bond: ", ending_rome_no_bond, "Yes bond: ", ending_rome_yes_bond)

    profit = 1 - (ending_rome_no_bond / ending_rome_yes_bond)
    if profit > 0.005:
        un_stake()
        if best_deal[1] == romeFrax:
            add_rome_frax_liq(rome.balance())
        else:
            make_swap(
                rome.balanceOf(account.address),
                best_deal[3],
                best_deal[1],
                {"from": account},
            )
            bond(best_deal[1], best_deal[2])


def if_end_is_near():
    if next_action_block < len(chain) - 1:
        redeem_bonds()
        stake()
        new_block = next_action_block + epoch_length

        with open("block_tracker.txt", "w") as txt:
            txt.write(str(new_block))


def main():
    if_end_is_near()
    real_deal()

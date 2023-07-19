from slither.slither import Slither


def is_visible(function):
    return function.visibility == "public" or function.visibility == "external"


# Instance Slither
slither = Slither("./token.sol")

# Get a reference to the contract
contract = slither.get_contract_from_name("BasicToken")

# Find all visible functions
visible_functions = [f for f in contract.functions if is_visible(f)]

from web3 import Web3
from typing import List, Dict, Optional, Union
import pydantic


class BytecodeCheckerResult(pydantic.BaseModel):
    contract_type: str
    eip_standard: bool
    missing_data: Optional[List[str]] = None


class Web3Provider:
    def __init__(self, mainnet: str):
        self.web3 = Web3(Web3.HTTPProvider(mainnet))

    def get_web3(self) -> Web3:
        return self.web3


class BytecodeChecker:
    def __init__(self, web3_provider: Web3Provider):
        self.web3_provider = web3_provider

    def check_bytecode_elements(self, address: str, check_list: List[str]) -> List[str]:
        web3 = self.web3_provider.get_web3()
        bytecode = web3.eth.get_code(address).hex()
        missing_elements = [
            element for element in check_list if element not in bytecode
        ]
        return missing_elements

    def check_contract_bytecode(
        self, address: str, check_list: List[str]
    ) -> Union[dict, None]:
        missing_elements = self.check_bytecode_elements(address, check_list)

        is_eip_standard = False
        if not missing_elements:
            is_eip_standard = True

        result = BytecodeCheckerResult(
            contract_type="ERC-20",
            eip_standard=is_eip_standard,
            missing_data=missing_elements,
        )

        return dict(result)

    # 4 bytes of keccak256("mint(address,uint256)")
    def check_bytecode_ismint(self, address: str) -> bool:
        web3 = self.web3_provider.get_web3()
        bytecode = web3.eth.get_code(address).hex()
        return "40c10f19" in bytecode

    # 4 bytes of keccak256("pause")
    def check_bytecode_ispause(self, address: str) -> bool:
        web3 = self.web3_provider.get_web3()
        bytecode = web3.eth.get_code(address).hex()
        return "8456cb59" in bytecode


def main():
    mainnet = "https://public-node-api.klaytnapi.com/v1/cypress"

    web3_provider = Web3Provider(mainnet)
    bytecode_checker = BytecodeChecker(web3_provider)

    check_list = [
        "a9059cbb",
        "095ea7b3",
        "70a08231",
        "23b872dd",
        "dd62ed3e",
        "18160ddd",
        "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
        "8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
    ]

    address = Web3.to_checksum_address("0x7f1712f846a69bf2a9dbc4d48f45f1d52ca32e28")

    result = bytecode_checker.check_contract_bytecode(address, check_list)
    result2 = bytecode_checker.check_bytecode_ismint(address)
    result3 = bytecode_checker.check_bytecode_ispause(address)

    print(result)
    print(result2)
    print(result3)


if __name__ == "__main__":
    main()

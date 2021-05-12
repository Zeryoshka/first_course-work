from .contract import Contract

def create_contracts(lots):
    '''
    function for create list of actual contracts
    '''
    contracts = []
    for lot in lots:
        if not lot.is_purchased:
            contracts.append(Contract(lot))
    return contracts

def sort_contarcts_for_players(contracts, players):
    '''
    function for create dict with player ids in keys and cintracts in value
    '''
    player_ids = list(map(lambda x: x.user.id, players))
    sorted_contracts = dict.fromkeys(player_ids, [])
    for contract in contracts:
        sorted_contracts[contract.player.user.id].append(contract)
    return sorted_contracts
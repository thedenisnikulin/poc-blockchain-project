import sys
import os
from typing import Tuple, Set
from PyInquirer import prompt
# local
from Blockchain import Blockchain
from Transaction import Transaction


def use_blockchain(blockchain: Blockchain, current_address: Tuple[str, int], peers: Set[Tuple[str, int]]):

    questions = {
        'main': {
            'type': 'list',
            'name': 'main',
            'message': f'Actions:',
            'choices': ['Refresh', 'Show peers', 'Show chain', 'New transaction', 'Mine block', 'Quit'],
        },
        'transaction': {
            'type': 'list',
            'name': 'transaction',
            'message': 'Whom to send?',
            'choices': [str(p) for p in peers]
        },
        'amount': {
            'type': 'input',
            'name': 'amount',
            'message': 'What amount would you like to send?'
        }
    }

    print(f'\nAddress: {current_address}')
    print(f'Balance: {blockchain.get_balance(current_address)}')
    answer = prompt(questions['main'])
    if answer['main'] == 'Refresh':
        clearconsole()
        return
    elif answer['main'] == 'Show peers':
        [print(str(p)) for p in peers]
        input('\nPress [ Enter ] to continue')
        clearconsole()
    # GET CHAIN
    elif answer['main'] == 'Show chain':
        print(blockchain.__str__)
        input('\nPress [ Enter ] to continue')
        clearconsole()
    # NEW TRANSACTION
    elif answer['main'] == 'New transaction':
        try:
            answer = prompt(questions['transaction'])
            recipient = answer['transaction'].split(', ')
            recipient = recipient[0][2: -1], int(recipient[1][0: -1])
            answer = prompt(questions['amount'])
            if int(answer['amount']) == 0:
                print('You can\'t send 0 coins')
            elif blockchain.get_balance(current_address) >= int(answer['amount']):
                t = Transaction(current_address, recipient, int(answer['amount']))
                blockchain.new_transaction(t)
            else:
                print('Not enough coins :(')
            input('\nPress [ Enter ] to continue')
            clearconsole()
        except IndexError:
            # This error raises when we get empty set
            print('No peers in the network :(')
            input('\nPress [ Enter ] to continue')
            clearconsole()
    # MINE BLOCK
    elif answer['main'] == 'Mine block':
        blockchain.add_block(current_address)
        clearconsole()
    # QUIT
    elif answer['main'] == 'Quit':
        sys.exit()


def clearconsole():
    """
    Clear the console. Thanks stackoverflow.
    """
    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('CLS')


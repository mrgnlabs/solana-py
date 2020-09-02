"""Unit tests for solana.system_program."""
import pytest

import solana.system_program as sp
from solana.account import Account
from solana.instruction import InstructionLayout, encode_data
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction


def test_decode_instruction_layout():
    """Test decode a transaction type."""
    create_account_params = sp.CreateAccountParams(
        from_pubkey=Account().public_key(),
        new_account_pubkey=Account().public_key(),
        lamports=123,
        space=1,
        program_id=PublicKey(1),
    )
    txn = sp.create_account(create_account_params)
    # pylint: disable=protected-access
    assert sp.SYSTEM_INSTRUCTION_LAYOUTS[sp._CREATE_IDX] == sp.decode_instruction_layout(txn.instructions[0])
    transfer_params = sp.TransferParams(
        from_pubkey=Account().public_key(), to_pubkey=Account().public_key(), lamports=123
    )
    txn = sp.transfer(transfer_params)
    # pylint: disable=protected-access
    assert sp.SYSTEM_INSTRUCTION_LAYOUTS[sp._TRANSFER_IDX] == sp.decode_instruction_layout(txn.instructions[0])

    # Invalid instruction
    with pytest.raises(ValueError):
        # pylint: disable=protected-access
        invalid_data = encode_data(InstructionLayout(idx=sp._ASSIGN_WITH_SEED_IDX + 1, fmt=""))
        txn.instructions[0] = TransactionInstruction(
            data=invalid_data, keys=txn.instructions[0].keys, program_id=txn.instructions[0].program_id
        )
        sp.decode_instruction_layout(txn.instructions[0])


def test_create_account():
    """Test creating a transaction for creat account."""
    params = sp.CreateAccountParams(
        from_pubkey=Account().public_key(),
        new_account_pubkey=Account().public_key(),
        lamports=123,
        space=1,
        program_id=PublicKey(1),
    )
    txn = sp.create_account(params)
    assert len(txn.instructions) == 1
    assert sp.decode_create_account(txn.instructions[0]) == params


def test_transfer():
    """Test creating a transaction for transfer."""
    params = sp.TransferParams(from_pubkey=Account().public_key(), to_pubkey=Account().public_key(), lamports=123)
    txn = sp.transfer(params)
    assert len(txn.instructions) == 1
    assert sp.decode_transfer(txn.instructions[0]) == params


def test_assign():
    """Test creating a transaction for transfer."""
    params = sp.AssignParams(
        account_pubkey=Account().public_key(),
        program_id=PublicKey(1),
    )
    txn = sp.assign(params)
    assert len(txn.instructions) == 1
    assert sp.decode_assign(txn.instructions[0]) == params
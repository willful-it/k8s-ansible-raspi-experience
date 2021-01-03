
import crud

import test_helper as h


def test_should_return_tokens_when_existing_in_the_db(test_db):
    number_of_tokens = 10
    h.create_tokens(test_db, number_of_tokens)

    tokens = crud.get_tokens(test_db)

    assert len(tokens) == number_of_tokens


def test_should_update_token_fields(test_db):
    h.create_tokens(test_db, 1)

    token = crud.get_tokens(test_db)[0]
    token.is_available = False

    updated_token = crud.update_token(test_db, token)
    db_token = crud.get_tokens(test_db)[0]

    assert not updated_token.is_available
    assert not db_token.is_available


def test_should_return_a_token_by_value(test_db):
    h.create_tokens(test_db)

    token = crud.get_tokens(test_db)[0]
    token_by_value = crud.get_token_by_value(test_db, token.value)

    assert token.id == token_by_value.id


def test_should_pop_a_token(test_db):
    h.create_tokens(test_db)

    token = crud.pop_token(test_db)
    db_token = crud.get_token_by_value(test_db, token.value)
    assert not db_token.is_available

from flask import make_response, abort
from config import db
from models import Users


def read_all():
    # Create the list of games from our data
    db_users = Users.query.all()
    print(db_users)
    list_users = []
    for user in db_users:
        user_id = user.user_id
        name = user.name
        date = user.date
        balance = user.balance
        country = user.country
        sex = user.sex
        data = {
            "user_id": user_id,
            "name": name,
            "date": date,
            "balance": balance,
            "country": country,
            "sex": sex
            }
        list_users.append(data)
    return list_users


def create(user):
    name = user.get("name")
    date = user.get("date")
    balance = user.get("balance")
    country = user.get("country")
    sex = user.get("sex")

    existing_user = (
        Users.query.filter(Users.name == name).one_or_none()
    )

    # Does such a game exist?
    # Yes
    if existing_user:
        abort(
            409,
            "User {0} already exist".format(name)
        )
    # No
    else:
        new_user = Users()
        new_user.name = name
        new_user.date = date
        new_user.balance = balance
        new_user.country = country
        new_user.sex = sex
        db.session.add(new_user)
        db.session.commit()


def read_one(received_user_id):
    user = Users.query.filter(
        Users.user_id == received_user_id
    ).one_or_none()
    if user:
        user_id = user.user_id
        name = user.name
        date = user.date
        balance = user.balance
        country = user.country
        sex = user.sex
        data = {
            "user_id": user_id,
            "name": name,
            "date": date,
            "balance": balance,
            "country": country,
            "sex": sex}

        return data
    else:
        abort(
            404,
            "User with {0} id not exist".format(received_user_id)
        )


def update(received_user_id, user):
    # Get the user requested from the db into session
    update_user = Users.query.filter(
        Users.user_id == received_user_id
    ).one_or_none()

    #
    name = user.get("name")
    date = user.get("date")
    balance = user.get("balance")
    country = user.get("country")
    sex = user.get("sex")

    existing_user = (
        Users.query.filter(Users.name == name)
        .filter(Users.date == date)
        .filter(Users.balance == balance)
        .filter(Users.country == country)
        .filter(Users.sex == sex)
        .one_or_none()
    )

    # Are we trying to find a user that does not exist?
    if update_user is None:
        abort(
            404,
            "User not found for Id: {received_game_id}".format(received_user_id),
        )

    # Would our update create a duplicate of another user already existing?
    elif (
        existing_user is not None and existing_user.user_id != received_user_id
    ):
        abort(
            409,
            "User {name} {date} {balance} {country} {sex} exists already".format(
                name=name,
                date=date,
                balance=balance,
                country=country,
                sex=sex
            ),
        )

    # Otherwise go ahead and update!
    else:
        update_user.name = name
        update_user.date = date
        update_user.balance = balance
        update_user.country = country
        update_user.sex = sex
        db.session.commit()
        return 200


def delete(received_user_id):
    # Get the user requested
    user = Users.query.filter(Users.user_id == received_user_id).one_or_none()

    # Did we find a user?
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return make_response(
            "User {user_id} deleted".format(user_id=received_user_id), 200
        )

    # Otherwise, nope, didn't find that user
    else:
        abort(
            404,
            "User not found for Id: {user_id}".format(user_id=received_user_id),
        )

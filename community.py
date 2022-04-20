from flask import make_response, abort
from config import db
from models import Community


def read_all():
    # Create the list of community from our data
    db_community = Community.query.order_by(Community.name).all()
    list_community = []
    for community in db_community:
        id = community.id
        name = community.name
        data = {"id": id, "name": name}
        list_community.append(data)
    return list_community


def create(community):
    name = community.get("name")
    existing_community = (
        Community.query.filter(Community.name == name).one_or_none()
    )

    # Does such a game exist?
    # Yes
    if existing_community:
        abort(
            409,
            "Community {0} already exist".format(name)
        )
    # No
    else:
        new_community = Community()
        new_community.name = name
        db.session.add(new_community)
        db.session.commit()


def read_one(received_community_name):
    community = Community.query.filter(
        Community.name == received_community_name
    ).one_or_none()
    if community:
        id = community.id
        name = community.name
        data = {
            "id": id,
            "name": name,
        }
        return data
    else:
        abort(
            404,
            "Community {0} not exist".format(received_community_name)
        )


def update(received_community_name, community):
    update_community = Community.query.filter(
        Community.name == received_community_name
    ).one_or_none()

    #
    name = community.get("name")

    existing_community = Community.query.filter(Community.name == name).one_or_none()


    # Are we trying to find a community that does not exist?
    if update_community is None:
        abort(
            404,
            "Community {0}  not found ".format(received_community_name),
        )

    # Would our update create a duplicate of another community already existing?
    elif (
        existing_community is not None and existing_community.name != received_community_name
    ):
        abort(
            409,
            "Community {name}  exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:
        update_community.name = name
        db.session.commit()
        return 200


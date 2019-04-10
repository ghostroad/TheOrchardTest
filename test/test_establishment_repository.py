from sqlalchemy import or_

from sietsema.models import Establishment, Rating, LatestRating


def test_filtering_by_latest_rating(repo):
    poor = Establishment(camis=3456, dba="Pho Lien", ratings=[
        Rating(grade="B", date="01/15/18"),
        Rating(grade="C", date="06/15/18"),
    ])

    okay = Establishment(camis=1234, dba="Brasserie Beaubien", cuisine="French", ratings=[
        Rating(grade="A", date="01/02/19"),
        Rating(grade="B", date="03/02/19"),
        Rating(grade="C", date="02/02/19")
    ])

    excellent = Establishment(camis=7654, dba="Trou de Beigne", cuisine="French", ratings=[
        Rating(grade="A", date="04/02/19"),
        Rating(grade="C", date="02/02/19")
    ])

    repo.save(poor, okay, excellent)

    okay_establishments = repo.latest_ratings_query().filter(
        or_(LatestRating.grade == "B", LatestRating.grade == "A")
    ).all()

    assert (set(okay_establishments) == {okay, excellent})
    assert (set(establishment.latest_rating.grade for establishment in okay_establishments) == {"A", "B"})

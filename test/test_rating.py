from datetime import date

from sietsema.models import Establishment, Rating


def test_creation(repo):
    repo.save(Establishment(camis=1234, dba="Brasserie Beaubien", ratings=[Rating(grade="A", date="01/02/19")]))

    ratings = Rating.query.all()
    assert (len(ratings) == 1)
    rating = ratings[0]
    assert (rating.date == date(2019, 1, 2))
    assert (rating.grade == "A")

class Driver:
    def __init__(self, car, user_id):
        self.car = car
        self.user_id = user_id

    def toDict(self):
        return {'car': self.car, 'user_id': self.user_id}


class DriversRating:
    def __init__(self, driver_entity_user_id, ratings_id):
        self.driver_entity_user_id = driver_entity_user_id
        self.ratings_id = ratings_id

    def toDict(self):
        return {'driver_entity_user_id': self.driver_entity_user_id, 'ratings_id': self.ratings_id}


class DriverRatings:
    def __init__(self, id, description, stars, user_id):
        self.id = id
        self.description = description
        self.stars = stars
        self.user_id = user_id

    def toDict(self):
        return {'id': self.id, 'description': self.description, 'stars': self.stars, 'user_id': self.user_id}

class Image:
    def __init__(self, id, oid):
        self.id = id
        self.oid = oid
    
    def __repr__(self):
        return self.id + ', ' + self.oid 

    def __str__(self):
        return self.id + ', ' + self.oid 

    def toDict(self):
        return {'id': self.id, 'oid': self.oid}

class Menu:
    def __init__(self, id, name, imageId, allergens, price, description):
        self.id = id
        self.name = name
        self.imageId = imageId
        self.allergens = allergens
        self.price = price
        self.description = description

    def __repr__(self):
        return self.id + ', ' + self.name + ', ' + self.imageId + ', ' + str(self.allergens) + ', $' + str(self.price) + ', ' \
            + self.description + ', ' + self.configurations

    def __str__(self):
        return self.id + ', ' + self.name + ', ' + self.imageId + ', ' + str(self.allergens) + ', $' + str(self.price) + ', ' \
            + self.description + ', ' + self.configurations
    
    def toDict(self):
        return {'id': self.id, 'allergens': self.allergens, 'description': self.description, 'image_id':  self.imageId, 'name':self.name, 'price': self.price}

class Promotion:
    def __init__(self, id, condition, discount, name):
        self.id = id
        self.condition = condition
        self.discount = discount
        self.name = name

    def __repr__(self):
        return self.condition + ', ' + str(self.discount) + ', ' + self.name

    def __str__(self):
        return self.condition + ', ' + str(self.discount)+ ', ' + self.name

    def toDict(self):
        return {'id': self.id, 'condition': self.condition, 'discount': self.discount, 'name': self.name}

class Rating:
    def __init__(self, id, imageId, stars, description, user_id):
        self.id = id
        self.imageId = imageId
        self.stars = stars
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return self.imageId + ', ' + str(self.stars) + ', ' + self.description

    def __str__(self):
        return self.imageId + ', ' + str(self.stars) + ', ' + self.description

    def toDict(self):
        return {'id': self.id, 'image_id': self.imageId, 'stars': self.stars, 'description': self.description, 'user_id': self.user_id}

class Hours:
    def __init__(self, day):
        self.day = day
    
    def toDict(self):
        if len(self.day) < 7:
            raise Exception ('[Error] incomplete days')
    
        return {'mon': self.day[0], 'tue': self.day[1], 'wed': self.day[2], 'thu': self.day[3], 'fri': self.day[4], 'sat': self.day[5], 'sun': self.day[6]}


class Restaurant:
    def __init__(self, id, address, averageRating, averageTime, backgroundId, 
                 geolocation, hours, iconId, name, ratings):
        self.id = id
        self.address = address
        self.averageRating = averageRating
        self.averageTime = averageTime
        self.backgroundId = backgroundId
        self.geolocation = geolocation
        self.hours = hours
        self.iconId = iconId
        self.name = name
        self.ratings = ratings

    def toDict(self):
        return {
            'id': self.id, 
            'address': self.address,
            'average_rating': self.averageRating,
            'average_time': self.averageTime,
            'background_id': self.backgroundId,
            'geolocation': self.geolocation,
            **self.hours,
            'icon_id': self.iconId,
            'name': self.name,
            'price_rating': self.ratings,
        }

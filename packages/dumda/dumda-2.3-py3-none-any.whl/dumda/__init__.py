from . import cities
from . import names
from . import phones
from . import emails
from . import text

class Person(object):
    def __init__(self, country: str ="united states", sex: str = None):
        self.name = names.Names().get_fullnames(n = 1, sex=sex)
        self.location = cities.Cities().get_random_cities(n=1, country=country)
        self.email = emails.generate_email(self.name)
        self.phone = phones.generate_number()

    def get_json(self):
        """
        returns a Json Object of the generated
        Person object as an alternative to manually working
        with the Python object
        :return: JSON Object
        """
        import json
        response = json.dumps({
            'full_name': self.name,
            'location': self.location,
            'email': self.email,
            'phone': self.phone
        })

        return json.loads(response)

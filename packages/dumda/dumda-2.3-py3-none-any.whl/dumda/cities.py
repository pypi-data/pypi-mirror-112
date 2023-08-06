class Cities:
    def __init__(self):
        self.cities = self.get_all()

    def __get_cities(self):
        import os
        import csv
        path = os.path.join(os.path.dirname(__file__), "world_cities.csv")
        f = open(path, 'r', encoding='utf-8')
        reader = csv.DictReader(f)
        return reader

    def get_all(self):
        """
        return list of all cities
        :return:
        """
        return [city['name'].rstrip() for city in list(self.__get_cities())]

    def get_random_cities(self, n, country: str = None):
        """
        returns a list of random cities in the given amount
        :param country:
        :param n: int, number of desired cities
        :return: list
        """
        from random import choice
        cities = list()

        if country:
            full_list = self.get_by_country(country)
        else:
            full_list = self.get_all()

        # Iterate through the given number
        for _ in range(n):
            city = choice(full_list)

            cities.append(city)
        if n == 1:
            return cities[0]
        return cities

    def get_by_country(self, name):
        """
        returns a list of cities based on a given country
        Note: There is only 'United Kingdom' not England
        :param name: str, country name
        :return: list
        """
        return [city['name'] for city in self.__get_cities()
                if city['country'].lower() == name.lower()]

    def get_by_letter(self, letter):
        """
        returns a list of cities based on a given letter
        :param letter: chr
        :return: list
        """
        cities = list()

        for city in self.get_all():
            if city[0].lower() == letter.lower():
                cities.append(city)

        return cities

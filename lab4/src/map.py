from typing import List
from .country import Country
from .city import City


class Map:
    def __init__(self, countries_data):
        self.countries = []
        self.grid: List[List[City]] = [[None] * (10 + 2) for _ in range((10 + 2))]
        self.__initialize_grid(countries_data)
        self.__validate_foreign_neighbours()

    def simulate_euro_diffusion(self) -> None:
        if len(self.countries) == 1:
            self.countries[0].day_of_full = 0
            return

        full = False
        day = 1
        while not full:
            for x in range(10 + 1):
                for y in range(10 + 1):
                    if self.grid[x][y] is not None:
                        city = self.grid[x][y]
                        city.transfer_to_neighbours()

            for x in range(10 + 1):
                for y in range(10 + 1):
                    if self.grid[x][y] is not None:
                        city = self.grid[x][y]
                        city.finalize_balance_per_day()

            full = True
            for country in self.countries:
                country.check_fullness(day)
                if country.full is False:
                    full = False

            day += 1

        self.countries.sort()

    def __initialize_grid(self, countries_data) -> None:
        for country_data in countries_data:
            country = Country(country_data["name"])
            for x in range(country_data["ll"]["x"], country_data["ur"]["x"] + 1):
                for y in range(country_data["ll"]["y"], country_data["ur"]["y"] + 1):
                    city = City(country.name, countries_data, x, y)
                    self.grid[x][y] = city
                    country.append_city(city)
            self.countries.append(country)

        for row in self.grid:
            for city in row:
                if city is not None:
                    neighbours_list = self.__get_neighbours(city.x, city.y)
                    city.set_neighbours(neighbours_list)

    def __get_neighbours(self, x, y) -> List[City]:
        neighbours = []
        if self.grid[x][y + 1] is not None:
            neighbours.append(self.grid[x][y + 1])
        if self.grid[x][y] is not None:
            neighbours.append(self.grid[x][y - 1])
        if self.grid[x + 1][y] is not None:
            neighbours.append(self.grid[x + 1][y])
        if self.grid[x - 1][y] is not None:
            neighbours.append(self.grid[x - 1][y])
        return neighbours

    def __validate_foreign_neighbours(self) -> None:
        if len(self.countries) <= 1:
            return

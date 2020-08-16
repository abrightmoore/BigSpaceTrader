class Produce:
    def __init__(self):
        self.products = []

    def get_product_tables(self):
        products = {
            "Agricultural" : {
                "Grains" : { "price" : 5, },
                "Livestock" : { "price" : 20 },
                "Beverages" : { "price" : 15 },
                "Crops" : { "price" : 10 },
                "Fabric" : {"price" : 30 },
                "Art" : { "price" : 300 },
                "Skilled Labour" : {"price" : 500 },
                "Artifacts" : { "price" : 1000 }
            },

            "Industrial" : {
                "Fuel" : { "price" : 20 },
                "Minerals" : { "price" : 30 },
                "Alloys" : { "price" : 40 },
                "Computers" : { "price": 50 },
                "Generators": {"price": 150},
                "Engineering": {"price": 175},
                "Weapons" : { "price" : 200 },
                "Habitats" : { "price" : 300 },
                "Professional": {"price": 800},
            }
        }

        return products


import json5



from src.Logger.python import Logger

class BFAV2CP:
    inputContent: dict
    inputManifest: dict

    outputContent: dict = {
        "Format": "1.29.5",
        "Changes": []
    }
    outputManifest: dict

    assets: list = []

    def __init__(self, _logger: Logger) -> None:
        self.inputContent = json5.load(
            open('input/content.json'))
        self.inputManifest = json5.load(
            open('input/manifest.json'))
        
        self.outputManifest = self.inputManifest
        self.outputManifest['ContentPackFor']['UniqueID'] = 'Pathoschild.ContentPatcher'
        self.outputManifest['Author'] += ' ~ BFAV2CP'

        self.logger = _logger

        for animal in self.inputContent['Categories']:
            self.logger.success(animal['Category'])

            shop = animal['AnimalShop']
            buildings: list = animal['Buildings']

            self.assets.append({
                "animal": animal,
                "path": shop['Icon'],
                "id": "shopIcon"

            })

            
            for type in animal['Types']:
                self.assets.append({
                    "animal": type,
                    "path": type['Sprites']['Adult'],
                    "id": "adultSprite",
                })
                self.assets.append({
                    "animal": type,
                    "path": type['Sprites']['Baby'],
                    "id": "babySprite",
                })
                if 'ReadyForHarvest' in type['Sprites']:
                    self.assets.append({
                        "animal": type,
                        "path": type['Sprites']['ReadyForHarvest']
                    })
                parsed = self.splitAnimalData(type['Data'])

                newAnimal = {
                    'key': type['Type'],
                    'value': {
                        'DisplayName': parsed['displayType'],
                        'House': parsed['buildingType'],
                        'Gender': 'MaleOrFemale',
                        'PurchasePrice': shop['Price'],
                        'ShopTexture': f'Animals/{type["Type"]} Icon',
                        'ShopSourceRect': {
                            'X': 0,
                            'Y': '0',
                            'Wdith': '32',
                            'Height': '16',
                        },
                        'RequiredBuilding': parsed['buildingType'],
                        'ShopDisplayName': shop['Name'],
                        'ShopDescription': shop['Description'],
                        'DaysToMature': parsed['daysToMature'],
                        'ProduceItemIds': [
                            {
                                'Id': 'Default',
                                'Condition': None,
                                'MinimumFriendship': 0,
                                'ItemId': parsed['defaultProduceIndex']
                            }
                        ],
                        'DeluxeProduceItemIds': [
                            {
                                'Id': 'Default',
                                'Condition': None,
                                'MinimumFriendship': 0,
                                'ItemId': parsed['deluxeProduceIndex']
                            }
                        ],
                        'DaysToProduce': parsed['daysToProduce'],
                        'HarvestType': [
                            'DropOvernight',
                            'HarvestWithTool',
                            None
                        ][parsed['harvestType']],
                        'HarvestTool': parsed['harvestTool'],
                        'Sound': parsed['sound'],
                        'BabySound': parsed['sound'],



                    }
                }

                self.logger.success(newAnimal)

    def splitAnimalData(type: str, data: str) -> dict:
        _parts = data.split('/')

        return {
            'daysToProduce': _parts[0],
            'daysToMature': _parts[1],
            'defaultProduceIndex': _parts[2],
            'deluxeProduceIndex': _parts[3],
            'sound': _parts[4],
            '_frontBackBounding': _parts[5:9],
            '_sideBounding': _parts[9:12],
            'harvestType': int(_parts[13]),
            'changeTextureWhenItemReady': _parts[14] == 'true',
            'buildingType': _parts[15],
            'frontBackSpriteSize': _parts[16:17],
            'sideSpriteSize': _parts[18:19],
            'fullnessDrain': _parts[20],
            'happinessDrain': _parts[21],
            'harvestTool': _parts[22],
            'meatIndex': _parts[23],
            'sellPrice': _parts[24],
            'displayType': _parts[25],
            'displayBuilding': _parts[26],

            'type': type
        }

        


        


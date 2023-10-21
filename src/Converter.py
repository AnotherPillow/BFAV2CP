import json5, json, shutil, os

from src.Logger.python import Logger

class BFAV2CP:
    inputContent: dict
    inputManifest: dict

    outputContent: dict = {
        "Format": "1.29.5",
        "Changes": []
    }
    outputManifest: dict
    uid: str

    assets: list = []

    def __init__(self, _logger: Logger) -> None:
        self.inputContent = json5.load(
            open('input/content.json'))
        self.inputManifest = json5.load(
            open('input/manifest.json'))
        
        self.outputManifest = self.inputManifest
        self.outputManifest['ContentPackFor']['UniqueID'] = 'Pathoschild.ContentPatcher'
        self.outputManifest['Author'] += ' ~ BFAV2CP'

        self.uid = self.outputManifest['UniqueID']

    

        self.logger = _logger

        for animal in self.inputContent['Categories']:
            self.logger.success(animal['Category'])

            shop = animal['AnimalShop']
            buildings: list = animal['Buildings']

            self.assets.append({
                "animal": animal['Category'],
                "trueAnimal": animal['Category'],
                "path": shop['Icon'],
                "target_path": f'Animals/{self.uid}-{animal["Category"]} Icon',
                "id": "shopIcon"
            })

            
            for type in animal['Types']:
                self.assets.append({
                    "animal": type['Type'],
                    "trueAnimal": animal['Category'],
                    "path": type['Sprites']['Adult'],
                    "id": "adultSprite",
                })
                self.assets.append({
                    "animal": type['Type'],
                    "trueAnimal": animal['Category'],
                    "path": type['Sprites']['Baby'],
                    "id": "babySprite",
                })
                self.assets.append({
                    "animal": type['Type'],
                    "trueAnimal": animal['Category'],
                    "path": shop['Icon'],
                    "target_path": f'Animals/{self.uid}-{type["Type"]} Icon',
                    "id": "shopIcon"
                })
                
                if 'ReadyForHarvest' in type['Sprites']:
                    self.assets.append({
                        "animal": type['Type'],
                        "trueAnimal": animal['Category'],
                        "path": type['Sprites']['ReadyForHarvest'],
                        "id": "harvestSprite"
                    })
                parsed = self.splitAnimalData(type['Data'])

                newAnimal = {
                    'key': type['Type'],
                    'value': {
                        'DisplayName': f"{parsed['displayType']}",
                        'House': parsed['buildingType'],
                        'Gender': 'MaleOrFemale',
                        'PurchasePrice': shop['Price'],
                        'ShopTexture': f'Animals/{self.uid}-{type["Type"]} Icon',
                        'ShopSourceRect': {
                            'X': 0,
                            'Y': 0,
                            'Width': 32,
                            'Height': 16,
                        },
                        'RequiredBuilding': parsed['buildingType'],
                        # 'ShopDisplayName': shop['Name'],
                        'ShopDisplayName': f"{parsed['displayType']}",
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
                        'Texture': f'Animals/{self.uid}-{type["Type"]}',
                        'HarvestedTexture': f'Animals/{self.uid}-{type["Type"]} Harvested',
                        'BabyTexture': f'Animals/{self.uid}-{{type["Type"]} Baby',
                        'SpriteWidth': parsed['frontBackSpriteSize'][0],
                        'SpriteHeight': parsed['frontBackSpriteSize'][1],
                        # 'Skins': 'TODO: make skins use types, not seperate animals',
                        'ShowInSummitCredits': True, # this is on because yes.
                    }
                }

                self.outputContent['Changes'].append({
                    'LogName': f'Load data for {animal["Category"]} ({type["Type"]})',
                    'Action': 'EditData',
                    'Target': 'Data/FarmAnimals',
                    'Entries': {
                        newAnimal['key']: newAnimal['value']
                    }
                })

                

                # self.logger.info(self.outputContent)

                # self.logger.success(newAnimal)

        for asset in self.assets:
            self.logger.info(asset)

            id = asset['id']

            if id == 'adultSprite':
                self.outputContent['Changes'].append({
                    'LogName': f'Load {id} for {asset["animal"]}',
                    'Action': 'Load',
                    'Target': f'Animals/{self.uid}-{asset["animal"]}',
                    'FromFile': asset['path']
                })
            elif id == 'babySprite':
                self.outputContent['Changes'].append({
                    'LogName': f'Load {id} for {asset["animal"]}',
                    'Action': 'Load',
                    'Target': f'Animals/{self.uid}-{asset["animal"]} Baby',
                    'FromFile': asset['path']
                })
            elif id == 'harvestsprite':
                self.outputContent['Changes'].append({
                    'LogName': f'Load {id} for {asset["animal"]}',
                    'Action': 'Load',
                    'Target': f'Animals/{self.uid}-{asset["animal"]} Harvested',
                    'FromFile': asset['path']
                })
            elif id == 'shopIcon':
                tpath = asset['target_path']
                self.outputContent['Changes'].append({
                    'LogName': f'Load {id} for {asset["animal"]}',
                    'Action': 'Load',
                    # 'Target': f'Animals/{asset["trueAnimal"]} Icon',
                    'Target': tpath,
                    'FromFile': asset['path']
                })
            


        with open('output/content.json', 'w', encoding='utf-8') as f:
            json.dump( self.outputContent, f, indent=4 )
            f.close()        
            
        with open('output/manifest.json', 'w', encoding='utf-8') as f:
            json.dump( self.outputManifest, f, indent=4 )
            f.close()

        if os.path.exists('output/assets'):
            shutil.rmtree('output/assets')
        
        shutil.copytree('input/assets', 'output/assets')
            

            


    def splitAnimalData(type: str, data: str) -> dict:
        _parts = data.split('/')

        # print(_parts[16])
        # print(_parts[17])

        return {
            'daysToProduce': _parts[0],
            'daysToMature': _parts[1],
            'defaultProduceIndex': _parts[2],
            'deluxeProduceIndex': _parts[3],
            'sound': _parts[4],
            '_frontBackBounding': _parts[5:10],
            '_sideBounding': _parts[9:13],
            'harvestType': int(_parts[13]),
            'changeTextureWhenItemReady': _parts[14] == 'true',
            'buildingType': _parts[15],
            'frontBackSpriteSize': _parts[16:18],
            'sideSpriteSize': _parts[18:20],
            'fullnessDrain': _parts[20],
            'happinessDrain': _parts[21],
            'harvestTool': _parts[22],
            'meatIndex': _parts[23],
            'sellPrice': _parts[24],
            'displayType': _parts[25],
            'displayBuilding': _parts[26],

            'type': type
        }

        

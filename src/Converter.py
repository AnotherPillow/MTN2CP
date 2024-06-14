import json5, shutil, os, json, urllib.request
from .xnb import *

from .Logger import logger

def addTbinIfNeeded(s: str) -> str: 
    if not s.endswith('.tbin'): s += '.tbin'
    return s

def q(v, d):
    if v == None: return d
    return v

class Converter:
    manifest: dict = {}
    farmType: dict = {}
    content: dict = {
        "Format": "2.0",
        "Changes": []
    }
    
    def __init__(self):
        self.manifest = json5.load(open('input/manifest.json', encoding='utf8'))
        self.farmType = json5.load(open('input/farmType.json', encoding='utf8'))

        if os.path.exists('output'):
            shutil.rmtree('output')

        downloadXNBCLI()
        chmodIfNeeded(xnbcliExecutable)
        logger.info('Extracting XNBs (if any)')
        extractFilesInADirectory('input')

        shutil.copytree('input', 'output')

        

    def convert(self):
        farmID = f"{self.manifest['UniqueID']}.{self.farmType['ID']}"
        farmMapsFileName = f"Mod_Farm_{self.farmType['farmMapFile']}"

        self.content['Changes'].append({
            "LogName": "load in map file for farm",
            "Action": "Load",
            "Target": "Maps/" + farmMapsFileName,
            "FromFile": addTbinIfNeeded(self.farmType['farmMapFile'])
        })

        iconSourcePath = self.farmType.get('Icon')
        iconContentPath = f"LooseSprites/Mod_Farm_Icon_{self.manifest['UniqueID']}"

        if iconSourcePath:
            self.content['Changes'].append({
                "LogName": "load in icon for farm",
                "Action": "Load",
                "Target": iconContentPath,
                "FromFile": iconSourcePath,
            })

        self.content['Changes'].append({
			"LogName": "Load in UI Strings",
            "Action": "EditData",
            "Target": "Strings/UI",
            "Entries": {
                f"{self.manifest['UniqueID']}_Farm_Description": self.farmType['Description']
            },
        })
        
        self.content['Changes'].append({
			"LogName": "Set up custom farm type",
            "Action": "EditData",
            "Target": "Data/AdditionalFarms",
            "Entries": {
                farmID: {
                    "ID": farmID,
                    "TooltipStringPath": f"Strings/UI:{self.manifest['UniqueID']}_Farm_Description",
                    "MapName": farmMapsFileName,
                    "IconTexture": iconContentPath if iconSourcePath else None,
                    "SpawnMonstersByDefault": self.farmType.get('spawnMonstersAtNight') or False
                }
            },
        })

        if q(q(self.farmType.get('farmHouse'), {}).get('pointOfInteraction'), None):
            house = self.farmType['farmHouse']['pointOfInteraction']
            fp = 'Maps/' + farmMapsFileName
            
            self.content['Changes'].append({
                "LogName": "set up farmhouse location for farm",
                "Action": "EditMap",
                "Target": fp,
                "MapProperties": {
                    "FarmHouseEntry": f"{house['x']} {house['y']}"
                }
            })
        if q(q(self.farmType.get('grandpaShrine'), {}).get('pointOfInteraction'), None):
            shrine = self.farmType['grandpaShrine']['pointOfInteraction']
            fp = 'Maps/' + farmMapsFileName
            
            self.content['Changes'].append({
                "LogName": "set up grandpaShrine location for farm",
                "Action": "EditMap",
                "Target": fp,
                "MapProperties": {
                    "GrandpaShrineLocation": f"{shrine['x']} {shrine['y']}"
                }
            })
        if q(q(self.farmType.get('greenHouse'), {}).get('coordinates'), None):
            greenhouse = self.farmType['greenHouse']['coordinates']
            fp = 'Maps/' + farmMapsFileName
            
            self.content['Changes'].append({
                "LogName": "set up greenHouse location for farm",
                "Action": "EditMap",
                "Target": fp,
                "MapProperties": {
                    "GreenhouseLocation": f"{greenhouse['x']} {greenhouse['y'] + 4}"
                }
            })
        if q(q(self.farmType.get('mailBox'), {}).get('pointOfInteraction'), None):
            box = self.farmType['mailBox']['pointOfInteraction']
            fp = 'Maps/' + farmMapsFileName
            
            self.content['Changes'].append({
                "LogName": "set up mailBox location for farm",
                "Action": "EditMap",
                "Target": fp,
                "MapProperties": {
                    "MailboxLocation": f"{box['x']} {box['y']}"
                }
            })
        if q(q(self.farmType.get('farmCave'), {}).get('pointOfInteraction'), None):
            cave = self.farmType['farmCave']['pointOfInteraction']
            fp = 'Maps/' + farmMapsFileName
            
            self.content['Changes'].append({
                "LogName": "set up farmCave location for farm",
                "Action": "EditMap",
                "Target": fp,
                "MapProperties": {
                    "FarmCaveEntry": f"{cave['x']} {cave['y']}"
                }
            })
        if q(q(self.farmType.get('petWaterBowl'), {}).get('pointOfInteraction'), None):
            bowl = self.farmType['petWaterBowl']['pointOfInteraction']
            fp = 'Maps/' + farmMapsFileName
            
            self.content['Changes'].append({
                "LogName": "set up petWaterBowl location for farm",
                "Action": "EditMap",
                "Target": fp,
                "MapProperties": {
                    "PetBowlLocation": f"{bowl['x'] - 1} {bowl['y']}"
                }
            })
        if q(q(self.farmType.get('rabbitStatue'), {}).get('pointOfInteraction'), None):
            statue = self.farmType['rabbitStatue']['pointOfInteraction']
            fp = 'Maps/' + farmMapsFileName
            
            self.content['Changes'].append({
                "LogName": "set up rabbitStatue location for farm",
                "Action": "EditMap",
                "Target": fp,
                "MapProperties": {
                    "WarpTotemEntry": f"{statue['x']} {statue['y']}"
                }
            })
        if q(q(self.farmType.get('shippingBin'), {}).get('pointOfInteraction'), None):
            bin = self.farmType['shippingBin']['pointOfInteraction']
            fp = 'Maps/' + farmMapsFileName
            x = bin['x']
            y = bin['y']

            self.content['Changes'].append({
                "LogName": "set up shippingBin location for farm",
                "Action": "EditMap",
                "Target": fp,
                "MapProperties": {
                    "ShippingBinLocation": f"{x} {y + 1}"
                }
            })
            
            buildings = [
                [x, y],
                [x + 1, y],
                [x + 1, y + 1],
                [x, y + 1],
            ]
            tilePatch = {
                "Action": "EditMap",
                "Target": fp,
                "MapTiles": []
            }
            for tile in buildings:
                mt = {
                    "Position": { "X": tile[0], "Y": tile[1]},
                    "Layer": "Buildings",
                    "Remove": True,
                }
                tilePatch['MapTiles'].append(mt)
            self.content['Changes'].append(tilePatch)


        self.translateManifest()
        self.save()

    def translateManifest(self):
        logger.info('Updating manifest..')
        self.manifest['UniqueID'] += '.CP'
        self.manifest['Author'] += ' ~ MTN2CP'
        
        self.manifest['ContentPackFor']['UniqueID'] = 'Pathoschild.ContentPatcher'
        
        
        if 'Dependencies' in self.manifest:
            self.manifest['Dependencies'] = \
                [mod for mod in self.manifest['Dependencies'] if mod['UniqueID'] not in ['SgtPickles.MTN']]
        
    def save(self):
        
        with open('output/manifest.json', 'w') as f:
            json.dump(self.manifest, f, indent=4)
        
        with open('output/content.json', 'w') as f:
            json.dump(self.content, f, indent=4)

        os.remove('output/farmType.json')
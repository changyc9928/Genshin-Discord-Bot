import asyncio

from query_graphql import query_artifact_domains, query_weapon_materials_book


class Domains:
    leylines = {
        "Blossom of Revelation": "Character EXP Materials",
        "Blossom of Wealth": "Mora"
    }
    weapon_domains = {}
    talent_domains = {}
    artifact_domains = {}
    trounce_domains = {
        "Wolf of the North Challenge": "Andrius (Lupus Boreas), Dominator of Wolves",
        "Beneath the Dragon-Queller": "Azhdaha, Sealed Lord of Vishaps",
        "Enter the Golden House": "Childe, Eleventh of the Fatui Harbingers",
        "Narukami Island: Tenshukaku": "La Signora (Rosalyne-Kruzchka Lohefalter), The Fair Lady"
    }
    world_bosses = {
        "Anemo Hypostasis": None,
        "Electro Hypostasis": None,
        "Cryo Regisvine": None,
        "Cryo Hypostasis": None,
        "Oceanid": None,
        "Pyro Regisvine": None,
        "Geo Hypostasis": None,
        "Primo Geovishap": None,
        "Maguu Kenki": None,
        "Pyro Hypostasis": None,
        "Perpetual Mechanical Array": None,
        "Hydro Hypostasis": None,
        "Thunder Manifestation": None,
        "Golden Wolflord": None
    }



    @staticmethod
    async def initialize():
        Domains.artifact_domains = await query_artifact_domains()
        tuple = await query_weapon_materials_book()
        Domains.weapon_domains = tuple[0]
        Domains.talent_domains = tuple[1]
        Domains.domains = {
            "Ley Line Outcrops": Domains.leylines,
            "Weapon Ascension Materials": Domains.weapon_domains,
            "Talent Books": Domains.talent_domains,
            "Artifacts": Domains.artifact_domains,
            "Trounce Domains": Domains.trounce_domains,
            "World Bosses": Domains.world_bosses
        }

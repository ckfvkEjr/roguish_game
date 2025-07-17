from game.config import TILE_SIZE

item_types = {
        "it1" : {
            "name" : "it1",
            "hp" : 10,
            "max_hp" : 10,
            "speed" : 0,
            "attack_speed" : 0,
            "attack_range" : 0,
            "damage" : 0,
            "size" : 0,
            "attack_type" : None,
            "texture" : "None"
        },
    "it2" : {
        "name" : "it2",
        "hp" : 0,
        "max_hp" : 0,
        "speed" : 0,
        "attack_speed" : 0.5,
        "attack_range" : 0,
        "damage" : 1,
        "size" : 0,
        "attack_type" : None,
        "texture" : "None"
    },
    "it3" : {
        "name" : "it3",
        "hp" : None,
        "max_hp" : None,
        "speed" : 0.125*(TILE_SIZE/50),
        "attack_speed" : None,
        "attack_range" : 0.5,
        "damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "None"
    },
}
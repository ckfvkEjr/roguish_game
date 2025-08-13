from game.config import TILE_SIZE

item_types = {
    "it1" : {
        "name" : "heart",
        "hp" : 10,
        "max_hp" : 10,
        "speed" : 0,
        "attack_speed" : 0,
        "attack_range" : 0,
        "damage" : 0,
        "max_damage" : 0,
        "min_damage" : 0,
        "size" : 0,
        "attack_type" : None,
        "texture" : "assets/item/heart.png"
    },
    "it2" : {
        "name" : "+1",
        "hp" : 0,
        "max_hp" : 0,
        "speed" : 0,
        "attack_speed" : 0.5,
        "attack_range" : 0,
        "damage" : 1,
        "max_damage" : 0,
        "min_damage" : 0,
        "size" : 0,
        "attack_type" : None,
        "texture" : "None"
    },
    "it3" : {
        "name" : "Ruler",
        "hp" : None,
        "max_hp" : None,
        "speed" : 0.125*(TILE_SIZE/50),
        "attack_speed" : None,
        "attack_range" : 0.5,
        "damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/ruler.png"
    },
}
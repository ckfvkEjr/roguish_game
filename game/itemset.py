from game.config import TILE_SIZE

item_types = {
    "it1" : {
        "name" : "heart",
        "hp" : 30,
        "max_hp" : 30,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/heart.png"
    },
    "it2" : {
        "name" : "+1",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : 3,
        "max_damage" : 3,
        "min_damage" : 1,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/+1.png"
    },
    "it3" : {
        "name" : "Ruler",
        "hp" : None,
        "max_hp" : None,
        "speed" : 0.125*(TILE_SIZE/50),
        "attack_speed" : None,
        "attack_range" : 0.5,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/ruler.png"
    },
    "it4" : {
        "name" : "s",
        "hp" : None,
        "max_hp" : None,
        "speed" : (TILE_SIZE/50)*0.5,
        "attack_speed" : 0.9,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/hand_clock.png"
    },
    "it5" : {
        "name" : "x^2",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "sqauare_min_max_damage" : 1,
        "texture" : "assets/item/x^2.png"
    },
    "it6" : {
        "name" : "wa!_palra",
        "hp" : None,
        "max_hp" : None,
        "speed" : (TILE_SIZE/50),
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/spppeeeed.png"
    },
    "it7" : {
        "name" : "heavy",
        "hp" : None,
        "max_hp" : None,
        "speed" : -((TILE_SIZE/50)*0.5),
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/mu.png"
    },
    "it8" : {
        "name" : "heart^2",
        "hp" : 50,
        "max_hp" : 50,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/heartv2.png"
    },
    "it9" : {
        "name" : "I_heart",
        "hp" : None,
        "max_hp" : 30,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/I_heart.png"
    },
    "it10" : {
        "name" : "I_heartv2",
        "hp" : None,
        "max_hp" : 50,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/I_heartv2.png"
    },
    "it11" : {
        "name" : "+5",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : 5,
        "max_damage" : 5,
        "min_damage" : 2,
        "size" : None,
        "attack_type" : None,
        "texture" : "assets/item/+5.png"
    },

}

coin_types = {
    "+1" : {
        "value" : 1,
        "texture" : "assets/loot/coin.png" 
    }
}

drop_items = {
    "heart" : {
        "hp" : 10,
        "texture" : "assets/loot/potion.png"
    }
}

rd_items = { "r1" : {
        "name" : "big",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : TILE_SIZE*0.1,
        "texture" : "assets/loot/rd_dice.png"
},
           "r2" : {
        "name" : "small",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : -(TILE_SIZE*0.1), 
        "texture" : "assets/loot/rd_dice.png"
},
            "r3" : {
        "name" : "-hp",
        "hp" : -10,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "texture" : "assets/loot/rd_dice.png"
},
            "r4" : {
        "name" : "+hp",
        "hp" : 10,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "texture" : "assets/loot/rd_dice.png"
},
            "r5" : {
        "name" : "+dg",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : 1,
        "max_damage" : 1,
        "min_damage" : 1,
        "size" : None,
        "texture" : "assets/loot/rd_dice.png"
},
            "r6" : {
        "name" : "-dg",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : -1,
        "max_damage" : -1,
        "min_damage" : -1,
        "size" : None,
        "texture" : "assets/loot/rd_dice.png"
},
            "r7" : {
        "name" : "long",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : 0.1,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "texture" : "assets/loot/rd_dice.png"
},
            "r8" : {
        "name" : "short",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : None,
        "attack_range" : -(0.1),
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "texture" : "assets/loot/rd_dice.png"
},
            "r9" : {
        "name" : "u_dada",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : 0.95,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "texture" : "assets/loot/rd_dice.png"
},
            "r10" : {
        "name" : "r_u_dada",
        "hp" : None,
        "max_hp" : None,
        "speed" : None,
        "attack_speed" : 1.05,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : None,
        "texture" : "assets/loot/rd_dice.png"
},
            "r11" : {
        "name" : "light",
        "hp" : None,
        "max_hp" : None,
        "speed" : (TILE_SIZE/50)*0.075,
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : -(TILE_SIZE*0.05),
        "texture" : "assets/loot/rd_dice.png"
},
            "r12" : {
        "name" : "heavy",
        "hp" : None,
        "max_hp" : None,
        "speed" : -((TILE_SIZE/50)*0.075),
        "attack_speed" : None,
        "attack_range" : None,
        "damage" : None,
        "max_damage" : None,
        "min_damage" : None,
        "size" : TILE_SIZE*0.05,
        "texture" : "assets/loot/rd_dice.png"
},

}

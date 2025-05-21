def print_map_data(map_data, width, height):
    print("Generated Map:")
    for y in range(height):
        for x in range(width):
            room = map_data[(x, y)]
            print(f"Room ({x}, {y}):")
            for row in room:
                print(" ".join(str(tile) for tile in row))
            print()

def print_room_connections(connections, width, height):
    print("Room Connections:")
    for y in range(height):
        for x in range(width):
            conn = connections[(x, y)]
            active = [d for d, ok in conn.items() if ok]
            print(f"Room ({x},{y}) -> {active}")
        print()

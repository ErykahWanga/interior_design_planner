from app.db.connection import init_db, get_session
from app.models.room import Room
from app.models.furniture import Furniture
from app.models.category import Category

def main():
    init_db()
    session = get_session()
    
    # Seed initial categories
    if not Category.all(session):
        for name in ['Seating', 'Storage', 'Decor']:
            category = Category(name)
            category.save(session)
    
    try:
        while True:
            print("\nInterior Design Planner")
            print("1. Add/Update Room")
            print("2. List Rooms")
            print("3. Add Category")
            print("4. Add Furniture to Room")
            print("5. Delete Furniture")
            print("6. View Room Details with Cost")
            print("7. Delete Room")
            print("8. Exit")
            
            choice = input("Enter choice (1-8): ").strip()
            if not choice:
                print("Please enter a valid choice.")
                continue

            if choice == '1':
                try:
                    name = input("Room name: ").strip()
                    if not name:
                        print("Room name cannot be empty.")
                        continue
                    room_id = input("Room ID to update (or press Enter for new room): ").strip()
                    room = Room.find_by_id(session, int(room_id)) if room_id else None
                    length = float(input(f"Room length (ft) {f'(current: {room.length})' if room else ''}: ") or (room.length if room else 0))
                    width = float(input(f"Room width (ft) {f'(current: {room.width})' if room else ''}: ") or (room.width if room else 0))
                    if length <= 0 or width <= 0:
                        print("Length and width must be positive.")
                        continue
                    room = room or Room(name, length, width)
                    room.name, room.length, room.width = name, length, width
                    room.save(session)
                    print(f"Room '{name}' {'updated' if room_id else 'added'}.")
                except ValueError:
                    print("Please enter valid numerical values for length and width.")

            elif choice == '2':
                rooms = Room.all(session)
                if rooms:
                    for room in rooms:
                        print(f"ID: {room.id}, Name: {room.name}, Size: {room.length}x{room.width} ft, Area: {room.area():.2f} sq ft")
                else:
                    print("No rooms found.")

            elif choice == '3':
                name = input("Category name: ").strip()
                if not name:
                    print("Category name cannot be empty.")
                    continue
                category = Category(name)
                category.save(session)
                print(f"Category '{name}' added.")

            elif choice == '4':
                try:
                    room_id = int(input("Enter Room ID: "))
                    room = Room.find_by_id(session, room_id)
                    if not room:
                        print("Room not found.")
                        continue
                    name = input("Furniture name: ").strip()
                    if not name:
                        print("Furniture name cannot be empty.")
                        continue
                    cost = float(input("Furniture cost: "))
                    if cost < 0:
                        print("Cost cannot be negative.")
                        continue
                    print("Available categories:")
                    categories = Category.all(session)
                    if not categories:
                        print("No categories available. Please add a category first.")
                        continue
                    for cat in categories:
                        print(f"ID: {cat.id}, Name: {cat.name}")
                    category_id = int(input("Enter Category ID: "))
                    category = session.query(Category).get(category_id)
                    if not category:
                        print("Category not found.")
                        continue
                    furniture = Furniture(name, cost, room_id, category_id)
                    furniture.save(session)
                    print(f"Furniture '{name}' added to room {room_id}.")
                except ValueError:
                    print("Please enter valid numerical values for room ID, cost, or category ID.")

            elif choice == '5':
                try:
                    furniture_id = int(input("Enter Furniture ID to delete: "))
                    furniture = session.query(Furniture).get(furniture_id)
                    if furniture:
                        furniture.delete(session)
                        print(f"Furniture {furniture_id} deleted.")
                    else:
                        print("Furniture not found.")
                except ValueError:
                    print("Please enter a valid Furniture ID.")

            elif choice == '6':
                try:
                    room_id = int(input("Enter Room ID: "))
                    room = Room.find_by_id(session, room_id)
                    if room:
                        print(f"\nRoom: {room.name}, Size: {room.length}x{room.width} ft, Area: {room.area():.2f} sq ft")
                        print("Furniture:")
                        furniture_list = room.furniture
                        furniture_dict = {f.id: {'name': f.name, 'cost': f.cost, 'category': f.category.name} for f in furniture_list}
                        if furniture_dict:
                            for f_id, f_data in furniture_dict.items():
                                print(f"  - ID: {f_id}, {f_data['name']}, Cost: ${f_data['cost']:.2f}, Category: {f_data['category']}")
                        else:
                            print("  No furniture in this room.")
                        total_cost = room.total_cost(session)
                        print(f"Total Furniture Cost: ${total_cost:.2f}\n")
                    else:
                        print("Room not found.")
                except ValueError:
                    print("Please enter a valid Room ID.")

            elif choice == '7':
                try:
                    room_id = int(input("Enter Room ID to delete: "))
                    room = Room.find_by_id(session, room_id)
                    if room:
                        room.delete(session)
                        print(f"Room {room_id} deleted.")
                    else:
                        print("Room not found.")
                except ValueError:
                    print("Please enter a valid Room ID.")

            elif choice == '8':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()
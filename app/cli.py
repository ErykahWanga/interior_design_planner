#this file containesdat
from app.db.connection import init_db, get_session
from app.models.room import Room

def main():
    init_db()
    session = get_session()
    
    while True:
        print("\nInterior Design Planner")
        print("1. Add/Update Room")
        print("2. List Rooms")
        print("3. Exit")
        try:
            choice = input("Enter choice (1-3): ").strip()
            if not choice:
                print("Please enter a valid choice.")
                continue

            if choice == '1':
                name = input("Room name: ").strip()
                if not name:
                    print("Room name cannot be empty.")
                    continue
                try:
                    room_id = input("Room ID to update (or press Enter for new room): ").strip()
                    room = Room.find_by_id(session, int(room_id)) if room_id else None
                    length = float(input(f"Room length (ft) {f'(current: {room.length})' if room else ''}: ") or (room.length if room else 0))
                    width = float(input(f"Room width (ft) {f'(current: {room.width})' if room else ''}: ") or (room.width if room else 0))
                    room = room or Room(name, length, width)
                    room.name, room.length, room.width = name, length, width
                    room.save(session)
                    print(f"Room '{name}' {'updated' if room_id else 'added'}.")
                except ValueError:
                    print("Please enter valid numerical values for length and width.")

            elif choice == '2':
                rooms = Room.all(session)
                for room in rooms:
                    print(f"ID: {room.id}, Name: {room.name}, Size: {room.length}x{room.width} ft")

            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except EOFError:
            print("Input interrupted. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            session.close()
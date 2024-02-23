import argparse
from models import Student, Group, Teacher, Subject
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Підключення до бази даних
engine = create_engine('postgresql://postgres:My5aK8_U91veR5ty@localhost:5432/fake_universaty')
Session = sessionmaker(bind=engine)
session = Session()


def model_factory(model_name):
    models = {
        "Teacher": Teacher,
        "Student": Student,
        "Group": Group,
        "Subject": Subject
    }
    return models.get(model_name)

def create(model_name, name):
    model_class = model_factory(model_name)
    if model_class:
        obj = model_class(name=name)
        session.add(obj)
        session.commit()
        return obj.id
    else:
        return f"Модель {model_name} не знайдена."

def read(model_name, item_id):
    model_class = model_factory(model_name)
    if model_class:
        obj = session.query(model_class).filter_by(id=item_id).first()
        if obj:
            return (obj.id, obj.name)
        else:
            return None
    else:
        return f"Модель {model_name} не знайдена."

def update(model_name, item_id, new_name):
    model_class = model_factory(model_name)
    if model_class:
        obj = session.query(model_class).filter_by(id=item_id).first()
        if obj:
            obj.name = new_name
            session.commit()
            return f"Ім'я об'єкта з ID {item_id} оновлено до {new_name}."
        else:
            return f"Об'єкта з ID {item_id} не знайдено."
    else:
        return f"Модель {model_name} не знайдена."

def remove(model_name, item_id):
    model_class = model_factory(model_name)
    if model_class:
        obj = session.query(model_class).filter_by(id=item_id).first()
        if obj:
            session.delete(obj)
            session.commit()
            return f"Об'єкт з ID {item_id} успішно видалений."
        else:
            return f"Об'єкта з ID {item_id} не знайдено."
    else:
        return f"Модель {model_name} не знайдена."

def list_all(model):
    objs = session.query(model).all()
    if objs:
        obj_list = [(obj.id, obj.name) for obj in objs]
        return obj_list
    else:
        return []

def handle_create_action(model_name, name):
    return create(model_name, name)

def handle_list_action(model_name):
    model_class = model_factory(model_name)
    if model_class:
        obj_list = list_all(model_class)
        if obj_list:
            result = f"Список усіх {model_name}:\n"
            for obj_id, obj_name in obj_list:
                result += f"ID: {obj_id}, Name: {obj_name}\n"
            return result
        else:
            return f"У базі даних немає жодного об'єкта типу {model_name}."
    else:
        return f"Модель {model_name} не знайдена."

def handle_read_action(model_name, item_id):
    return read(model_name, item_id)

def handle_update_action(model_name, item_id, new_name):
    return update(model_name, item_id, new_name)

def handle_remove_action(model_name, item_id):
    return remove(model_name, item_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI програма для CRUD операцій із базою даних")
    parser.add_argument("--action", "-a", choices=["create", "read", "update", "remove", "list"], required=True, help="Дія для виконання (create, read, update, delete, list)")
    parser.add_argument("--model", "-m", choices=["Student", "Group", "Teacher", "Subject"], required=True, help="Модель для виконання операції")
    parser.add_argument("--name", "-n", help="Ім'я вчителя або студента")
    parser.add_argument("--id", "-i", help="ID елементу, який потрібно видалити")
    args = parser.parse_args()

    if args.action == "create":
        print(handle_create_action(args.model, args.name))
    elif args.action == "list":
        print(handle_list_action(args.model))
    elif args.action == "read":
        print(handle_read_action(args.model, args.id))
    elif args.action == "update":
        print(handle_update_action(args.model, args.id, args.name))
    elif args.action == "remove":
        print(handle_remove_action(args.model, args.id))
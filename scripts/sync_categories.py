import os
from pathlib import Path

import pymysql


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def read_categories(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {file_path}")

    categories: list[str] = []
    seen: set[str] = set()

    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        name = raw_line.strip()
        if not name:
            continue

        normalized = name.casefold()
        if normalized in seen:
            continue

        seen.add(normalized)
        categories.append(name)

    return categories


def get_connection() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=os.environ.get("HESK_DB_HOST", "localhost"),
        port=int(os.environ.get("HESK_DB_PORT", "3306")),
        user=os.environ["HESK_DB_USER"],
        password=os.environ["HESK_DB_PASSWORD"],
        database=os.environ["HESK_DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def fetch_existing_categories(connection: pymysql.connections.Connection) -> dict[str, dict]:
    query = """
        SELECT id, name, cat_order, autoassign, type, priority
        FROM hesk_categories
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    existing: dict[str, dict] = {}
    for row in rows:
        existing[row["name"].casefold()] = row
    return existing


def get_next_cat_order(connection: pymysql.connections.Connection) -> int:
    query = "SELECT COALESCE(MAX(cat_order), 0) AS max_order FROM hesk_categories"
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
    return int(row["max_order"]) + 1


def insert_category(
    connection: pymysql.connections.Connection,
    name: str,
    cat_order: int,
) -> None:
    query = """
        INSERT INTO hesk_categories (name, cat_order, autoassign, type, priority)
        VALUES (%s, %s, '1', '0', 3)
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (name, cat_order))


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    env_file = project_root / ".env"
    categories_file = project_root / "categories.txt"

    load_env_file(env_file)

    os.environ.setdefault("HESK_DB_HOST", "localhost")
    os.environ.setdefault("HESK_DB_PORT", "3306")

    categories_from_file = read_categories(categories_file)

    print("=== Lectura de categories.txt ===")
    print(f"Categorías leídas: {len(categories_from_file)}")
    for category in categories_from_file:
        print(f" - {category}")

    connection = get_connection()

    try:
        existing = fetch_existing_categories(connection)
        print("\n=== Categorías existentes en HESK ===")
        if existing:
            for row in existing.values():
                print(f" - {row['name']}")
        else:
            print(" - No hay categorías cargadas")

        new_categories: list[str] = []
        skipped_categories: list[str] = []

        for category in categories_from_file:
            if category.casefold() in existing:
                skipped_categories.append(category)
            else:
                new_categories.append(category)

        print("\n=== Resultado de comparación ===")
        print(f"Existentes / omitidas: {len(skipped_categories)}")
        for category in skipped_categories:
            print(f" - OMITIDA: {category}")

        print(f"Nuevas a insertar: {len(new_categories)}")
        for category in new_categories:
            print(f" - NUEVA: {category}")

        next_order = get_next_cat_order(connection)

        for category in new_categories:
            insert_category(connection, category, next_order)
            next_order += 1

        connection.commit()

        print("\n=== Inserción finalizada ===")
        if new_categories:
            print("Se insertaron correctamente las categorías nuevas.")
        else:
            print("No hubo inserciones. El proceso fue idempotente.")
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
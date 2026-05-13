import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Catalogue, engine

def create_db():
    Base.metadata.create_all(engine)
    print("Database + tables created.")

def import_csv(csv_path="library_catalogue.csv"):
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(csv_path)

    # convert NaN → None
    df = df.where(pd.notnull(df), None)

    count = 0

    for _, row in df.iterrows():

        # avoid crashing on bad years
        year = row["releaseYear"]
        if year is not None:
            try:
                year = int(year)
            except:
                year = None

        book = Catalogue(
            title=row["title"],
            author=row["author"],
            publisher=row["publisher"],
            releaseYear=year,
            description=row["description"]
        )

        session.add(book)
        count += 1

    session.commit()
    session.close()

    print(f"Imported {count} books into database.")

if __name__ == "__main__":
    create_db()
    import_csv()
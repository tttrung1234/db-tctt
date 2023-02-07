from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}?check_same_thread=False"

engine = create_engine(sqlite_url)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

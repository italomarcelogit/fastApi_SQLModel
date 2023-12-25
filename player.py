from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from random import randint

# setup sqlite 
class Player(SQLModel, table=True):
    id_player: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    nick_name: str
    age: Optional[int] = Field(default=None, index=True)
    mail: str

sqlite_file_name = "dados.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
# fim setup sqlite 

# setup fast api
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/insert_player/")
def create_player(player: Player):
    with Session(engine) as session:
        session.add(player)
        session.commit()
        session.refresh(player)
        return player

@app.get("/players/")
def read_players():
    with Session(engine) as session:
        players = session.exec(select(Player)).all()
        return players

@app.get("/populate/")
def populate():
    for i in range(randint(1, 100)):
        with Session(engine) as session:
            session.add(Player(id_player=i*10, name=f"Jogador {i*10}", nick_name=f"player{i*10}", 
                                age=randint(18,50), mail=f"player{i*10}@gmail.com"))
            session.commit()
    return "Jogadores criados aleatóriamente"
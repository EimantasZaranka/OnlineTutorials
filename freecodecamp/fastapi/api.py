from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

champions = {
	1: {
		"name": "Teemo",
		"species": "Yordle",
		"region": "Bandle City",
		"occupation": ["Scout"]
	},
	2:{
		"name": "Illaoi",
		"species": "Human",
		"region": "Bilgewater",
		"occupation": ['Nagakabouros Truth Bearer', 'Protector of Life']
	},
	3:{
		"name": "Ornn",
		"species": "Spirit God",
		"region": "Freljord",
		"occupation": ["Smith", "Craftsman", "Guardian", "Demi-God Spirit"]
	}
}


class Champion(BaseModel):
	name: str
	species: str
	region: str
	occupation: list

class UpdateChampion(BaseModel):
	name: Optional[str] = None
	species: Optional[str] = None
	region: Optional[str] = None
	occupation: Optional[list] = None

@app.get("/")
def index():
	return {"title": "Learning FastAPI"}

@app.get("/get-champion/{champion_id}")
def get_champion(champion_id: int = Path(None, description="The ID of the champion")):
	return champions[champion_id]

#Optional parameters cannot come before required parameters
@app.get("/get-by-name")
def get_champion_by_name(*, name: Optional[str] = None):
	for champ in champions.values():
		if champ['name'] == name:
			return champ
	return {"Data": "Champion not found!"}

@app.get("/get-by-name/{champ_id}")
def get_champion_by_id_and_name(*, champ_id: int, name: Optional[str]=None):
	if champions[champ_id]['name'] == name or name == None:
		return champions[champ_id]
	return {'Data': 'Not found'}

@app.post("/create-champion/{champ_id}")
def create_champion(champ_id: int, champion: Champion):
	if champ_id in champions:
		return {"Data": "Champion exists"}
	champions[champ_id] = champion
	return {"Data": "Champion added", "Champion": champions[champ_id]}


@app.put("/update-champion/{champ_id}")
def update_champ(champ_id: int, champion: UpdateChampion):
	if champ_id not in champions:
		return {"Data": "Champ do not exist"}

	for name, field in champion.dict().items():
		if field != None:
			champions[champ_id][name] = field

	return {"Data": "Champion updated", "Champion": champions[champ_id]}

@app.delete("/delete-champ/{champ_id}")
def delete_champ(champ_id: int):
	if champ_id not in champions:
		return {'Data':'Champ does not exist'}
	del champions[champ_id]
	return {'Data': f'Champ {champ_id} was deleted'}
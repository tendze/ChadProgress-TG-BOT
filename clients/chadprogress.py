import requests

class ChadProgressClient:
    def __init__(self, base_url: str):
        self.base_url = base_url 
    
    def register(self, login: str, password: str, name: str, role: str) -> str | None:
        request_body = {
            "email": login,
            "password": password,
            "name": name,
            "role": role
        }

        request = requests.post(self.base_url+"/authorization/register", json=request_body)
        response_body = request.json()

        return response_body.get("token")
        
    
    def login(self, login: str, password: str):
        request_body = {
            "email": login,
            "password": password
        }

        request = requests.post(self.base_url+"/authorization/login", json=request_body)
        response_body = request.json()

        return response_body.get("token")
    
    def get_user_by_id(self, token: str, id: int):
        data = {
            "user-id": id
        }

        return requests.get(f"{self.base_url}/user/user", json=data, headers=self.bearer_header(token))
    
    def create_trainer_profile(self, token: str, qualification: str, experience: str, achievement: str):
        data = {
            "qualification": qualification,
            "experience": experience,
            "achievement": achievement
        }
        
        return requests.post(f"{self.base_url}/user/trainers/profile", json=data, headers=self.bearer_header(token))
    
    def get_trainers_list(self, token: str) -> list[any]:
        return requests.get(f"{self.base_url}/user/trainers", headers=self.bearer_header(token))

    def get_trainer_profile(self, token: str, trainerID: int = None):
        if trainerID != None:
            return requests.get(f"{self.base_url}/user/trainers/profile", json={"trainer-id": trainerID}, headers=self.bearer_header(token))
        
        return requests.get(f"{self.base_url}/user/trainers/profile", headers=self.bearer_header(token))

    def get_trainers_clients(self, token: str):
        return requests.get(f"{self.base_url}/user/trainers/clients", headers=self.bearer_header(token))

    def create_client_profile(self, token: str, height: float, weight: float, bodyfat: float):
        data = {
            "height": height,
            "weight": weight,
            "bodyfat": bodyfat
        }
        return requests.post(f"{self.base_url}/user/clients/profile", json=data, headers=self.bearer_header(token))

    def get_client_profile(self, token: str):
        return requests.get(f"{self.base_url}/user/clients/profile", headers=self.bearer_header(token))

    def select_trainer(self, token: str, trainer_id: int):
        data = {
            "trainer-id": trainer_id
        }
        return requests.patch(f"{self.base_url}/user/clients/select-trainers", json=data, headers=self.bearer_header(token))

    def add_metrics(self, token: str, height: float, weight: float, bodyfat: float, bmi: float, measured_at: str):
        data = {
            "height": height,
            "weight": weight,
            "bodyfat": bodyfat,
            "bmi": bmi,
            "measured-at": measured_at
        }
        return requests.post(f"{self.base_url}/user/clients/metrics", json=data, headers=self.bearer_header(token))

    def get_metrics(self, token: str):
        return requests.get(f"{self.base_url}/user/clients/metrics", headers=self.bearer_header(token))

    def create_plan(self, token: str, client_id: int, description: str, schedule: str):
        data = {
            "client-id": client_id,
            "description": description,
            "schedule": schedule
        }
        return requests.post(f"{self.base_url}/user/training-plan", json=data, headers=self.bearer_header(token))

    def get_plan(self, token: str, trainer_id: int, client_id: int):
        data = {
            "trainer-id": trainer_id,
            "client-id": client_id
        }
        return requests.get(f"{self.base_url}/user/training-plan", json=data, headers=self.bearer_header(token))

    def add_progress_report(self, token: str, client_id: int, comments: str):
        data = {
            "client-id": client_id,
            "comments": comments
        }
        return requests.post(f"{self.base_url}/user/progress-reports", json=data, headers=self.bearer_header(token))

    def get_progress_reports(self, token: str, trainer_id: int, client_id: int):
        data = {
            "trainer-id": trainer_id,
            "client-id": client_id
        }
        return requests.get(f"{self.base_url}/user/progress-reports", json=data, headers=self.bearer_header(token))
    
    def bearer_header(self, jwt: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {jwt}",
            "Content-type": "application/json"
        }
    
    
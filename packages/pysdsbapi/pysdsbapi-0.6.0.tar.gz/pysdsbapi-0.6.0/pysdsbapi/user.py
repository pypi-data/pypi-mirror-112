class User:
    def __init__(self, id : str, password : str):
        self.id = id
        self.password = password


    def __str__(self):
        return f'User(id={self.id}, password={self.password})'
    
    def __repr__(self):
        return self.__str__()
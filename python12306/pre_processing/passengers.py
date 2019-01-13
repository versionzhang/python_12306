from utils.data_structure import PassengerDetail


class PassengerTool(object):

    def __init__(self, raw_data):
        self.passenger = []
        self.raw_data = raw_data

    def to_python(self):
        self.passenger = [PassengerDetail(v) for v in self.raw_data]
        return self

    def find_people_by_names(self, names):
        data = list(filter(lambda x: x.passenger_name in names, self.passenger))
        return data

    def get_final_data(self):
        self.to_python()
        return self


PassengerData = PassengerTool(raw_data=[]).get_final_data()

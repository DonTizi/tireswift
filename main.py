import csv
from datetime import datetime, date, time, timedelta
import json

# service for costs/time
services = {
    "compact": {"prices": 150, "time": 30},
    "medium": {"prices": 150, "time": 30},
    "full-size": {"prices": 150, "time": 30},
    "class 1 truck": {"prices": 250, "time": 60},
    "class 2 truck": {"prices": 700, "time": 120},
}

type = {
    "compact": {"type": 1},
    "medium": {"type": 2},
    "full-size": {"type": 3},
    "class 1 truck": {"type": 4},
    "class 2 truck": {"type": 5},
}


# client class
class client:
    def __init__(self, CallDateTime, AppointmentDateTime, CarType):
        self.CallDateTime = CallDateTime
        self.AppointmentDateTime = AppointmentDateTime
        self.CarType = CarType


class Scheduler:
    def __init__(self):
        # self.available_slots = [True] * 720 # 60 minutes (or time slots) in an hour, from 7 am to 7 pm
        self.stations = []
        self.extras = []
        self.rows = []  # number of clients accepted, reservation start - end - vehicletype - station

        for i in range(5):
            row = [True] * 720
            self.stations.append(row)

        for j in range(5):
            row = [0] * 720
            self.extras.append(row)

        self.AmountGained = 0
        self.AmountLost = 0

    def book_appointment(self, client, duration):
        start_time = client.AppointmentDateTime

        if 7 <= start_time.hour < 19:  # if between 7 am to 7 pm
            end_time_slot = self.ConvertToSlot(start_time) + duration

            if end_time_slot > 720:
                print("Time slot goes over-time, will not book.")
                self.loss(client)
                return False

            if self.is_station_available(client, self.ConvertToSlot(start_time), end_time_slot):
                self.fill_station(client, start_time, end_time_slot)
                return True
            elif self.is_extra_available(client, self.ConvertToSlot(start_time), end_time_slot):
                print(f"Appointment booked from {start_time.hour}:{start_time.minute} to "
                      f"{int(end_time_slot / 60) + 7}:{end_time_slot % 60}")  # convert slots back to actual time
                self.gain(client)
                return True
            else:
                print("Slot already booked. Please choose another time.")
                self.loss(client)
                return False
        else:
            print("Request to book is out of range, must be between 7 am to 7 pm.")
            self.loss(client)
            return False

    def ConvertToSlot(self, time):
        return (time.hour - 7) * 60 + time.minute

    # check if space is available in stations
    def is_station_available(self, client, start_time, end_time):
        if client.CarType == "compact":
            return all(self.stations[0][i] for i in range(start_time, end_time))
        elif client.CarType == "medium":
            return all(self.stations[1][i] for i in range(start_time, end_time))
        elif client.CarType == "full-size":
            return all(self.stations[2][i] for i in range(start_time, end_time))
        elif client.CarType == "class 1 truck":
            return all(self.stations[3][i] for i in range(start_time, end_time))
        elif client.CarType == "class 2 truck":
            return all(self.stations[4][i] for i in range(start_time, end_time))

    # fill station
    def fill_station(self, client, start_time, end_time):
        if client.CarType == "compact":
            for i in range(self.ConvertToSlot(start_time), end_time):
                self.stations[0][i] = False
            print(f"Appointment booked from {start_time.hour}:{start_time.minute} to "
                  f"{int(end_time / 60) + 7}:{end_time % 60}")  # convert slots back to actual time
            self.gain(client)
            self.rows.append([client.AppointmentDateTime, timedelta(hours=int(end_time/60+7), minutes=(end_time%60)),
                              client.CarType, "Station 1"])
        elif client.CarType == "medium":
            for i in range(self.ConvertToSlot(start_time), end_time):
                self.stations[1][i] = False
            print(f"Appointment booked from {start_time.hour}:{start_time.minute} to "
                  f"{int(end_time / 60) + 7}:{end_time % 60}")  # convert slots back to actual time
            self.gain(client)
            self.rows.append([client.AppointmentDateTime, timedelta(hours=int(end_time/60+7), minutes=(end_time%60)),
                              client.CarType, "Station 2"])
        elif client.CarType == "full-size":
            for i in range(self.ConvertToSlot(start_time), end_time):
                self.stations[2][i] = False
            print(f"Appointment booked from {start_time.hour}:{start_time.minute} to "
                  f"{int(end_time / 60) + 7}:{end_time % 60}")  # convert slots back to actual time
            self.gain(client)
            self.rows.append([client.AppointmentDateTime, timedelta(hours=int(end_time/60+7), minutes=(end_time%60)),
                              client.CarType, "Station 3"])
        elif client.CarType == "class 1 truck":
            for i in range(self.ConvertToSlot(start_time), end_time):
                self.stations[3][i] = False
            print(f"Appointment booked from {start_time.hour}:{start_time.minute} to "
                  f"{int(end_time / 60) + 7}:{end_time % 60}")  # convert slots back to actual time
            self.gain(client)
            self.rows.append([client.AppointmentDateTime, timedelta(hours=int(end_time/60+7), minutes=(end_time%60)),
                              client.CarType, "Station 4"])
        elif client.CarType == "class 2 truck":
            for i in range(self.ConvertToSlot(start_time), end_time):
                self.stations[4][i] = False
            print(f"Appointment booked from {start_time.hour}:{start_time.minute} to "
                  f"{int(end_time / 60) + 7}:{end_time % 60}")  # convert slots back to actual time
            self.gain(client)
            self.rows.append([client.AppointmentDateTime, timedelta(hours=int(end_time/60+7), minutes=(end_time%60)),
                              client.CarType, "Station 5"])

    # check if space available in extra
    def is_extra_available(self, client, start_time, end_time):
        temporary = 0
        for station in self.extras:
            bl = all(self.extras[temporary][i] == 0 for i in range(start_time, end_time)) # condition is not bool
            if bl == True:
                for i in range(start_time, end_time):
                    self.extras[temporary][i] = type[client.CarType]["type"]
                timedelta(end_time)
                self.rows.append([client.AppointmentDateTime,
                                  timedelta(hours=int(end_time/60 + 7), minutes=(end_time%60)), client.CarType, f"Station {temporary + 6}"])
                return True
            temporary = temporary + 1
        return False

    def loss(self, client):
        self.AmountLost = self.AmountLost - services[client.CarType]["prices"]

    def gain(self, client):
        self.AmountGained = self.AmountGained + services[client.CarType]["prices"]

    def GetTimeStamp(self, slot):
        return time(int(slot / 60), (slot % 60))


# this calendar consists of 31 days of october and 30 days of november, each day consisting one schedular
class calendar:
    def __init__(self):
        self.october = []
        self.november = []
        for i in range(31):
            self.october.append(Scheduler())
        for i in range(30):
            self.november.append(Scheduler())

    def book_appointment(self, client, duration):
        if client.AppointmentDateTime.month == 10:
            self.october[client.AppointmentDateTime.day - 1].book_appointment(client, duration)
        elif client.AppointmentDateTime.month == 11:
            self.november[client.AppointmentDateTime.day - 1].book_appointment(client, duration)

    def CalcDailyOctGain(self, day):
        return self.october[day - 1].AmountGained

    def CalcDailyOctLoss(self, day):
        return self.october[day - 1].AmountLost

    def CalcDailyNovGain(self, day):
        return self.november[day - 1].AmountGained

    def CalcDailyNovLoss(self, day):
        return self.november[day - 1].AmountLost


# Main app class that you will create and run using app.run()
class App:
    def __init__(self):
        self.clients = []
        self.calendar = calendar()

    def CalculateTotalRevenueOctober(self):
        temporary = 0
        for i in self.calendar.october:
            temporary = temporary + i.AmountGained
        return temporary

    def CalculateTotalRevenueNovember(self):
        temporary = 0
        for i in self.calendar.november:
            temporary = temporary + i.AmountGained
        return temporary

    def TotalRevenue(self):
        return self.CalculateTotalRevenueOctober() + self.CalculateTotalRevenueNovember()

    def CalculateTotalLossOctober(self):
        temporary = 0
        for i in self.calendar.october:
            temporary = temporary + i.AmountLost
        return temporary

    def CalculateTotalLossNovember(self):
        temporary = 0
        for i in self.calendar.november:
            temporary = temporary + i.AmountLost
        return temporary

    def TotalLoss(self):
        return self.CalculateTotalLossOctober() + self.CalculateTotalLossNovember()

    # store .csv values into client class and into the memory
    def ImportData(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                CallDateTime = row[0].split(' ')
                CallDate = CallDateTime[0]
                CallTime = CallDateTime[1]

                AppointmentDateTime = row[1].split(' ')
                AppointmentDate = AppointmentDateTime[0]
                AppointmentTime = AppointmentDateTime[1]

                d = date.fromisoformat(CallDate)
                t = time.fromisoformat(CallTime)
                call = datetime(d.year, d.month, d.day, t.hour, t.minute)

                d = date.fromisoformat(AppointmentDate)
                t = time.fromisoformat(AppointmentTime)
                appoint = datetime(d.year, d.month, d.day, t.hour, t.minute)

                self.clients.append(client(call, appoint, row[2]))
            self.clients.sort(key=lambda x: x.CallDateTime)

    def ExportData(self):
        with open('sorted.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for day in self.calendar.october:
                for row in day.rows:
                    csv_writer.writerow(row)
            for day in self.calendar.november:
                for row in day.rows:
                    csv_writer.writerow(row)

    def run(self):
        self.ImportData('C:\\Users\\thefa\\PycharmProjects\\OpenCV\\datafile.csv')
        for cli in self.clients:
            self.calendar.book_appointment(cli, services[cli.CarType]["time"])
        self.ExportData()
        print(self.TotalRevenue())
        print(self.TotalLoss())


App = App()
App.run()

from . import models
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .model_handers import DeviceInfo
from .dto_types import DeviceInfoDTO, CalcAdImpr

app = FastAPI()

WORKLOAD_HOURS_WEEKDAYS = {
    "MAX": [12, 13, 16, 17, 18, 19],
    "MED": [7, 8, 9, 10, 11, 14, 15, 20, 21, 22],
    "MIN": [0, 1, 2, 3, 4, 5, 6, 23]
}

WORKLOAD_HOURS_WEEKENDS = {
    "MAX": [12, 13, 14, 15, 16, 17, 18, 19],
    "MED": [10, 11, 14, 20, 21],
    "MIN": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 23, 22]
}

MAX_IN_HOUR = 24

# 6 , 9, 18, 24, 30, 36, 42, 48, 54, 60, 66 и 72


@app.post("/create_device")
async def create_device(dev: DeviceInfoDTO):
    return await DeviceInfo.create(
        DeviceInfo.CreateT(mac=dev.mac,
                           timestamp=dev.timestamp,
                           bilboard_id=dev.bilboard_id))


@app.post("/get_info")
async def get_info():
    timestamps = await DeviceInfo.get_distinct_timestamps()

    response = dict()

    for timestamp in timestamps:
        r = await models.objects.execute(
            models.DeviceInfo.select(models.DeviceInfo.id).where(
                models.DeviceInfo.timestamp == timestamp))
        response[str(timestamp)] = {
            "ftime": timestamp.strftime("%a,%b,%Y-%m-%d,%H:%M%S"),
            "count": len(r)
        }

    return JSONResponse(content=response)


@app.post("/calc_ad_imr")
async def calc_ad_imr(data: CalcAdImpr):
    number_ad_impr = data.number

    response = {
        b:
        {d: {h: 0
             for h in range(1, 23 + 1)}
         for d in range(1,7+1)}
        for b in DeviceInfo.BILBOARD_IDS
    }

    bilboard_stat_by_weekday = dict()
    for day in range(1, 7 + 1):
        bilboard_stat_by_weekday[
            day] = await DeviceInfo.get_bilboard_stat_by_weekday(weekday=day)

    for day in range(1, 5 + 1):
        __tmp = bilboard_stat_by_weekday[day]
        sorted_stat = sorted(list(__tmp.items()), key=lambda i: i[1])
        min_watches = list(  map( lambda ss: ss[0] , sorted_stat[0:12]))
        med_watches = list(  map( lambda ss: ss[0] , sorted_stat[12:20]))
        max_watches = list(  map( lambda ss: ss[0] , sorted_stat[20:]))

        for hour in range(0, 23 + 1):
            if hour in WORKLOAD_HOURS_WEEKDAYS["MAX"]:
                for bb_id in min_watches:
                    response[bb_id][day][hour] = 18
                for bb_id in med_watches:
                    response[bb_id][day][hour] = 24
                for bb_id in max_watches:
                    response[bb_id][day][hour] = 36
            elif hour in WORKLOAD_HOURS_WEEKDAYS["MED"]:
                for bb_id in min_watches:
                    response[bb_id][day][hour] = 9
                for bb_id in med_watches:
                    response[bb_id][day][hour] = 18
                for bb_id in max_watches:
                    response[bb_id][day][hour] = 24
            else:
                for bb_id in min_watches:
                    response[bb_id][day][hour] = 6
                for bb_id in med_watches:
                    response[bb_id][day][hour] = 9
                for bb_id in max_watches:
                    response[bb_id][day][hour] = 18

    for day in range(6, 7 + 1):
        __tmp = bilboard_stat_by_weekday[day]
        sorted_stat = sorted(list(__tmp.items()), key=lambda i: i[1])
        min_watches = list(  map( lambda ss: ss[0] , sorted_stat[0:12]))
        med_watches = list(  map( lambda ss: ss[0] , sorted_stat[12:20]))
        max_watches = list(  map( lambda ss: ss[0] , sorted_stat[20:]))

        for hour in range(0, 23 + 1):
            if hour in WORKLOAD_HOURS_WEEKENDS["MAX"]:
                for bb_id in min_watches:
                    response[bb_id][day][hour] = 18
                for bb_id in med_watches:
                    response[bb_id][day][hour] = 24
                for bb_id in max_watches:
                    response[bb_id][day][hour] = 36
            elif hour in WORKLOAD_HOURS_WEEKENDS["MED"]:
                for bb_id in min_watches:
                    response[bb_id][day][hour] = 9
                for bb_id in med_watches:
                    response[bb_id][day][hour] = 18
                for bb_id in max_watches:
                    response[bb_id][day][hour] = 24
            else:
                for bb_id in min_watches:
                    response[bb_id][day][hour] = 6
                for bb_id in med_watches:
                    response[bb_id][day][hour] = 9
                for bb_id in max_watches:
                    response[bb_id][day][hour] = 18

    return response


@app.get("/get_data")
async def get_data(limit: int = 100, offset: int = 0):
    return await DeviceInfo.get_devices(limit=limit, offset=offset)


@app.get("/get_number_devices_with_timestamp")
async def get_number_devices_with_timestamp():
    return await DeviceInfo.get_number_devices_with_timestamp()


@app.get("/get_data_by_vendor")
async def get_data_by_vendor(vendor_id: int,
                             limit: int = 100,
                             offset: int = 0):
    return await DeviceInfo.get_devices_by_vendor_id(vendor_id=vendor_id,
                                                     limmit=limit,
                                                     offset=offset)


@app.get("/get_data_by_timestamp")
async def get_data_by_timestamp(timestamp: str,
                                limit: int = 100,
                                offset: int = 0):
    return await DeviceInfo.get_devices_by_timestamp(timestamp=timestamp,
                                                     limmit=limit,
                                                     offset=offset)


@app.get("/get_data_by_bilboard_id")
async def get_data_by_bilboard_id(bilboard_id: int,
                                  limit: int = 100,
                                  offset: int = 0):
    return await DeviceInfo.get_devices_by_bilboard_id(bilboard_id=bilboard_id,
                                                       limmit=limit,
                                                       offset=offset)


@app.get("/get_data_by_weekday")
async def get_data_by_weekday(weekday: int, limit: int = 100, offset: int = 0):
    if weekday > 7 or weekday < 1:
        return {
            "error":
            "The number of the day of the week can not exceed 7 and be less than 1"
        }
    return await DeviceInfo.get_devices_by_weekday(weekday=weekday,
                                                   limit=limit,
                                                   offset=offset)


@app.get("/get_number_devices_by_weekday")
async def get_number_devices_by_weekday(weekday: int):
    if weekday > 7 or weekday < 1:
        return {
            "error":
            "The number of the day of the week can not exceed 7 and be less than 1"
        }
    return await DeviceInfo.get_number_devices_by_weekday(weekday=weekday)


@app.get("/get_number_devices_by_month")
async def get_number_devices_by_weekday(month: int):
    if month > 12 or month < 1:
        return {
            "error":
            "The number of the month of the week can not exceed 7 and be less than 1"
        }
    return await DeviceInfo.get_number_devices_by_month(month=month)


## STAT FUNCTION


@app.get("/get_bilboard_stat_by_timestamp")
async def get_bilboard_stat_by_timestamp(timestamp: str):
    return await DeviceInfo.get_bilboard_stat_by_timestamp(timestamp)


@app.get("/get_bilboard_stat_by_weekday")
async def get_bilboard_stat_by_timestamp(weekday: int):
    if weekday > 7 or weekday < 1:
        return {
            "error":
            "The number of the day of the week can not exceed 7 and be less than 1"
        }
    return await DeviceInfo.get_bilboard_stat_by_weekday(weekday)


@app.get("/get_bilboard_stat_by_month")
async def get_bilboard_stat_by_timestamp(month: int):
    if month > 12 or month < 1:
        return {
            "error":
            "The number of the month of the week can not exceed 7 and be less than 1"
        }
    return await DeviceInfo.get_bilboard_stat_by_month(month)
class Commands:
    takeoff = dict(type="Ford", model="Mustang", year=1964)
    go_to_position = dict(type="Ford", model="Mustang", year=1964)
    land = dict(type="Ford", model="Mustang", year=1964)
    return_to_home = dict(type="Ford", model="Mustang", year=1964)
    start_mission = dict(type="Ford", model="Mustang", year=1964)
    change_mode = dict(type="Ford", model="Mustang", year=1964)


class Connect:
    init = dict(connect="1", disconnect="0")

    def connection_result(self,fog_name,result):
        reachable_drones=result
        return reachable_dronesasd
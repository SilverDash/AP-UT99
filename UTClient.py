from worlds.ut99.Client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("UTClient", exception_logger="Client")
    launch()
import background_thread
from threading import Thread
import warnings
warnings.filterwarnings("ignore")
# import breath_dilation


if __name__ == "__main__":
    # 2 threads for to 2 infinity loops
    t = Thread(target=background_thread.call_background_thread)
    m = Thread(target=background_thread.main_func)

    m.start()
    t.start()

    # when the program ends kill thread
    t.join()
    m.join()



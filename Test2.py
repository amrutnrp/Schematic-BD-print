
from schBD_print import *
# from imager import improve_view, view_str


if __name__ == "__main__":

    import pickle

    import sys
    _this = sys.modules[__name__]
    with open('s.pkl', 'rb') as f:
        S1, S2, S3 = pickle.load(f)

    # del S1, S3
    # _s_obj = S2


    A= improve_view(S2)
    view_str(A)

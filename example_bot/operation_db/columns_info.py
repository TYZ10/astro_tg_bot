

class ColumnsInfoDB:
    def __init__(self):
        self.userid = "userid"
        self.username = "username"
        self.full_name = "full_name"
        self.first_arrival = "first_arrival"
        self.last_action = "last_action"
        self.generation_count = "generation_count"
        self.payments_end = "payments_end"
        self.generation_count_all = "generation_count_all"

        self.data_birth = "data_birth"
        self.time_birth = "time_birth"
        self.place_birth = "place_birth"
        self.latitude = "latitude"
        self.longitude = "longitude"

        self.referrals_count = "referrals_count"
        self.referral_user = "referral_user"
        self.referral_all_count_user = "referral_all_count_user"
        self.referral_all_count_points_user = "referral_all_count_points_user"
        self.payments_id = "payments_id"

        self.time_prediction = "time_prediction"


COLUMNS_INFO = ColumnsInfoDB()

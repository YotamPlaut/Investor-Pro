import datetime

from dataOps_dev.UTILS.utils import *
if __name__ == '__main__':
    bearer_token='AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODjeKi3HQdi9EBFzlvsj9pXHwgZJt0sZO0ifZs2tmuTl5Zkout3y-ps8edB7Q-yu-wqT2P9ZMHoRZl4zF9ffdFqikDVY2OrjKoSIraBpZ2ulGQxGUf2h21XZbz5o5IbOwjc'
    stock_index=137
    api_start_date = '2023-05-24'
    api_end_date = '2024-05-19'
    api_info = indices_EoD_by_index_from_date_to_date(bearer=bearer_token, index_id=stock_index,
                                                      start_date=api_start_date, end_date=api_end_date)
    print(api_info)

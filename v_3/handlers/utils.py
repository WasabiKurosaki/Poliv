from settings import pixel_meter


def get_width_and_length(x_list: list, y_list: list) -> tuple:
    """
    Находим высоту и ширину для картинки в метрах
    """
    h_matrix = max(y_list) - min(y_list)
    w_matrix = max(x_list) - min(x_list)

    return pixel_meter * h_matrix, pixel_meter * w_matrix

# from pynput import keyboard
# def on_press(key):
#     try:
#         print(f'Нажата буквенно-цифровая клавиша: {key.char}')
#     except AttributeError:
#         print(f'Нажата специальная клавиша: {key}')

# def on_release(key):
#     print(f'{key} released')
#     if key == keyboard.Key.esc:
#         # Возврат False - остановит слушатель
#         return False

# # блок `with` слушает события до выхода
# # до остановки слушателя
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

# #...или неблокирующим способом:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()

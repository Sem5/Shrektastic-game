import pygame as pg

WIDTH = 600
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)


def is_win(turn: str, contents: dict[tuple[int, int], None | str]) -> bool:
    for y in range(3):
        if contents[0, y] == turn and contents[1, y] == turn and contents[2, y] == turn:
            return True
    for x in range(3):
        if contents[x, 0] == turn and contents[x, 1] == turn and contents[x, 2] == turn:
            return True
    if contents[0, 0] == turn and contents[1, 1] == turn and contents[2, 2] == turn:
        return True
    if contents[2, 0] == turn and contents[1, 1] == turn and contents[0, 2] == turn:
        return True
    return False


def draw_rectos(squares: dict[tuple[int, int], pg.Rect], window: pg.Surface):
    for x, y in squares:
        pg.draw.rect(window, 'cyan', squares[x, y], 5)


def draw_x(window: pg.Surface, square: pg.Rect):
    picter = pg.image.load('Shrektastic.jpg')
    picter = pg.transform.scale(picter, (WIDTH // 3, HEIGHT // 3))
    window.blit(picter, square.topleft)


def draw_o(window: pg.Surface, square: pg.Rect):
    picter = pg.image.load('Shrektastic_enemy.jpg')
    picter = pg.transform.scale(picter, (WIDTH // 3, HEIGHT // 3))
    window.blit(picter, square.topleft)


def get_sqwr_coords(x: int, y: int) -> tuple[int, int]:
    if x <= WIDTH // 3:  # First row check
        if y <= HEIGHT // 3:
            return 0, 0
        elif y <= (HEIGHT // 3) * 2:
            return 0, 1
        else:
            return 0, 2
    elif x <= WIDTH // 3 * 2:  # Second row check
        if y <= HEIGHT // 3:
            return 1, 0
        elif y <= (HEIGHT // 3) * 2:
            return 1, 1
        else:
            return 1, 2
    else:
        if y <= HEIGHT // 3:
            return 2, 0
        elif y <= (HEIGHT // 3) * 2:
            return 2, 1
        else:
            return 2, 2


def mainloop(squares: dict[tuple[int, int], pg.Rect], window: pg.Surface, contents: dict[tuple[int, int], None | str],
             x_plc_snd: pg.mixer.Sound, x_win_snd: pg.mixer.Sound, o_plc_snd: pg.mixer.Sound, o_win_snd: pg.mixer.Sound,
             draw_snd: pg.mixer.Sound, winpic_x: pg.Surface, winpic_o: pg.Surface):
    running = True
    click_count = 0
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pg.mouse.get_pos()
                    coordinates = get_sqwr_coords(x, y)
                    # if contents[coordinates] != 'x' and contents[coordinates] != 'y':
                    if not contents[coordinates]:
                        if click_count % 2 == 0:
                            draw_x(window, squares[coordinates])
                            draw_rectos(squares, window)
                            contents[coordinates] = 'x'
                            o_plc_snd.stop()
                            x_plc_snd.play()
                            if is_win('x', contents):
                                x_plc_snd.stop()
                                o_plc_snd.stop()
                                window.blit(winpic_x, (WIDTH / 4, HEIGHT / 3))
                                x_win_snd.play()
                                running = False
                        else:
                            draw_o(window, squares[coordinates])
                            draw_rectos(squares, window)
                            contents[coordinates] = 'o'
                            x_plc_snd.stop()
                            o_plc_snd.play()
                            if is_win('o', contents):
                                o_plc_snd.stop()
                                x_plc_snd.stop()
                                window.blit(winpic_o, (WIDTH / 4, HEIGHT / 3))
                                o_win_snd.play()
                                running = False
                        pg.display.flip()
                        click_count += 1
                        # Draw
                        if click_count == 9 and running:
                            x_plc_snd.stop()
                            o_plc_snd.stop()
                            draw_snd.play()
                            pg.time.wait(round(draw_snd.get_length() * 1000))
                            running = False
                        elif not running:
                            if click_count % 2 == 0:  # O
                                pg.time.wait(round(o_win_snd.get_length() * 1000))
                            else:
                                pg.time.wait(round(x_win_snd.get_length() * 1000))


def main():
    window = pg.display.set_mode(SIZE)
    # Fonts
    pg.font.init()
    font_x = pg.font.SysFont('comicsansms', 100)
    font_o = pg.font.SysFont('impact', 100)
    winpic_x = font_x.render('X won!', False, 'blue')
    winpic_o = font_o.render('O WON!', False, 'red')
    # Contents
    contents = {}
    # Sounds
    pg.mixer.init()
    draw_snd = pg.mixer.Sound('net43.mp3')
    x_plc_snd = pg.mixer.Sound('aga-poveril-nu-i-bredjatina.mp3')
    o_plc_snd = pg.mixer.Sound('sdoh.mp3')
    x_win_snd = pg.mixer.Sound('shreks-beastly-roar.mp3')
    o_win_snd = pg.mixer.Sound('loud-shrek.mp3')
    x_plc_snd.set_volume(1)
    o_win_snd.set_volume(1)
    x_win_snd.set_volume(1)
    o_plc_snd.set_volume(1)
    # Squares
    squares = {}
    side = WIDTH // 3
    for x in range(3):
        for y in range(3):
            square = pg.Rect(x * side, y * side, side, side)
            squares[x, y] = square
            contents[x, y] = None
    # Drawing
    picter = pg.image.load('Shrektastic.jpg')
    picter = pg.transform.scale(picter, SIZE)
    window.blit(picter, (0, 0))
    draw_rectos(squares, window)
    pg.display.flip()
    mainloop(squares, window, contents, x_plc_snd, x_win_snd, o_plc_snd, o_win_snd, draw_snd, winpic_x, winpic_o)


if __name__ == '__main__':
    main()

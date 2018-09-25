import pygame
import columns_p5

# Highscore: 7535

# I turned in columns_game, not this one.

class ColumnsState:
    def __init__(self):
        self.running = True
        self._state = columns_p5.GameState()

        self._RED = 10
        self._GREEN = 22
        self._BLUE = 150

        self._WIDTH = 500              # 318
        self._HEIGHT = 689             # 689

        self._FRAME_RATE = 20
        self._TICK_DELAY = 22

        self._faller = []
        self._next_faller = []

        self.score = 0

    def run(self) -> None:
        pygame.init()

        self._create_surface((self._WIDTH, self._HEIGHT))
        self._state.build_board()
        clock = pygame.time.Clock()

        self._background = pygame.image.load('underwater_bg.jpg')
        self._rotate_sound = pygame.mixer.Sound('rotate_soundv6.wav')
        self._landing_sound = pygame.mixer.Sound('landing_sound.wav')
        self._clear_sound = pygame.mixer.Sound('clear_sound.wav')
        self._bgm = pygame.mixer.music.load('columns_bgm.wav')


        pygame.mixer.music.play(-1)

        self._tick = 0
        self._fallers_past = 0

        while self.running:
            clock.tick(self._FRAME_RATE)
            self._tick += 1

            self._handle_events()

            if not self._state.game_over:
                if not self._state.faller_exists:
                    self._state.collapse_jewels()
                    self._state.check_matches()
                    if self._state.match_exists:
                        self._draw_grid()
                        pygame.display.flip()
                        self._clear_sound.play()
                        self._state.clear_matched()
                        self._state.collapse_jewels()
                        self.score += 137
                        print('Score: {}'.format(self.score))

                    else:
                        self._state.reset()
                        self._faller.clear()
                        self._state.get_random_column()
                        if self._fallers_past == 0:
                            self._next_faller = self._state.get_random_jewels()
                            self._faller.extend(self._state.get_random_jewels())
                        else:
                            self._faller.extend(self._next_faller)
                            self._next_faller = self._state.get_random_jewels()

                        self._fallers_past += 1


                else:
                    self._state.fall_faller(self._faller)
            else:
                self._end_game()

            if self._tick == self._TICK_DELAY:
                self._state.pass_time()
                if self._state.should_freeze:
                    self._landing_sound.play()
                self._tick = 0

            self._draw_surface()

        pygame.quit()



    def _create_surface(self, size: (int, int)) -> None:
        self.surface = pygame.display.set_mode(size, pygame.RESIZABLE)



    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._create_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._rotate_sound.play()
                    self._state.rotate_faller()

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self._state.shift_faller('>')
        if key[pygame.K_LEFT]:
            self._state.shift_faller('<')
        if key[pygame.K_DOWN]:
            if self._state.faller_exists and self._state.row < self._state.BOARD_ROWS:
                self._tick = 0
                self._state.pass_time()
                self._state._clear_jewel(self._state.row - 3, self._state.column)  # this doesn't fix the ghosting problem
                if self._state.should_freeze:
                    self._landing_sound.play()




    def _draw_surface(self):
        self.surface.fill((self._RED, self._GREEN, self._BLUE))

        self.surface.blit(pygame.transform.scale(self._background, (self._frac_to_pix_x(1), self._frac_to_pix_y(1))), (0, 0))

        self._draw_grid()
        pygame.display.flip()



    def _draw_grid(self):
        CELL_WIDTH_PIX = 52               # 53
        CELL_HEIGHT_PIX = 52              # 53
        CELL_WIDTH_FRAC = CELL_WIDTH_PIX / self._WIDTH
        CELL_HEIGHT_FRAC = CELL_HEIGHT_PIX / self._HEIGHT

        tl_x_frac = 0.135          # 0.18
        tl_y_frac = 0.01

        col_list = [2, 5, 8, 11, 14, 17]

        for row in range(self._state.BOARD_ROWS):
            for col in col_list:
                rect = pygame.Rect(self._frac_to_pix_x(tl_x_frac), self._frac_to_pix_y(tl_y_frac), self._frac_to_pix_x(CELL_WIDTH_FRAC), self._frac_to_pix_y(CELL_HEIGHT_FRAC))
                pygame.draw.rect(self.surface, (self._RED, self._GREEN, self._BLUE), rect)
                self._draw_faller(row, col, rect)
                tl_x_frac += CELL_WIDTH_FRAC
            tl_x_frac = 0.135     # 0.18
            tl_y_frac += CELL_HEIGHT_FRAC

        nf_tl_x = 0.8223
        nf_tl_y = 0.082

        for row in range(len(self._faller)):
            next_faller_rect = pygame.Rect(self._frac_to_pix_x(nf_tl_x), self._frac_to_pix_y(nf_tl_y), self._frac_to_pix_x(CELL_WIDTH_FRAC), self._frac_to_pix_y(CELL_HEIGHT_FRAC))
            pygame.draw.rect(self.surface, (self._RED, self._GREEN, self._BLUE), next_faller_rect)
            pygame.draw.rect(self.surface, (0, 0, 0), next_faller_rect, 2)
            self._draw_next_faller(self._next_faller, row, next_faller_rect)
            nf_tl_y += CELL_HEIGHT_FRAC

        # grid edge frac is 0.8039999999999999



    def _draw_faller(self, row, col, rect):
        board = self._state.board
        if board[row][col] == 'S':
            pygame.draw.ellipse(self.surface, (255, 0, 0), rect)   # red
        elif board[row][col] == 'T':
            pygame.draw.ellipse(self.surface, (214, 112, 29), rect)  # orange
        elif board[row][col] == 'V':
            pygame.draw.ellipse(self.surface, (248, 255, 53), rect)  # yellow
        elif board[row][col] == 'W':
            pygame.draw.ellipse(self.surface, (54, 112, 0), rect)  # green
        elif board[row][col] == 'X':
            pygame.draw.ellipse(self.surface, (53, 255, 224), rect)  # light blue
        elif board[row][col] == 'Y':
            pygame.draw.ellipse(self.surface, (53, 80, 255), rect)   # dark blue
        elif board[row][col] == 'Z':
            pygame.draw.ellipse(self.surface, (140, 53, 255), rect)  # purple

        if board[row][col - 1] == '|' and board[row][col + 1] == '|':
            pygame.draw.ellipse(self.surface, (124, 124, 124), rect, 4) # gray
        if board[row][col - 1] == '*' and board[row][col + 1] == '*':
            pygame.draw.ellipse(self.surface, (0, 0, 0), rect, 8)

        else:
            pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)



    def _draw_next_faller(self, list_of_jewels, row, rect):
        if list_of_jewels[row] == 'S':
            pygame.draw.ellipse(self.surface, (255, 0, 0), rect)  # red
        elif list_of_jewels[row] == 'T':
            pygame.draw.ellipse(self.surface, (214, 112, 29), rect)  # orange
        elif list_of_jewels[row] == 'V':
            pygame.draw.ellipse(self.surface, (248, 255, 53), rect)  # yellow
        elif list_of_jewels[row] == 'W':
            pygame.draw.ellipse(self.surface, (54, 112, 0), rect)  # green
        elif list_of_jewels[row] == 'X':
            pygame.draw.ellipse(self.surface, (53, 255, 224), rect)  # light blue
        elif list_of_jewels[row] == 'Y':
            pygame.draw.ellipse(self.surface, (53, 80, 255), rect)  # dark blue
        elif list_of_jewels[row] == 'Z':
            pygame.draw.ellipse(self.surface, (140, 53, 255), rect)  # purple



    def _frac_to_pix_x(self, frac_x: float):
        return self._frac_to_pix(frac_x, self.surface.get_width())


    def _frac_to_pix_y(self, frac_y: float):
        return self._frac_to_pix(frac_y, self.surface.get_height())


    def _frac_to_pix(self, frac: float, max_pixel: int):
        return int(frac * max_pixel)



    def _end_game(self):
        self.running = False



if __name__ == '__main__':
    ColumnsState().run()

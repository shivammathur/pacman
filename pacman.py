import pygame


class Color:
    """
    Class to store hex values for colors/
    """
    def __init__(self):
        """
        Constructor Function
        """
        self.black = (0, 0, 0)
        self.grey = (100, 100, 100)
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.purple = (255, 0, 255)
        self.yellow = (255, 255, 0)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        """
        Constructor function
        :param x:
        :type x:
        :param y:
        :type y:
        :param width:
        :type width:
        :param height:
        :type height:
        :param color:
        :type color:
        """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


class Block(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """

    def __init__(self, color, width, height):
        """
        Constructor. Pass in the color of the block and its x and y position
        :param color:
        :type color:
        :param width:
        :type width:
        :param height:
        :type height:
        """

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.color = Color()
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color.white)
        self.image.set_colorkey(self.color.white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls
    """

    change_x = 0
    change_y = 0

    def __init__(self, x, y, filename):
        """
        Constructor function
        :param x:
        :type x:
        :param y:
        :type y:
        :param filename:
        :type filename:
        """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    def prev_direction(self):
        """
        Clear the speed of the player
        """
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    def change_speed(self, x, y):
        """
        Change the speed of the player
        :param x:
        :type x:
        :param y:
        :type y:
        """
        self.change_x += x
        self.change_y += y

    def update(self, walls, gate):
        """
        Find a new position for the player
        :param walls: 
        :type walls: 
        :param gate: 
        :type gate: 
        """

        # Get the old position, in case we need to go back to it
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y

        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y

        if gate:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


class Ghost(Player):
    """
    Class to handle ghosts
    """

    def ghost_change_speed(self, direction_list, ghost, turn, steps, l):
        """
        Change the speed of the ghost
        :param direction_list: 
        :type direction_list: 
        :param ghost: 
        :type ghost: 
        :param turn: 
        :type turn: 
        :param steps: 
        :type steps: 
        :param l: 
        :type l: 
        :return: 
        :rtype: 
        """
        try:
            z = direction_list[turn][2]
            if steps < z:
                self.change_x = direction_list[turn][0]
                self.change_y = direction_list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == 'ghost_four':
                    turn = 2
                else:
                    turn = 0
                self.change_x = direction_list[turn][0]
                self.change_y = direction_list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


class Game:
    """
    Class to run the game.
    """

    def __init__(self):
        """
        Constructor Function
        """

        # This is a list of walls. Each is in the form [x, y, width, height]
        self.walls = [
            [0, 0, 6, 600],
            [0, 0, 600, 6],
            [0, 600, 606, 6],
            [600, 0, 6, 606],
            [300, 0, 6, 66],
            [60, 60, 186, 6],
            [360, 60, 186, 6],
            [60, 120, 66, 6],
            [60, 120, 6, 126],
            [180, 120, 246, 6],
            [300, 120, 6, 66],
            [480, 120, 66, 6],
            [540, 120, 6, 126],
            [120, 180, 126, 6],
            [120, 180, 6, 126],
            [360, 180, 126, 6],
            [480, 180, 6, 126],
            [180, 240, 6, 126],
            [180, 360, 246, 6],
            [420, 240, 6, 126],
            [240, 240, 42, 6],
            [324, 240, 42, 6],
            [240, 240, 6, 66],
            [240, 300, 126, 6],
            [360, 240, 6, 66],
            [0, 300, 66, 6],
            [540, 300, 66, 6],
            [60, 360, 66, 6],
            [60, 360, 6, 186],
            [480, 360, 66, 6],
            [540, 360, 6, 186],
            [120, 420, 366, 6],
            [120, 420, 6, 66],
            [480, 420, 6, 66],
            [180, 480, 246, 6],
            [300, 480, 6, 66],
            [120, 540, 126, 6],
            [360, 540, 126, 6],
        ]

        self.ghost_one_directions = [
            [0, -30, 4],
            [15, 0, 9],
            [0, 15, 11],
            [-15, 0, 23],
            [0, 15, 7],
            [15, 0, 3],
            [0, -15, 3],
            [15, 0, 19],
            [0, 15, 3],
            [15, 0, 3],
            [0, 15, 3],
            [15, 0, 3],
            [0, -15, 15],
            [-15, 0, 7],
            [0, 15, 3],
            [-15, 0, 19],
            [0, -15, 11],
            [15, 0, 9],
        ]

        self.ghost_two_directions = [
            [0, -15, 4],
            [15, 0, 9],
            [0, 15, 11],
            [15, 0, 3],
            [0, 15, 7],
            [-15, 0, 11],
            [0, 15, 3],
            [15, 0, 15],
            [0, -15, 15],
            [15, 0, 3],
            [0, -15, 11],
            [-15, 0, 3],
            [0, -15, 11],
            [-15, 0, 3],
            [0, -15, 3],
            [-15, 0, 7],
            [0, -15, 3],
            [15, 0, 15],
            [0, 15, 15],
            [-15, 0, 3],
            [0, 15, 3],
            [-15, 0, 3],
            [0, -15, 7],
            [-15, 0, 3],
            [0, 15, 7],
            [-15, 0, 11],
            [0, -15, 7],
            [15, 0, 5],
        ]

        self.ghost_three_directions = [
            [30, 0, 2],
            [0, -15, 4],
            [15, 0, 10],
            [0, 15, 7],
            [15, 0, 3],
            [0, -15, 3],
            [15, 0, 3],
            [0, -15, 15],
            [-15, 0, 15],
            [0, 15, 3],
            [15, 0, 15],
            [0, 15, 11],
            [-15, 0, 3],
            [0, -15, 7],
            [-15, 0, 11],
            [0, 15, 3],
            [-15, 0, 11],
            [0, 15, 7],
            [-15, 0, 3],
            [0, -15, 3],
            [-15, 0, 3],
            [0, -15, 15],
            [15, 0, 15],
            [0, 15, 3],
            [-15, 0, 15],
            [0, 15, 11],
            [15, 0, 3],
            [0, -15, 11],
            [15, 0, 11],
            [0, 15, 3],
            [15, 0, 1],
        ]

        self.ghost_four_directions = [
            [-30, 0, 2],
            [0, -15, 4],
            [15, 0, 5],
            [0, 15, 7],
            [-15, 0, 11],
            [0, -15, 7],
            [-15, 0, 3],
            [0, 15, 7],
            [-15, 0, 7],
            [0, 15, 15],
            [15, 0, 15],
            [0, -15, 3],
            [-15, 0, 11],
            [0, -15, 7],
            [15, 0, 3],
            [0, -15, 11],
            [15, 0, 9],
        ]

        self.color = Color()
        # Call this function so the Pygame library can initialize itself
        pygame.init()

        # Create an 606x606 sized screen
        self.screen = pygame.display.set_mode([606, 606])

        # Set the title of the window
        pygame.display.set_caption('Pacman')

        # Create a surface we can draw on
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(self.color.black)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 30)
        self.all_sprites_list = None

    def setup_walls(self):
        """
        Make the walls. (x_pos, y_pos, width, height)
        :return:
        :rtype:
        """
        wall_list = pygame.sprite.RenderPlain()

        # Loop through the list. Create the wall, add it to the list
        for item in self.walls:
            wall = Wall(item[0], item[1], item[2], item[3], self.color.grey)
            wall_list.add(wall)
            self.all_sprites_list.add(wall)

        # return our new list
        return wall_list

    def setup_gate(self):
        """
        Add gates in the walls
        :return:
        :rtype:
        """
        gate = pygame.sprite.RenderPlain()
        gate.add(Wall(282, 242, 42, 2, self.color.white))
        self.all_sprites_list.add(gate)
        return gate

    def start_game(self):
        """
        start the game
        """

        pl = len(self.ghost_one_directions) - 1
        bl = len(self.ghost_two_directions) - 1
        il = len(self.ghost_three_directions) - 1
        cl = len(self.ghost_four_directions) - 1

        # default locations for Pacman and ghosts
        w = 303 - 16  # Width
        p_h = 7 * 60 + 19
        m_h = 4 * 60 + 19
        b_h = 3 * 60 + 19
        i_w = 303 - 16 - 32
        c_w = 303 + 32 - 16

        self.all_sprites_list = pygame.sprite.RenderPlain()
        block_list = pygame.sprite.RenderPlain()
        ghost_list = pygame.sprite.RenderPlain()
        pacman_collide = pygame.sprite.RenderPlain()
        wall_list = self.setup_walls()
        gate = self.setup_gate()

        p_turn = 0
        p_steps = 0

        b_turn = 0
        b_steps = 0

        i_turn = 0
        i_steps = 0

        c_turn = 0
        c_steps = 0

        # Create the player paddle object
        pacman = Player(w, p_h, 'images/pacman.png')
        self.all_sprites_list.add(pacman)
        pacman_collide.add(pacman)

        ghost_two = Ghost(w, b_h, 'images/red.png')
        ghost_list.add(ghost_two)
        self.all_sprites_list.add(ghost_two)

        ghost_one = Ghost(w, m_h, 'images/pink.png')
        ghost_list.add(ghost_one)
        self.all_sprites_list.add(ghost_one)

        ghost_three = Ghost(i_w, m_h, 'images/blue.png')
        ghost_list.add(ghost_three)
        self.all_sprites_list.add(ghost_three)

        ghost_four = Ghost(c_w, m_h, 'images/yellow.png')
        ghost_list.add(ghost_four)
        self.all_sprites_list.add(ghost_four)

        # Draw the grid
        for row in range(19):
            for column in range(19):
                if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                    continue
                else:
                    block = Block(self.color.yellow, 4, 4)

                    # Set a random location for the block
                    block.rect.x = 30 * column + 6 + 26
                    block.rect.y = 30 * row + 6 + 26

                    b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                    p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
                    if b_collide:
                        continue
                    elif p_collide:
                        continue
                    else:
                        # Add the block to the list of objects
                        block_list.add(block)
                        self.all_sprites_list.add(block)

        bll = len(block_list)
        score = 0
        done = False
        while not done:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pacman.change_speed(-30, 0)
                    if event.key == pygame.K_RIGHT:
                        pacman.change_speed(30, 0)
                    if event.key == pygame.K_UP:
                        pacman.change_speed(0, -30)
                    if event.key == pygame.K_DOWN:
                        pacman.change_speed(0, 30)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pacman.change_speed(30, 0)
                    if event.key == pygame.K_RIGHT:
                        pacman.change_speed(-30, 0)
                    if event.key == pygame.K_UP:
                        pacman.change_speed(0, 30)
                    if event.key == pygame.K_DOWN:
                        pacman.change_speed(0, -30)

            pacman.update(wall_list, gate)
            returned = ghost_one.ghost_change_speed(self.ghost_one_directions, False, p_turn, p_steps, pl)
            p_turn = returned[0]
            p_steps = returned[1]
            ghost_one.ghost_change_speed(self.ghost_one_directions, False, p_turn, p_steps, pl)
            ghost_one.update(wall_list, False)

            returned = ghost_two.ghost_change_speed(self.ghost_two_directions, False, b_turn, b_steps, bl)
            b_turn = returned[0]
            b_steps = returned[1]
            ghost_two.ghost_change_speed(self.ghost_two_directions, False, b_turn, b_steps, bl)
            ghost_two.update(wall_list, False)

            returned = ghost_three.ghost_change_speed(self.ghost_three_directions, False, i_turn, i_steps, il)
            i_turn = returned[0]
            i_steps = returned[1]
            ghost_three.ghost_change_speed(self.ghost_three_directions, False, i_turn, i_steps, il)
            ghost_three.update(wall_list, False)

            returned = ghost_four.ghost_change_speed(self.ghost_four_directions, 'ghost_four', c_turn, c_steps, cl)
            c_turn = returned[0]
            c_steps = returned[1]
            ghost_four.ghost_change_speed(self.ghost_four_directions, 'ghost_four', c_turn, c_steps, cl)
            ghost_four.update(wall_list, False)

            # See if the pacman block has collided with anything.
            blocks_hit_list = pygame.sprite.spritecollide(pacman, block_list, True)

            # Check the list of collisions.
            if len(blocks_hit_list) > 0:
                score += len(blocks_hit_list)

            self.screen.fill(self.color.black)

            wall_list.draw(self.screen)
            gate.draw(self.screen)
            self.all_sprites_list.draw(self.screen)
            ghost_list.draw(self.screen)

            text = self.font.render(str(score) + '/' + str(bll), True, self.color.white)
            self.screen.blit(text, [270, 254])

            if score == bll:
                self.do_next(
                    'Congratulations, you won!',
                    145,
                    block_list,
                    ghost_list,
                    pacman_collide,
                    wall_list,
                    gate,
                )
                return

            ghost_hit_list = pygame.sprite.spritecollide(pacman, ghost_list, False)

            if ghost_hit_list:
                self.do_next(
                    'Game Over',
                    235,
                    block_list,
                    ghost_list,
                    pacman_collide,
                    wall_list,
                    gate,
                )
                return

            pygame.display.flip()

            self.clock.tick(10)

    def do_next(self, message, left, block_list, ghost_list, pacman_collide, wall_list, gate):
        """
        Go to next configuration in the game
        :param message:
        :type message:
        :param left:
        :type left:
        :param block_list:
        :type block_list:
        :param ghost_list:
        :type ghost_list:
        :param pacman_collide:
        :type pacman_collide:
        :param wall_list:
        :type wall_list:
        :param gate:
        :type gate:
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    if event.key == pygame.K_RETURN:
                        del self.all_sprites_list
                        del block_list
                        del ghost_list
                        del pacman_collide
                        del wall_list
                        del gate
                        self.start_game()
                        return

            # Grey background
            w_surface = pygame.Surface((400, 200))  # the size of your rect
            w_surface.fill((255, 255, 255))  # this fills the entire surface
            self.screen.blit(w_surface, (100, 200))  # (0,0) are the top-left coordinates

            # Won or lost
            text1 = self.font.render(message, True, self.color.black)
            self.screen.blit(text1, [left, 233])

            text2 = self.font.render('To play again, press ENTER.', True, self.color.black)
            self.screen.blit(text2, [135, 300])
            text3 = self.font.render('To quit, press ESCAPE.', True, self.color.black)
            self.screen.blit(text3, [165, 340])

            pygame.display.flip()
            self.clock.tick(10)


if __name__ == '__main__':
    # main function
    game = Game()
    game.start_game()
    pygame.quit()

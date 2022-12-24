import pygame


class imgButton:
    def __init__(self, image, width, height, pos, hover_transparency, align='topleft'):
        if hover_transparency <= 1:
            self.alpha = hover_transparency * 255
        else:
            self.alpha = hover_transparency
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        if align == 'topleft' or align == 'top_left':
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        elif align == 'bottomleft' or align == 'bottom_left':
            self.rect = self.image.get_rect(bottomleft=(self.x, self.y))
        elif align == 'topright' or align == 'top_right':
            self.rect = self.image.get_rect(topright=(self.x, self.y))
        elif align == 'bottomright' or align == 'bottom_right':
            self.rect = self.image.get_rect(bottomright=(self.x, self.y))
        else:
            self.rect = self.image.get_rect(center=(self.x, self.y))
        self.clicked = False

    def checkForInput(self):
        pos = pygame.mouse.get_pos()
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if self.rect.collidepoint(pos):
            self.image.set_alpha(self.alpha)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


class rect:
    def __init__(self, width, height, base_colour, hover_colour, alpha, pos, align='top_left'):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        if alpha <= 1:
            self.alpha = alpha * 255
        else:
            self.alpha = alpha
        self.base_colour = base_colour
        self.hover_colour = hover_colour
        if align == 'centre' or align == 'center':
            self.x = self.x - width // 2
            self.y = self.y - height // 2
        if align == 'bottomleft' or align == 'bottom_left' or align == 'bottom left':
            self.y = self.y - height
        if align == 'topright' or align == 'top_right' or align == 'top right':
            self.x = self.x - width
        if align == 'bottomright' or align == 'bottom_right' or align == 'bottom right':
            self.x = self.x - width
            self.y = self.y - height
        self.rect = pygame.Surface((self.width, self.height))
        self.rect.set_alpha(self.alpha)
        self.rect.fill(self.base_colour)
        self.clicked = False

    def checkForInput(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        if self.x <= x <= (self.x + self.width) and self.y <= y <= (self.y + self.height):
            return True
        return False

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        # Check mouseover and clicked conditions
        if self.x <= x <= (self.x + self.width) and self.y <= y <= (self.y + self.height):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if self.x <= x <= (self.x + self.width) and self.y <= y <= (self.y + self.height):
            self.rect.fill(self.hover_colour)
        else:
            self.rect.fill(self.base_colour)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.rect, (self.x, self.y))

        return action


class textRect:
    def __init__(self, text, font, base_colour, hover_colour, pos, align='centre'):
        self.x = pos[0]
        self.y = pos[1]
        self.base_colour = base_colour
        self.hover_colour = hover_colour
        self.text_input = str(text)
        self.font = font
        self.text = self.font.render(self.text_input, True, self.base_colour)
        if align == 'topleft' or align == 'top_left':
            self.rect = self.text.get_rect(topleft=(self.x, self.y))
        elif align == 'bottomleft' or align == 'bottom_left':
            self.rect = self.text.get_rect(bottomleft=(self.x, self.y))
        elif align == 'topright' or align == 'top_right':
            self.rect = self.text.get_rect(topright=(self.x, self.y))
        elif align == 'bottomright' or align == 'bottom_right':
            self.rect = self.text.get_rect(bottomright=(self.x, self.y))
        else:
            self.rect = self.text.get_rect(center=(self.x, self.y))
        self.clicked = False

    def checkForInput(self):
        pos = pygame.mouse.get_pos()
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if self.rect.collidepoint(pos):
            self.text = self.font.render(self.text_input, True, self.hover_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.text, (self.rect.x, self.rect.y))

        return action


class textGridItem:
    def __init__(self, text, font, colour, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.colour = colour
        self.text_input = str(text)
        self.font = font
        self.text = self.font.render(self.text_input, True, self.colour)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.text, self.rect)


class imageGridItem:
    def __init__(self, image, width, height, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = width
        self.height = height
        self.image = pygame.transform.smoothscale(image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)


def format_position(pos, width, height, align='centre'):
    """Turns position from its alignment to topleft alignment"""
    x = pos[0]
    y = pos[1]
    if align == 'centre' or align == 'center':
        x = x - width // 2
        y = y - height // 2
    elif align == 'bottomleft' or align == 'bottom_left' or align == 'bottom left':
        y = y - height
    elif align == 'topright' or align == 'top_right' or align == 'top right':
        x = x - width
    elif align == 'bottomright' or align == 'bottom_right' or align == 'bottom right':
        x = x - width
        y = y - height
    elif align == 'midleft' or align == 'mid_left' or align == 'mid left':
        y = y - height // 2
    elif align == 'midright' or align == 'mid_right' or align == 'mid right':
        x = x - width
        y = y - height // 2
    elif align == 'midtop' or align == 'mid_top' or align == 'mid top':
        x = x - width // 2
    elif align == 'midbottom' or align == 'mid_bottom' or align == 'mid bottom':
        x = x - width // 2
        y = y - height

    return [x, y]

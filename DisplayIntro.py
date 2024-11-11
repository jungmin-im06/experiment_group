import pygame

# Initialize Pygame
def display_intro():

    # putting text on the screen
    def render_text(text, font, color, position):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, position)
        return text_surface.get_rect(topleft=position)
    
    # wrapping text to fit within display
    def wrap_text(text, font, max_width):

        words = text.split(' ')
        lines = []
        current_line = ''

        # adding words into a string until they cannot fit in one line
        for word in words:
            test_line = current_line + word + ' '
            # Check the width of the test_line
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '

        # adding rest of the remaining words
        if current_line != '':
            lines.append(current_line)

        return lines
    
    # initializing pygame
    pygame.init()

    # setting values such as colors and size of display
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (0, 100, 255)

    width = 1200
    height = 600

    # Set up the display to be full screen
    computer = pygame.display.Info()
    screen_width, screen_height = computer.current_w, computer.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.NOFRAME)
    pygame.display.set_caption("Start Display")

    font = pygame.font.Font('resource/Nanum/NanumGothicCoding-Regular.ttf', 30)

    # Display instructions
    instructions_text_1 = "귀하는 60분 정도 분량의 동영상 1개를 시청해야 합니다. 해당 동영상은 연세대학교의 법정의무 장애인식개선교육입니다."
    instructions_text_2 = "모든 실험참가자의 학습시간은 70분으로 고정되어 있습니다. 따라서 누적 영상 재생 시간이 70분에 도달하면 자동으로 영상이 중단됩니다. 시간에 유의하여 영상을 시청해주시기 바랍니다."
    instructions_text_3 = "영상을 중지하려면 스페이스 바를, 15초 이전으로 돌아갈려면 왼쪽방향키를 눌러주세요."
    instructions_text_4 = "동영상을 시청하시려면 아래의 시작 버튼을 눌러주세요."

    text_lines = []
    text_lines.append(wrap_text(instructions_text_1, font, width))
    text_lines.append(wrap_text(instructions_text_2, font, width))
    text_lines.append(wrap_text(instructions_text_3, font, width))
    text_lines.append(wrap_text(instructions_text_4, font, width))
    
    button_text = "시작"
    button_x = screen_width/2 - font.size(button_text)[0]/2

    yonsei = pygame.image.load('resource/image/Yonsei_Uni_Logo.png')
    yonsei = pygame.transform.smoothscale(yonsei, (100,100))
    yonsei_x = screen_width/2 - yonsei.get_width()/2

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button area
                if button_rect.collidepoint(event.pos):
                    return True

        # Fill the screen with white background
        screen.fill(WHITE)

        screen.blit(yonsei, (yonsei_x, (screen_height/2)-height/2))

        y_position = (screen_height/2)-height/2 + yonsei.get_height() + 50

        # Putting the texts to fit the display
        for text_line in text_lines:
            
            # drawing each line
            for i, line in enumerate(text_line):
                line_surface = font.render(line, True, BLACK)
                screen.blit(line_surface, ((screen_width/2)-width/2, y_position))

                y_position += font.get_height()+1

            y_position += font.get_height()

        # Draw button
        button_rect = render_text(button_text, font, WHITE, (button_x, y_position))

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if the mouse is over the button
        if button_rect.collidepoint(mouse_pos):
            button_color = LIGHT_BLUE  # Change to lighter color on hover
        else:
            button_color = BLUE  # Default button color

        pygame.draw.rect(screen, button_color, button_rect.inflate(20, 10))
        render_text(button_text, font, WHITE, button_rect.topleft)

        pygame.display.flip()


if __name__ == "__main__":
    display_intro()

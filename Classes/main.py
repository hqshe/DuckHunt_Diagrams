import pygame
import Settings
import Gun
import Menu
import GameContext

def main():
    pygame.init()
    settings = Settings()
    context = GameContext(settings)
    gun = Gun(context)
    menu = Menu(context)
    pygame.mixer.music.play()
    run = True
    context.level = 0
    context.generate_enemy_coordinates()
    while run:
        context.timer.tick(settings.fps)

        if context.level != 0:
            if context.counter < 60:
                context.counter += 1
            else:
                context.counter = 1
                context.time_passed += 1
                if context.mode == 2:
                    context.time_remaining -= 1

        context.screen.fill('black')
        context.screen.blit(context.bgs[context.level - 1], (0, 0))
        context.screen.blit(context.banners[context.level - 1], (0, context.HEIGHT - 200))
        menu.draw()

        if context.level == 1:
            context.target_boxes = context.draw_level(context.one_coords)
            context.one_coords = context.move_level()
            if context.shot:
                context.one_coords = gun.check_shot(context.target_boxes, context.one_coords)
                context.shot = False

        elif context.level == 2:
            context.target_boxes = context.draw_level(context.two_coords)
            context.two_coords = context.move_level()
            if context.shot:
                context.two_coords = gun.check_shot(context.target_boxes, context.two_coords)
                context.shot = False

        elif context.level == 3:
            context.target_boxes = context.draw_level(context.three_coords)
            context.three_coords = context.move_level()
            if context.shot:
                context.three_coords = gun.check_shot(context.target_boxes, context.three_coords)
                context.shot = False

        if context.level > 0:
            gun.draw_gun()
            context.draw_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()

                if (0 < mouse_position[0] < context.WIDTH) and (0 < mouse_position[1] < context.HEIGHT - 200):
                    context.shot = True
                    context.total_shots += 1
                    if context.mode == 1:
                        context.ammo -= 1

                if (670 < mouse_position[0] < 860) and (660 < mouse_position[1] < 715):
                    context.resume_level = context.level
                    context.pause = True
                    context.clicked = True

                if (670 < mouse_position[0] < 860) and (715 < mouse_position[1] < 760):
                    context.menu = True
                    pygame.mixer.music.play()
                    context.clicked = True
                    context.new_coords = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and context.clicked:
                context.clicked = False

        if context.level > 0:
            if context.target_boxes == [[], [], []] and context.level < 3:
                context.level += 1
            if (context.level == 3 and context.target_boxes == [[], [], [], []]) or (
                    context.mode == 1 and context.ammo == 0) or (
                    context.mode == 2 and context.time_remaining == 0):
                context.new_coords = True
                pygame.mixer.music.play()
                if context.mode == 0:
                    if context.time_passed < context.best_freeplay or context.best_freeplay == 0:
                        context.best_freeplay = context.time_passed
                        context.write_values = True
                if context.mode == 1:
                    if context.points > context.best_ammo:
                        context.best_ammo = context.points
                        context.write_values = True
                if context.mode == 2:
                    if context.points > context.best_timed:
                        context.best_timed = context.points
                        context.write_values = True
                context.game_over = True

        if context.write_values:
            file = open('../high_scores.txt', 'w')
            file.write(f'{context.best_freeplay}\n{context.best_ammo}\n{context.best_timed}')
            file.close()
            context.write_values = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

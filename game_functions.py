import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import json


def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:  # 发射子弹
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # 快捷键退出
        update_history(stats)
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()  # 更新子弹的位置
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)  # 删除消失的子弹
            # print(len(bullets))
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 子弹和alien的碰撞检测,collisions是子弹-alien字典
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:  # 删除现有子弹创建新的外星人
        bullets.empty()
        ai_settings.increase_speed()

        # 全部alien消灭后提高一个等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)


def fire_bullets(ai_settings, screen, ship, bullets):  # 若没有达到限制，就发射子弹
    if len(bullets) <= ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)  # 创建新子弹，将它添加到bullets中
        bullets.add(new_bullet)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):  # 更新所有外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测alien和飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):  # 检查有无外星人到达底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):  # 响应飞船被撞击，或者外星人触底，称为游戏重置
    if stats.ship_left > 0:
        stats.ship_left -= 1
        # 更新记分牌
        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)  # 创建一群新的外星人
        ship.center_ship()  # 飞船重置在底部中间
        sleep(0.5)  # 单位:s
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)  # 游戏重置，显示光标


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):  # 创建一群外星人
            creat_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    # 计算一行可以容纳多少alien
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_history(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()  # 单机paly开始新游戏时，重置游戏信息
        stats.game_active = True

        # 重置记分牌
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人和子弹，生成新的alien，飞船居中
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 隐藏光标
        pygame.mouse.set_visible(False)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_high_score(stats, sb):
    # 是否产生了更新最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)  # 每次循环填充背景色,背景颜色:浅灰
    for bullet in bullets.sprites():  # 每次绘制组里的子弹
        bullet.draw_bullet()
    ship.blitme()  # 每次在新位置绘制飞船
    aliens.draw(screen)  # 每次重新绘制外星人
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()  # 如果游戏处于非活动状态，绘制按钮
    pygame.display.flip()  # 让最近的绘制屏幕可见:每执行一个while都会绘制一个屏幕擦去旧屏幕


def update_history(stats):
    data = "data.json"
    with open(data, 'w') as db:
        json.dump(stats.high_score, db)
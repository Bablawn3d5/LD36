// Copyright 2016 Bablawn3d5

#pragma once

#include <entityx/entityx.h>
#include <SFML/Graphics.hpp>
#include <string>

struct Renderable {
    std::string texture_name;
    std::string sprite_name;
    // HACK(SMA):This doesn't work in metaregister for whatever reason.
    //uint8_t r = 200, g = 0,b = 200, a = 255;
    uint32_t r = 200, g = 0,b = 200, a = 255;
    sf::Vector2f scale{1.f,1.f};
    std::string font_name;
    std::string font_string;
    uint32_t font_size = 30;
    bool isDitry = true;

    std::shared_ptr<sf::Drawable> drawable;
    std::weak_ptr<sf::Transformable> transform;
    // TODO(SMA): Animation data to feed into the renderer
    // std::weak_ptr<Animated> animation;
};

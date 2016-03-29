local kb = libs.keyboard;

-- Documentation
-- http://www.unifiedremote.com/api

-- Keyboard Library
-- http://www.unifiedremote.com/api/libs/keyboard

actions.move_left = function ()
   kb.stroke("leftarrow");
end
actions.move_right = function ()
   kb.stroke("rightarrow");
end
actions.rotate_cannon_left = function ()
   kb.stroke("downarrow");
end
actions.rotate_cannon_right = function ()
   kb.stroke("uparrow");
end
actions.power_down = function ()
   kb.stroke("pagedown");
end
actions.power_up = function ()
   kb.stroke("pageup");
end
actions.weapon_prev = function ()
   kb.stroke("q");
end
actions.weapon_next = function ()
   kb.stroke("w");
end
actions.fire = function ()
   kb.stroke("space");
end

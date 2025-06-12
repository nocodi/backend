import black
from django.conf import settings
from rest_framework.exceptions import ValidationError

from bot.models import Bot
from component.telegram.models import Component


def generate_code(bot: Bot) -> str:
    components = Component.objects.filter(
        bot_id=bot.id,
        component_type=Component.ComponentType.TRIGGER,
    )
    bot_component_codes = []
    raw_state_check = None
    for component in components:
        if component.component_content_type.model != "onmessage":
            raise ValidationError(
                "Only OnMessage trigger components are supported. you requested {component.__class__.__name__}",
            )

        for next_component in component.get_all_next_components():
            object = next_component.component_content_type.model_class().objects.get(
                pk=next_component.pk,
            )
            code_result = object.generate_code()
            if isinstance(code_result, tuple):
                keyboard, callback_code = code_result
                if keyboard:
                    bot_component_codes.append(keyboard)
                if callback_code:
                    bot_component_codes.append(callback_code)
            else:
                if "raw_state" in code_result:
                    raw_state_check = code_result
                else:
                    bot_component_codes.append(code_result)

    if raw_state_check:
        bot_component_codes.append(raw_state_check)

    with open("bot/bot_templates/main.txt") as f:
        base = f.read()

    code = base.format(
        FUNCTION_CODES="\n\n".join(bot_component_codes),
        TOKEN=bot.token,
        BASE_URL=settings.BALE_API_URL,
    )
    return black.format_str(code, mode=black.Mode())

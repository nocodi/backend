from django.conf import settings
from rest_framework.exceptions import ValidationError

from bot.models import Bot
from component.telegram.models import Component


def generate_code(bot: Bot) -> str:
    components = Component.objects.filter(
        bot_id=bot.id,
        component_type=Component.ComponentType.TRIGGER,
    )
    bot_component_codes = ""
    for component in components:
        if component.component_content_type.model != "onmessage":
            raise ValidationError(
                "Only OnMessage trigger components are supported. you requested {component.__class__.__name__}",
            )

        for next_component in component.get_all_next_components():
            # if next_component.id == component.id:
            #     continue
            object = next_component.component_content_type.model_class().objects.get(
                pk=next_component.pk,
            )
            bot_component_codes += object.generate_code()
            bot_component_codes += "\n" * 2

    with open("bot/bot_templates/main.txt") as f:
        base = f.read()
    code = base.format(
        FUNCTION_CODES=bot_component_codes,
        TOKEN=bot.token,
        BASE_URL=settings.BALE_API_URL,
    )

    return code

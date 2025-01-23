from loader import dp
from .Admin import IsAdmin
from .Group import IsGroup
from .Group import IsPrivateChatFilter
from .Group import IsAdmin_group_call
from .Chat import IsPrivate
from .Group import IsAdmin_group



if __name__ == 'filters':
    dp.filters_factory.bind(IsAdmin_group)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivateChatFilter)
    dp.filters_factory.bind(IsAdmin_group_call)
    dp.filters_factory.bind(IsPrivate)
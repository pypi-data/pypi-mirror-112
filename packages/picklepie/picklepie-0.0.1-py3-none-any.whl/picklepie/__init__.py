from pkg_resources import get_distribution as __dist

def version () :
    return __dist('picklepie').version

from .site import SiteConfigSchema
from .tools import HasKey, Nullable, Url, List

SiteEnableSchema = List(SiteConfigSchema)
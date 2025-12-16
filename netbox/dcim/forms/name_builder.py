from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from netbox_custom_objects.models import CustomObjectType
from dcim.models import Site, Location
from utilities.forms.fields import DynamicModelChoiceField

config = settings.PLUGINS_CONFIG.get("custom_object_types_name", {})

System = CustomObjectType.objects.get(name=config.get("system", "systeme")).get_model()
SubSystem = CustomObjectType.objects.get(
    name=config.get("subsystem", "sous_systeme")
).get_model()
Component = CustomObjectType.objects.get(
    name=config.get("component", "composant")
).get_model()


__all__ = ("NameBuilderForm",)


class NameBuilderForm(forms.Form):
    """
    A form to build device names based on site and location selections.
    """

    nb_site = DynamicModelChoiceField(
        label=_("Site"),
        queryset=Site.objects.all(),
    )
    nb_location = DynamicModelChoiceField(
        label=_("Location"),
        queryset=Location.objects.all(),
        query_params={"site_id": "$nb_site"},
    )
    nb_system = DynamicModelChoiceField(
        queryset=System.objects.all(),
        label=_("System"),
    )
    nb_subsystem = DynamicModelChoiceField(
        queryset=SubSystem.objects.all(),
        label=_("Subsystem"),
        query_params={"system": "$nb_system"},
    )
    nb_component = DynamicModelChoiceField(
        queryset=Component.objects.all(),
        label=_("Component"),
        query_params={"system": "$nb_system", "subsystem": "$nb_subsystem"},
    )
    nb_name = forms.CharField(
        label=_("Name"),
    )

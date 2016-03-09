from django.contrib import admin

# Register your models here.

from chemical.models import Atom, Substance, Reaction

class AtomAdmin(admin.ModelAdmin):
  fields = ['atom_number', 'symbol','atom_mass',  'name', 'name_latin']
  list_display = ('atom_number', 'symbol', 'atom_mass', 'name', 'name_latin')

admin.site.register(Atom, AtomAdmin)


class SubstanceAdmin(admin.ModelAdmin):
  fields = ['name', 'charge', 'is_radical', 'formula_brutto']
  list_display = ('id_substance',  'name',  'charge', 'is_radical', 'formula_brutto')

admin.site.register(Substance, SubstanceAdmin)

class ReactionAdmin(admin.ModelAdmin):
  fields = ['name',  'is_favorite', 'is_stationary', 'is_isothermal' ]
  list_display = ('id_reaction',  'name', 'is_favorite', 'is_stationary', 'is_isothermal' )

admin.site.register(Reaction, ReactionAdmin)

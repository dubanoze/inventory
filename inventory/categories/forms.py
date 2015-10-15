# -*- coding: utf-8 -*-
#
# inventory/categories/forms.py
#

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Category

log = logging.getLogger('inventory.categories.forms')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()

    def clean(self):
        parent = self.cleaned_data.get('parent')
        name = self.cleaned_data.get('name')
        owner = self.cleaned_data.get('owner')
        names = Category.objects.filter(name=name)
        log.debug("All %s names in all trees: %s", name, names)

        if Category.DEFAULT_SEPARATOR in name:
            msg = _(("A category name cannot contain the category delimiter"
                     " '{}'.").format(Category.DEFAULT_SEPARATOR))
            raise ValidationError(msg)

        if parent:
            # Test saving a category to itself.
            if name == parent.name:
                msg = _("You cannot save a category as a child to itself.")
                raise forms.ValidationError(msg)

            # Test that this name does not already exist as a node in this
            # tree.
            if not self.initial:
                node_trees = Category.objects.get_all_root_trees(name, owner)
                log.debug("All root trees: %s", node_trees)
                parents = Category.get_parents(parent)
                parents.append(parent)
                log.debug("Parents: %s", parents)
                flag = False

                for nset in node_trees:
                    for parent in parents:
                        if parent in nset:
                            flag = True

                if flag:
                    msg = _(("A category in this tree with name [{}] "
                             "already exists.").format(name))
                    raise forms.ValidationError(msg)
        # Test that there is not already a root category with this value.
        elif not self.initial and name in [item.name for item in names
                                           if not item.parent]:
            msg = _(("A root level category name [{}] already "
                     "exists.").format(name))
            raise forms.ValidationError(msg)

        return self.cleaned_data

/*
 * Project view
 *
 * js/views/project_view.js
 */

"use strict";


// Single project view
App.Views.Project = Backbone.View.extend({

  render: function() {
    // Get this model's public_id
    var publicId = this.model.get('public_id');
    // public_id
    this.$el.find('.project-public-id label.value-label').html(
      App.models.projectMeta.get('public_id').label);
    this.$el.find('.project-public-id span.value').html(publicId);
    this.$el.find('.project-public-id span.help').html(
      App.models.projectMeta.get('public_id').help_text);
    // inventory_type
    this.$el.find('.project-inventory-type label.value-label').html(
      App.models.projectMeta.get('inventory_type').label);
    this.getInventoryTypes();
    this.$el.find('.project-inventory-type span.help').html(
      App.models.projectMeta.get('inventory_type').help_text);
    // name
    this.$el.find('.project-name label.value-label').html(
      App.models.projectMeta.get('name').label);
    this.$el.find('.project-name input.value').val(this.model.get('name'));
    this.$el.find('.project-name span.help').html(
      App.models.projectMeta.get('name').help_text);
    // image
    this.$el.find('.project-image label.value-label').html(
      App.models.projectMeta.get('image').label);
    //this.$el.find('.project-image button[name="project-logo"]');
    this.$el.find('.project-image span').html(this.model.get('image'));
    this.$el.find('.project-image span.help').html(
      App.models.projectMeta.get('image').help_text);
    // membership
    this.$el.find('.project-membership label.value-label').html(
      App.models.projectMeta.get('memberships').label);
    this.$el.find('.project-membership span.help').html(
      App.models.projectMeta.get('memberships').help_text);
    // public
    this.$el.find('.project-public label.value-label').html(
      App.models.projectMeta.get('public').label);
    this.$el.find('.project-public input.value').val(this.model.get('public'));
    this.getYesNo('public', '.project-public select.value');
    this.$el.find('.project-public span.help').html(
      App.models.projectMeta.get('public').help_text);
    // active
    this.$el.find('.project-active label.value-label').html(
      App.models.projectMeta.get('active').label);
    this.$el.find('.project-active input.value').val(this.model.get('active'));
    this.getYesNo('active', '.project-active select.value');
    this.$el.find('.project-active span.help').html(
      App.models.projectMeta.get('active').help_text);
    // creator
    this.$el.find('.project-creator label.value-label').html(
      App.models.projectMeta.get('creator').label);
    this.$el.find('.project-creator span.value').html(
      this.model.get('creator'));
    //this.$el.find('.project-creator span.help').html(
    //  App.models.projectMeta.get('creator').help_text);
    // created
    this.$el.find('.project-created label.value-label').html(
      App.models.projectMeta.get('created').label);
    this.$el.find('.project-created span.value').html(
      this.model.get('created'));
    //this.$el.find('.project-created span.help').html(
    //  App.models.projectMeta.get('created').help_text);
    // updater
    this.$el.find('.project-updater label.value-label').html(
      App.models.projectMeta.get('updater').label);
    this.$el.find('.project-updater span.value').html(
      this.model.get('updater'));
    //this.$el.find('.project-updater span.help').html(
    // App.models.projectMeta.get('updater').help_text);
    // updated
    this.$el.find('.project-updated label.value-label').html(
      App.models.projectMeta.get('updated').label);
    this.$el.find('.project-updated span.value').html(
      this.model.get('updated'));
    //this.$el.find('.project-updated span.help').html(
    //  App.models.projectMeta.get('updated').help_text);

    // Setup some events
    var base = '#projects #' + publicId;
    var file = base + ' button[name="project-logo"]';
    var setFile = base + ' input[type="file"]';
    var save = base + ' button[name="project-save"]';
    $(file).on('click', this.openFileBox.bind(this));
    $(setFile).on('change', {self: this}, this.setupImage);
    $(save).on('click', this.saveModel.bind(this));
    },

  getInventoryTypes: function() {
    var option = "<option></option>";
    var $select = this.$el.find('.project-inventory-type select.value');
    var $option = null, optionPublicId = '';
    var publicId = this.model.get('inventory_type_public_id');

    _.forEach(App.collections.inventoryType, function(value, key) {
      $option = $(option);
      optionPublicId = App.collections.inventoryType.at(key).get('public_id');

      if(publicId === optionPublicId) {
        $option.prop('selected', true);
      }

      $option.val(optionPublicId);
      $option.text(App.collections.inventoryType.at(key).get('name'));
      $option.appendTo($select);
    });
  },

  getYesNo: function(field, select) {
    var option = "<option></option>";
    var $option = null;
    var optionValue = this.model.get(field);
    var $select = this.$el.find(select);

    // Use the `public` meta values for all booleans.
    _.forEach(App.models.projectMeta.get('public').choices,
      function(value, key) {
      $option = $(option);

      if(value.value === optionValue) {
        $option.prop('selected', true);
      }

      $option.val(value.value);
      $option.text(value.display_name);
      $option.appendTo($select);
    });
  },

  openFileBox: function(event) {
    var $fi = this.$el.find('input[type="file"]');
    // Clear out previous images.
    $fi.empty();
    $fi.attr('type', '');
    $fi.attr('type', 'file');
    $fi.trigger('click');
  },

  setupImage: function(event) {
    var self = event.data.self;
    var files = $(this).prop('files');

    if(files.length > 0) {
      $('#project-filename').text(files[0].name);
    }
  },

  saveModel: function(event) {
    event.preventDefault();
    App.utils.setLogin();
    this.model.save()
      .done(function(result) {
        console.log(result);
      })
      .fail(function(error) {
        App.utils.showMessage(error.responseJSON.detail);
      });

    return false;
  }
});


App.viewFunctions.project = function(model) {
  var publicId = model.get('public_id');
  var $template = $(App.templates.project_template());
  $template.appendTo($('#projects #' + publicId));
  var options = {
    template: $template[0],
    model: model,
    el: "#" + publicId
  };

  new App.Views.Project(options).render();
};

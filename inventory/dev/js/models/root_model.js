/*
 * API root model
 *
 * js/models/root_model.js
 */

"use strict";


App.Models.RootModel = Backbone.Model.extend({
  urlRoot: API_ROOT,
  defaults: {},
  mutators: {
    collection: {
      set: function(key, value, options, set) {
        var self = this;

        _.forEach(value, function(value, key) {
          if(key === 'items') {
            _.forEach(value, function(value, key) {
              self.set(key, value, options);
            });
          } else {
            self.set(key, value, options);
          }
        });
      }
    }
  }
});

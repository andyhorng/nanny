# import
MainView = eztable.backbone.MainView
FormView = eztable.backbone.FormView

class {{resource_class}} extends Backbone.Model

class {{resource_collection_class}} extends Backbone.Collection
    model: {{resource_class}}
    url: '{{resource_url}}'

$ ()->
    {{resource_collection_variable}} = new {{resource_collection_class}}
    main = new MainView
        model: {{resource_collection_variable}}

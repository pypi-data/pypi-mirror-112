function initEditorCkDjango(editor_ck__hidden_image_id, widget_attrs_id) {
    let prefix = 'editor_ck__hidden_image_';
    let __widget_attrs_id = editor_ck__hidden_image_id.replace(prefix, '')
    if (__widget_attrs_id === widget_attrs_id && __widget_attrs_id.indexOf('__prefix__') !== -1) {
        return;
    }

    let _editorConfig = {};
    try {
        _editorConfig = document.getElementById(__widget_attrs_id).attributes["field_settings"].nodeValue;
        _editorConfig = JSON.parse(_editorConfig);
    } catch (e) {
        _editorConfig = {};
    }
    ClassicEditor.create(
        document.querySelector('#' + __widget_attrs_id),
        _editorConfig
    ).then(editor => {
    }).catch(err => {
    });
    /*let ppp = []
    ClassicEditor.builtinPlugins.map(plugin => {
        ppp.push(plugin.pluginName)
    });
    console.log(ppp)*/
}